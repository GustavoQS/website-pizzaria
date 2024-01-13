import uuid

from web_app.app import session
from web_app.models import DB


# mostra todos os itens do cardapio no banco de dados
def ver_cardapio():
    resultado = []
    try:
        with DB() as db:
            query = 'SELECT * FROM cardapio'
            resultado = db.select(query)
    except Exception as e:
        print(f'MySQL: Erro ao consultar cardápio\nError: {e}')

    comida = []
    for i in resultado:
        comida.append({"id": i[0], "tipo": i[1], "nome": i[2], "descricao": i[3], "img": i[4], "valor": i[5], "habilitado": i[6]})

    return comida

# compara itens na sacola do usuario (cookie com id e quantidade) com itens do cardapio (banco de dados com tudo)
def ver_sacola():
    temp = session['sacola']
    sacola = []

    comida = ver_cardapio()
    # se existe sacola
    if temp:
        for i in comida:
            for j in temp:
                # verifica se item do cardapio == item na sacola
                if j['id'] == i['id']:
                    fvalor = j['qnt'] * i['valor']
                    sacola.append({'id': i['id'], 'qnt': j['qnt'], 'nome': i['nome'], 'img': i['img'],
                                   'descricao': i['descricao'], 'valor': fvalor})

    # retorna uma lista com tudo sobre cada item na sacola do usuario
    # baseado em informações do cardapio + quantidade e observações do item na sacola
    return sacola


def total_sacola():
    total = 0
    sacola = ver_sacola()
    for i in sacola:
        total += i['valor']

    return total


def verificar_sacola(produtoId):
    temp = session['sacola']

    for i in temp:
        if i['id'] == produtoId:
            return {'id': produtoId, 'qnt': i['qnt']}

    return False


def teste():
    itensdb = []
    try:
        db = DB()
        pedidoid = ('49816',)
        querry2 = 'SELECT * FROM itenspedidos WHERE pedidoID = %s'
        itensdb = db.select_att(querry2, pedidoid)
    except Exception as e:
        print(f'MySQL: {e}')
    finally:
        DB().close()
        print(itensdb)


def itens_dos_pedidos(resultado_query_pedidos):
    pedidos = []
    for i in resultado_query_pedidos:
        itensdb = []
        try:
            with DB() as db:
                pedidoid = (str(i[0]),)
                querry2 = 'SELECT * FROM itenspedidos WHERE pedidoID = %s'
                itensdb = db.select_att(querry2, pedidoid)
        except Exception as e:
            print(f'MySQL: {e}')

        sacola_usr = []
        for j in itensdb:
            x = nome_do_item(j[1])
            sacola_usr.append({'nome': x, 'qnt': j[2], 'valor': j[3], 'obsItem': j[4]})

        if i[9]:
            dataformatado = i[9].strftime("%Y-%m-%d %H:%M:%S")
        else:
            dataformatado = '-'

        pedidos.append(
            {'id': i[0], 'itens': sacola_usr, 'nome': i[1], 'tel': i[2], 'cep': i[3], 'rua': i[4], 'num': i[5],
             'obsEnd': i[6], 'valor': float(i[7]), 'pagamento': i[8], 'dataHora': dataformatado, 'preparado': i[10],
             'entregue': i[11], 'cancelado': i[12]})

    # print(pedidos[0]['itens'][0]['nome'])
    return pedidos


def nome_do_item(produtoId):
    temp = ver_cardapio()
    for i in temp:
        if i['id'] == produtoId:
            return i['nome']


def test_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False