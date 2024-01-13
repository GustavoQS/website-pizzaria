## La Família D'Pizza - Visualização

Assista ao [vídeo]() do projeto em execução no meu canal do Youtube.

## Navegação

- [Cliente](#cliente)
  - [Home](#home)
  - [Seleção de Item](#seleção-de-item)
  - [Pesquisa](#pesquisa)
  - [Sacola](#sacola)
  - [Confirmar pedido](#confirmar-pedido)
  - [Status do pedido](#status-do-pedido)
    
- [Funcionário](#funcionário)
  - [Login](#login)
  - [Home dos funcionários](#home-dos-funcionários)
  - [Ver cardápio](#ver-cardápio)
  - [Adicionar item](#adicionar-item)
  - [Editar item](#editar-item)
  - [Cozinha](#cozinha)
  - [Entrega](#entrega)
  - [Pedidos concluídos](#pedidos-concluídos)
  - [Pedidos cancelados](#pedidos-cancelados)
  - [Registro de funcionário](#registro-de-funcionário)

- [Mensagem de erro](#mensagem-de-erro)

## Cliente

Veja as funcionalidades que os clientes do website tem acesso

### Home
  - Página inicial do usuário, para visualizar o cardápio
    
    ![Home](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/sacola.png)

### Seleção de Item
  - Este canvas aparece quando o usuário clica em algum item do cardápio

    ![info](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/info-produto.png)

### Pesquisa
  - Quando o usuário clica no ícone da lupa, este canvas aparece. Possibilita o usuário fazer uma pesquisa dinâmica.

    ![Pesquisa](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/pesquisa.png)

### Sacola
  - Canvas que mostra a sacola do usuário, com os itens adicionados.
  - Também permite alterações na sacola, basta clicar no item que um canvas de [Seleção de Item](#seleção-de-tem) aparece, mas adaptado as funcionalidades da sacola.

    ![sacola](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/canvas-sacola.png)

### Confirmar Pedido
  - Este canvas fica visível quando o usuário seleciona a opção "Confirmar Pedido" na sacola.
  - Aqui que a [API ViaCep](https://viacep.com.br/) é utilizada.

    ![confirmar](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/canvas-confirmarpedido.png)

### Status do pedido
  - Após confirmar o pedido, o usuário pode verificar o status do mesmo, através do ID de pedido
  - Esta página é automaticamente aberta ao confirmar o pedido

    1. Sendo preparado
       
       ![preparando](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/pedido-preparando.png)

    2. A caminho

       ![emrota](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/pedido-caminho.png)

    3. Entregue

       ![entregue](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/usuario/pedido-entregue.png)

## Funcionário

Funcionalidades que apenas os funcionários tem acesso, após passarem por um sistema de login

### Login
  - Sistema que permite o login de funcionários
    
    ![login](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/login.png)

### Home dos funcionários
  - Página inicial dos usuários, que os permitem selecionar onde desejam ser redirecionados.
    
    ![home-funcionarios](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/home.png)

### Ver cardápio
  - Página que permite visualizar o cardápio, abrindo possibilidade do uso de mais funções
    
    ![homecardapio](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/cardapio.png)

### Adicionar item
  - Canvas que permite a adição de um novo item
    
    ![novoitem](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/canvas-novoitem.png)

### Editar item
  - Modificação de item ja existente
    
    ![modificar](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/canvas-editaritem.png)

### Cozinha
  - Visualização de pedidos a serem preparados
    
    ![cozinha](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/pedidos-cozinha.png)

### Entrega
  - Permite visualizar pedidos que estão a caminho do endereço do cliente
    
    ![entrega](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/pedidos-entrega.png)

### Pedidos concluídos
  - Veja os pedidos que foram entregues e concluídos
    
    ![sucesso](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/pedidos-concluidos.png)

### Pedidos cancelados
  - Pedidos que por algum motivo, foram cancelados no processo de preparo ou entrega.
    
    ![cancelado](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/pedidos-cancelados.png)

### Registro de funcionário
  - Formulário para registro de um novo funcionário
    
    ![registro](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/registrar.png)

## Mensagem de erro

Mensagem que aparece quando algum erro inesperado acontece.

![error](https://github.com/GustavoQS/webiste-pizzaria/blob/master/screenshots/funcionario/error.png)
