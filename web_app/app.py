import uuid
import secrets
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, jsonify, request, session, redirect, Flask

from web_app.functions import ver_cardapio, total_sacola, ver_sacola, itens_dos_pedidos, test_uuid
from web_app.models import DB

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def index():
    userId = session.get('userId')
    if not userId:
        session['userId'] = str(uuid.uuid4())
        session['sacola'] = []

    cardapio = ver_cardapio()
    sacola = ver_sacola()
    total = total_sacola()

    if sacola == []:
        sacola = 0

    return render_template("index.html", comida=cardapio, userId=userId, sacola=sacola, total=total)


@app.route("/api/get_produto_info/<int:produtoId>")
def get_produto_info(produtoId):

    temp = {}
    naSacola = 0
    produto_info = {}

    # procura item selecionado no cardapio
    comida = ver_cardapio()
    for i in comida:
        if i['id'] == produtoId:
            temp = i

    index = -5

    for i in session['sacola']:
        if i['id'] == produtoId:
            index = session['sacola'].index(i)

    qnt = 1
    # se item esta no cardapio
    if temp:
        # pega todas as informações do item no bd
        sacola = ver_sacola()
        # verifica se o item ja esta na sacola
        for i in sacola:
            if i['id'] == produtoId:
                naSacola = 1
                qnt = i['qnt']

        # se item na sacola, quantidade do item = quantidade do item da sacola
        if naSacola:
            produto_info = {
                "id": temp['id'],
                "nome": temp['nome'],
                "descricao": temp['descricao'],
                "valor": temp['valor'],
                "valortotal": temp['valor']*qnt,
                "img": temp['img'],
                "nasacola": 1,
                "qnt": qnt,
                "obsItem": session['sacola'][index]['obsItem']
            }
        # senao, quantidade do item = 1 (padrao)
        elif not naSacola:
            produto_info = {
                "id": temp['id'],
                "nome": temp['nome'],
                "descricao": temp['descricao'],
                "valor": temp['valor'],
                "valortotal": temp['valor']*qnt,
                "img": temp['img'],
                "nasacola": 0,
                "qnt": 1,
            }

        return jsonify(produto_info)
    else:
        return jsonify({'error': 'Produto não encontrado'}), 404


@app.route("/search")
def search():
    comida = ver_cardapio()
    query = request.args.get('q', '')
    resultados = [item for item in comida if query.lower() in item['nome'].lower() or  query.lower() in item['descricao'].lower()]

    return jsonify(resultados)


@app.route("/api/addSacola", methods=['POST'])
def add_sacola():

    produtoId = int(request.form.get('id'))
    qnt = int(request.form.get('qnt'))
    sacola = int(request.form.get('s'))
    # se sacola == 0 -> usuário acrescentar X quantidade do item
    # senao -> usuário quer modificar a quantidade do item na sacola
    obs = str(request.form.get('obsItem'))

    possui = False

    for i in session['sacola']:

        # se usuário ja tem item na sacola
        if i['id'] == produtoId:
            index = session['sacola'].index(i)

            possui = True

            if qnt == 0:
                del session['sacola'][index]
                session.modified = True
                break

            # usuário acrescentar X quantidade do item
            if sacola == 0:

                i['qnt'] += qnt
                if obs:
                    i['obsItem'] += ' ; ' + obs

            # usuário quer modificar a quantidade do item na sacola
            elif sacola == 1:

                i['qnt'] = qnt

                if obs != i['obsItem']:
                    i['obsItem'] = ' ' + obs

            # remove item antigo da sacola e atualiza com informações novas
            index = session['sacola'].index(i)
            del session['sacola'][index]
            session['sacola'].append(i)
            session.modified = True
            break

    # se usuário não tem item na sacola
    if not possui:
        session['sacola'].append({'id': produtoId, 'qnt': qnt, 'obsItem': str(obs)})
        session.modified = True

    return redirect('/')


