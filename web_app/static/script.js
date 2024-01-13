document.addEventListener('DOMContentLoaded', function () {

    // MOSTRAR INFORMAÇÃO DO PRODUTO QUE USUÁRIO CLICAR

    // selecione todos os card com .produto da HOME
    const produtos = document.querySelectorAll('.produto');
    // add event listener para cada .produto da HOME
    produtos.forEach(function (produto) {
        produto.addEventListener('click', function () {
            
            // pega informação do produto pelo atributo data-id
            const produtoId = produto.getAttribute('data-id');

            getProdutoInfoById(produtoId, 0);
        });
    });
    
    // selecione todos os card da SACOLA
    const itemsSacola = document.querySelectorAll('.itemSacola');
    // add event listener para cada .produto da SACOLA
    itemsSacola.forEach(function (item) {
        item.addEventListener('click', function () {
            // pega informação do produto pelo atributo data-id
            
            const itemSacolaId = item.getAttribute('data-id');
        
            getProdutoInfoById(itemSacolaId, 1);
        });
    }); 
    

    // PESQUISA DINAMICA
    var textoInput = document.getElementById('pesquisa-input');
    textoInput.addEventListener('input', function () {
        var query = textoInput.value;

        //ajax request
        fetch('/search?q=' + query)
            .then(response => response.json())
            .then( data => {
                resultadoPesquisa(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // SACOLA
    const sacolaDiv = document.querySelector('.nav-sacola-inner');
    if (sacolaDiv) {
        sacolaDiv.addEventListener('click', function () {
            mostrarSacola();
        });
    }
    

    // btn CONFIRMAR PEDIDO
    const btnConfirmar = document.getElementById('btn-confirmar-pedido');
    btnConfirmar.addEventListener('click', function () {
        confirmarPedido();
    } );


    // MOSTRAR INFORMAÇÃO DO PRODUTO QUE USUÁRIO CLICAR
    function getProdutoInfoById(produtoId, btnsacola) {
        fetch(`/api/get_produto_info/${produtoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(produtoInfo => {
                // att menu canvas
                document.querySelector('.produto-nome').textContent = produtoInfo.nome;
                document.querySelector('.produto-descricao').textContent = produtoInfo.descricao;
                
                const produtoImg = document.querySelector('.produto-img');
                produtoImg.src = produtoInfo.img;

                // mostra menu canvas
                var infoCanvas = new bootstrap.Offcanvas(document.getElementById('info-offcanvas'));

                var obsItem = document.getElementById('obsItem');
                obsItem.value = '';

                let qnt = document.querySelector('.qnt');
                if (btnsacola == 0) { // se clicou em um item fora da sacola
                    document.getElementById('form-s').value = 0;
                    
                    document.getElementById('btn-info-add').textContent = 'Adicionar';

                    qnt.textContent = 1;
                    quantidadeProduto = 1;
                    document.getElementById('form-qnt').value = quantidadeProduto;

                    let precoFormatado = produtoInfo.valor.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });;
                    document.querySelector('.produto-valor').textContent = "R$ " + precoFormatado;

                } else if (btnsacola = 1) { // se clicou em um item na sacola
                    document.getElementById('form-s').value = 1;

                    obsItem.value = produtoInfo.obsItem;
                    obsItem.setAttribute('index', produtoInfo.obsItem )

                    document.getElementById('btn-info-add').textContent = 'Atualizar sacola';

                    qnt.textContent = produtoInfo.qnt;
                    quantidadeProduto = produtoInfo.qnt;
                    document.getElementById('form-qnt').value = produtoInfo.qnt;
                    
                    let precoFormatado = produtoInfo.valortotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });;
                    document.querySelector('.produto-valor').textContent = "R$ " + precoFormatado;
                } 
                  
                document.getElementById('form-id').value = produtoId;
                infoCanvas.show(); 

                // ADICIONAR OU DIMINUIR QUANTIDADE DO PRODUTO 
                // add qnt
                document.querySelector('.mais-qnt').onclick = function () {
                    if (parseInt(qnt.textContent) < 1) {
                        qnt.textContent = 1;
                    }

                    let qntAtual = parseInt(qnt.textContent);
                    if (qntAtual >= 0) {
                        // att quantidade de unidades a serem compradas
                        let qntNovo = qntAtual + 1;
                        qnt.textContent = qntNovo;
                        quantidadeProduto = qntNovo;
                        document.getElementById('form-qnt').value = quantidadeProduto;
                        // att preco conforme preco segundo a API
                        let precoFinal = produtoInfo.valor * qntNovo;
                        precoFinal = precoFinal.toFixed(2)
                        document.querySelector('.produto-valor').textContent = "R$ " + precoFinal;
                    }
                }
                // diminui qnt
                document.querySelector('.menos-qnt').onclick = function () {
                    if (parseInt(qnt.textContent) < 0) {
                        qnt.textContent = 0;
                    }

                    let qntAtual = parseInt(qnt.textContent);
                    if (qntAtual > 0) {
                        // att quantidade de unidades a serem compradas
                        let qntNovo = qntAtual - 1;
                        qnt.textContent = qntNovo;
                        quantidadeProduto = qntNovo;
                        document.getElementById('form-qnt').value = quantidadeProduto;
                        // att preco conforme preco segundo a API
                        let precoFinal = produtoInfo.valor * qntNovo;
                        precoFinal = precoFinal.toFixed(2)
                        document.querySelector('.produto-valor').textContent = "R$ " + precoFinal;
                    }
                }

                return produtoInfo.qnt;
                
            })
            .catch(error => {
                console.error('Error fetching pizza info:', error);
            });
    }

    // mostrar resultados da pesquisa dentro do canvas de pesquisa
    function resultadoPesquisa(resultados) {
        var divResultados = document.querySelector('.resultados-pesquisa');
        divResultados.innerHTML = '';

        //att div resultados
        resultados.forEach(function (item) {
            var cardResultado = '<div class="card card-pesquisa mb-3 produto" data-id="' + item.id + '"><div class="row g-0"><div class="col-sm-4" ><img src="' + item.img + '" class="img-fluid rounded-start h-100" alt="' + item.nome + '"></div><div class="col-sm-8"><div class="card-body card-pesquisa h-100 d-flex flex-column"><div class="align-self-start flex-fill"><h5 class="card-title">' + item.nome + '</h5><p class="card-text">' + item.descricao + '</p></div><div class="d-flex align-items-end"><h4 class="text-end mb-0 mt-2">R$ ' + item.valor + '</h4></div></div></div></div></div>';
            divResultados.insertAdjacentHTML('beforeend', cardResultado);

            var produtoPesq = divResultados.lastElementChild;
            produtoPesq.addEventListener('click', function () {
                getProdutoInfoById(item.id);
            });
            

        });
    }

    function mostrarSacola() {
        // mostra menu canvas
        const offcanvas = new bootstrap.Offcanvas(document.getElementById('sacola-offcanvas'));
        offcanvas.show();
    }
    
    function confirmarPedido () {
        const offcanvasConfirmar = new bootstrap.Offcanvas(document.getElementById('confirmar-offcanvas'));
        offcanvasConfirmar.show()

    }

});


(function(){

    const cep = document.querySelector("input[name=cep]");
  
    cep.addEventListener('blur', e=> {
        const value = cep.value.replace(/[^0-9]+/, '');
        const url = `https://viacep.com.br/ws/${value}/json/`;
      
        fetch(url)
        .then( response => response.json())
        .then( json => {
              
            if( json.logradouro ) {
                document.querySelector('input[name=rua]').value = json.logradouro;
                document.querySelector('input[name=bairro]').value = json.bairro;
                document.querySelector('input[name=cidade-estado]').value = json.localidade + " - " + json.uf;
            }
      
        });
      
    });

})();
