## La Família D'Pizza - Visualização

[<img src="../screenshots/yt.png" alt="Assista ao vídeo" width="50%">](https://www.youtube.com/watch?v=cFS2MGdqH0w)

Assista ao [vídeo](https://www.youtube.com/watch?v=cFS2MGdqH0w) do projeto em execução no meu canal do Youtube.

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
    
    ![Home](../screenshots/usuario/sacola.png)

### Seleção de Item
  - Este canvas aparece quando o usuário clica em algum item do cardápio

    ![info](../screenshots/usuario/info-produto.png)

### Pesquisa
  - Quando o usuário clica no ícone da lupa, este canvas aparece. Possibilita o usuário fazer uma pesquisa dinâmica.

    ![Pesquisa](../screenshots/usuario/pesquisa.png)

### Sacola
  - Canvas que mostra a sacola do usuário, com os itens adicionados.
  - Também permite alterações na sacola, basta clicar no item que um canvas de [Seleção de Item](#seleção-de-tem) aparece, mas adaptado as funcionalidades da sacola.

    ![sacola](../screenshots/usuario/canvas-sacola.png)

### Confirmar Pedido
  - Este canvas fica visível quando o usuário seleciona a opção "Confirmar Pedido" na sacola.
  - Aqui que a [API ViaCep](https://viacep.com.br/) é utilizada.

    ![confirmar](../screenshots/usuario/canvas-confirmarpedido.png)

### Status do pedido
  - Após confirmar o pedido, o usuário pode verificar o status do mesmo, através do ID de pedido
  - Esta página é automaticamente aberta ao confirmar o pedido

    1. Sendo preparado
       
       ![preparando](../screenshots/usuario/pedido-preparando.png)

    2. A caminho

       ![emrota](../screenshots/usuario/pedido-caminho.png)

    3. Entregue

       ![entregue](../screenshots/usuario/pedido-entregue.png)

## Funcionário

Funcionalidades que apenas os funcionários tem acesso, após passarem por um sistema de login

### Login
  - Sistema que permite o login de funcionários
    
    ![login](../screenshots/funcionario/login.png)

### Home dos funcionários
  - Página inicial dos usuários, que os permitem selecionar onde desejam ser redirecionados.
    
    ![home-funcionarios](../screenshots/funcionario/home.png)

### Ver cardápio
  - Página que permite visualizar o cardápio, abrindo possibilidade do uso de mais funções
    
    ![homecardapio](../screenshots/funcionario/cardapio.png)

### Adicionar item
  - Canvas que permite a adição de um novo item
    
    ![novoitem](../screenshots/funcionario/canvas-novoitem.png)

### Editar item
  - Modificação de item ja existente
    
    ![modificar](../screenshots/funcionario/canvas-editaritem.png)

### Cozinha
  - Visualização de pedidos a serem preparados
    
    ![cozinha](../screenshots/funcionario/pedidos-cozinha.png)

### Entrega
  - Permite visualizar pedidos que estão a caminho do endereço do cliente
    
    ![entrega](../screenshots/funcionario/pedidos-entrega.png)

### Pedidos concluídos
  - Veja os pedidos que foram entregues e concluídos
    
    ![sucesso](../screenshots/funcionario/pedidos-concluidos.png)

### Pedidos cancelados
  - Pedidos que por algum motivo, foram cancelados no processo de preparo ou entrega.
    
    ![cancelado](../screenshots/funcionario/pedidos-cancelados.png)

### Registro de funcionário
  - Formulário para registro de um novo funcionário
    
    ![registro](../screenshots/funcionario/registrar.png)

## Mensagem de erro

Mensagem que aparece quando algum erro inesperado acontece.

![error](../screenshots/error.png)