@app.route('/api/confirmarpedido', methods=['POST'])
def confirmar_pedido():

    if session['sacola'] != []:
        hora = datetime.now()
        nome = request.form.get('nomeusr')
        tel = request.form.get('fone')
        cep = request.form.get('cep')
        rua = request.form.get('rua')
        num = request.form.get('num')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        ciduf = request.form.get('cidade-estado')
        pagamento = request.form.get('pagamento')

        valorT = total_sacola()

        if not complemento:
            complemento = '-'

        if nome and tel and cep and rua and num and bairro and ciduf:
            sucesso = False
            # add ao banco de dados
            try:
                # add pedido
                with DB() as db:
                    query = 'INSERT INTO pedidos (pedidoId, nome, tel, cep, rua, num, obsEnd, valorT, pagamento, dataHora, preparado, entregue, cancelado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    db.edit(query, (session['userId'], nome, tel, cep, rua, num, complemento, valorT, str(pagamento), hora, '0', '0', '0' ))

                    # add cada item do pedido
                    querry2 = 'INSERT INTO itenspedidos (pedidoId, itemId, qnt, valor, obsItem) VALUES (%s, %s, %s, %s, %s)'
                    detalhes_sacola = ver_sacola()
                    # nested loop para achar mais informações de cada item na sacola e inserir no banco de dados
                    for item in detalhes_sacola:
                        for item_session in session['sacola']:
                            if item_session['id'] == item['id']:
                                db.edit(querry2, (session['userId'], item['id'], item['qnt'], item['valor'], item_session['obsItem']))

                    print("NOVO Pedido # " + session['userId'] + " inserido com SUCESSO as " + str(hora)[11:19] + " na data " + str(hora)[:10])
                    sucesso = True

            except Exception as e:
                print(f'MySQL erro: {e}')

            if sucesso:
                id = session['userId']

                session.pop('userId', None)
                session.pop('sacola', None)
                session.pop('funcionarioId', None)

                return redirect(f'/status/{id}')

    return redirect('/')


# verifica status do pedido
@app.route('/status/<pedido_id>')
def status_pedido(pedido_id):
    if test_uuid(pedido_id):
        try:
            with DB() as db:
                query = 'SELECT datahora, preparado, entregue, cancelado FROM pedidos WHERE pedidoId = %s'
                id = (pedido_id,)
                resultado = db.select_att(query, id)
        except Exception as e:
            print(f'MySQL erro: {e}')

        hora = str(resultado[0][0])[11:19]
        data = str(resultado[0][0])[:10]
        cozinha = resultado[0][1]
        entregue = resultado[0][2]
        cancelado = resultado[0][3]

        mensagem = ''
        if cancelado == 1:
            mensagem = 'Seu pedido foi cancelado!'
        elif cozinha == 0 and entregue == 0:
            mensagem = 'Seu pedido esta sendo preparado!'
        elif cozinha == 1 and entregue == 0:
            mensagem = 'Seu pedido esta a caminho de você!'
        elif entregue == 1:
            mensagem = 'Seu pedido ja foi entregue!'

        return render_template('status.html', pedidoId=pedido_id, status=mensagem, data=data, hora=hora)
    else:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('userId', None)
    session.pop('sacola', None)

    # se ja logado
    funcionarioId = session.get('funcionarioId')
    if funcionarioId:
        return redirect('/funcionarios/home')

    if request.method == 'POST':
        print("Logando como funcionário...")

        usuario = request.form.get('usuario')
        senha = str(request.form.get('senha'))
        if not senha or not usuario:
            return redirect('/login')

        resultado = []
        try:
            with DB() as db:
                arg = (usuario,)
                verificar = 'SELECT * FROM funcionarios WHERE usuario = %s'
                resultado = db.select_att(verificar, arg)
        except Exception as e:
            print(f'MySQL erro: {e}')

        if resultado == []:
            print('Usuário Inválido')
            return redirect('/login')

        if resultado[0][1] != usuario:
            print('Usuário Inválido')
            return redirect('/login')

        if not check_password_hash(resultado[0][2], senha):
            print('Senha diferente')
            return redirect('/login')

        session['funcionarioId'] = resultado[0]

        return redirect('/funcionarios/home')

    return render_template('pedidos-login.html')


@app.route('/logout')
def logout():
    session.pop('userId', None)
    session.pop('sacola', None)

    session.pop('funcionarioId', None)

    return redirect('/')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/funcionarios/home')

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = str(request.form.get('senha'))
        confsenha = str(request.form.get('confsenha'))

        if not usuario:
            print('Preencha campo usuário')
            return redirect('/registrar')
        if not senha:
            print('Preencha campo senha')
            return redirect('/registrar')
        if not confsenha:
            print('Preencha campo confirmação de senha')
            return redirect('/registrar')

        if senha != confsenha:
            print('senhas diferentes')
            return redirect('/registrar')

        resultado = []
        try:
            with DB() as db:
                arg = (usuario,)
                verificar = 'SELECT * FROM funcionarios WHERE usuario = %s'
                resultado = db.select_att(verificar, arg)
        except Exception as e:
            print(f'MySQL erro: {e}')

        if resultado == []:
            print('Inserindo novo funcionário')
            hash_senha = generate_password_hash(senha)
            ultimo_login = datetime.now()

            try:
                with DB() as db:
                    novo_funcionario = 'INSERT INTO funcionarios (usuario, senha, ultimoAcesso) VALUES (%s, %s, %s)'
                    db.edit(novo_funcionario, (str(usuario), hash_senha, ultimo_login))
            except Exception as e:
                print(f'MySQL erro: {e}')

        else:
            print('Usuário ja existe')
            return redirect('/registrar')

    return render_template('funcionarios-registrar.html')


@app.route('/funcionarios/home')
def funcionarios_home():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    return render_template('funcionarios-index.html')


@app.route('/pedidos/cozinha', methods=['POST', 'GET'])
def cozinha():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    resultado = []
    try:
        with DB() as db:
            query = 'SELECT * FROM pedidos WHERE preparado = 0 AND cancelado = 0 ORDER BY (datahora) DESC'
            resultado = db.select(query)
    except Exception as e:
        print(f'MySQL erro: {e}')

    itensPedidos = itens_dos_pedidos(resultado)

    vazio = 0
    if itensPedidos == []:
        vazio = 1

    if request.method == 'POST':
        data = request.get_json()
        pedido_id = data.get('id')
        preparado = data.get('preparado')

        if preparado == 1:
            try:
                with DB() as db:
                    query2 = f'UPDATE pedidos SET preparado = 1 WHERE pedidoId = %s'
                    arg = (pedido_id,)
                    db.edit(query2, arg)
            except Exception as e:
                print(f'MySQL erro: {e}')

        elif preparado == 0:
            try:
                with DB() as db:
                    query2 = f'UPDATE pedidos SET cancelado = 1 WHERE pedidoId = %s'
                    arg = (pedido_id,)
                    db.edit(query2, arg)
            except Exception as e:
                print(f'MySQL erro: {e}')

        return redirect('/pedidos/cozinha')

    return render_template('pedidos-cozinha.html', pedidos=itensPedidos, sempedidos=vazio)


@app.route('/pedidos/entrega', methods=['POST', 'GET'])
def entrega():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    resultado = []
    try:
        with DB() as db:
            query = 'SELECT * FROM pedidos WHERE preparado = 1 AND entregue = 0 AND cancelado = 0 ORDER BY (datahora) DESC'
            resultado = db.select(query)
    except Exception as e:
        print(f'MySQL erro: {e}')

    itensPedidos = itens_dos_pedidos(resultado)

    vazio = 0
    if itensPedidos == []:
        vazio = 1

    if request.method == 'POST':
        data = request.get_json()
        pedido_id = data.get('id')

        try:
            with DB() as db:
                query3 = f'UPDATE pedidos SET entregue = 1 WHERE pedidoId = %s'
                arg = (pedido_id,)
                db.edit(query3, arg)
        except Exception as e:
            print(f'MySQL erro: {e}')

        return redirect('/pedidos/entrega')

    return render_template('pedidos-entrega.html', pedidos=itensPedidos, sempedidos=vazio)


@app.route('/pedidos/cancelados')
def cancelados():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    resultado = []
    try:
        with DB() as db:
            query = 'SELECT * FROM pedidos WHERE cancelado = 1 ORDER BY (datahora) DESC'
            resultado = db.select(query)
    except Exception as e:
        print(f'MySQL erro: {e}')

    itensPedidos = itens_dos_pedidos(resultado)

    return render_template('pedidos-cancelados.html', pedidos=itensPedidos)


@app.route('/pedidos/concluidos')
def concluidos():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    resultado = []
    try:
        with DB() as db:
            query = 'SELECT * FROM pedidos WHERE preparado = 1 AND entregue = 1 AND cancelado = 0 ORDER BY (datahora) DESC'
            resultado = db.select(query)
    except Exception as e:
        print(f'MySQL erro: {e}')

    itensPedidos = itens_dos_pedidos(resultado)

    return render_template('pedidos-concluidos.html', pedidos=itensPedidos)


@app.route('/cardapio', methods=['GET', 'POST'])
def editar_cardapio():
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    cardapio = ver_cardapio()

    if request.method == 'POST':
        id = int(request.form.get('id'))
        img = request.form.get('img')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        nome = request.form.get('nome')
        editar = int(request.form.get('editar'))
        tipo = request.form.get('opcaoTipo')

        if not tipo:
            print("Preencha tipo")
            return redirect('/cardapio')
        if not nome:
            print("Preencha nome")
            return redirect('/cardapio')
        if not preco:
            print('Preencha preco')
            return redirect('/cardapio')
        if not descricao:
            print('Preencha descricao')
            return redirect('/cardapio')
        if not img:
            print('Preencha img')
            return redirect('/cardapio')

        if editar == 1:
            if not id:
                print('Erro no id do item')
                return redirect('/cardapio')

            print("Editando Item no Cardápio")

            try:
                with DB() as db:
                    query_editar = 'UPDATE cardapio SET tipo = %s, nome = %s, descricao = %s, img = %s, preco = %s WHERE id = %s'
                    db.edit(query_editar, (str(tipo), nome, descricao, img, round(preco, 2), id))
            except Exception as e:
                print(f'MySQL erro: {e}')

            return redirect('/cardapio')

        elif editar == 0:
            print("Adicionando Item no Cardápio")
            try:
                with DB() as db:
                    query_add = f'INSERT INTO cardapio (tipo, nome, descricao, img, preco) VALUES (%s, %s, %s, %s, %s)'
                    db.edit(query_add, (str(tipo), nome, descricao, img, round(preco, 2)))
            except Exception as e:
                print(f'MySQL erro: {e}')

            return redirect('/cardapio')

        elif editar == 3:
            if not id:
                print('Erro no id')
                return redirect('/cardapio')

            print("Desabilitando Item no Cardápio")

            try:
                with DB() as db:
                    arg = (id,)
                    query_deletar = 'UPDATE cardapio SET habilitado = 0 WHERE id = %s'
                    db.edit(query_deletar, arg)
            except Exception as e:
                print(f'MySQL erro: {e}')

            return redirect('/cardapio')

        elif editar == 4:
            if not id:
                print('Erro no id do item')
                return redirect('/cardapio')

            print("Habilitando Item no Cardápio")

            try:
                with DB() as db:
                    arg = (id,)
                    query_deletar = 'UPDATE cardapio SET habilitado = 1 WHERE id = %s'
                    db.edit(query_deletar, arg)
            except Exception as e:
                print(f'MySQL erro: {e}')

            return redirect('/cardapio')

    return render_template('cardapio.html', cardapio=cardapio)


@app.route('/cardapio/ver/<int:produtoId>')
def funcionario_consultar_item(produtoId):
    funcionarioId = session.get('funcionarioId')
    if not funcionarioId:
        return redirect('/login')

    temp = {}

    # verifica se item est ano cardapio
    cardapio = ver_cardapio()
    for i in cardapio:
        if i['id'] == produtoId:
            temp = i

    if temp:
        produto_info = {
            "id": temp['id'],
            "nome": temp['nome'],
            "descricao": temp['descricao'],
            "preco": temp['valor'],
            "img": temp['img'],
            "tipo": temp['tipo']
        }
        return jsonify(produto_info)
    else:
        return jsonify({'error': 'Produto não encontrado'}), 404


@app.errorhandler(Exception)
def handle_exception(e):
    print(f"ERRO: {str(e)}")
    return render_template('error.html', erro='Algo deu errado. Tente novamente mais tarde.'), 500
