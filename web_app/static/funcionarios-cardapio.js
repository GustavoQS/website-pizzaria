document.addEventListener('DOMContentLoaded', function () {
// CARDAPIO

        // EDITAR item
        const produtos = document.querySelectorAll('.produto');
        produtos.forEach(function (produto) {
            produto.addEventListener('click', function () {
                
                // pega informação do produto pelo atributo data-id
                const produtoId = produto.getAttribute('data-id');

                let btnDeletarAtivar = document.getElementById('btn-pre-deletar');
                btnDeletarAtivar.innerText = 'Retirar do cardápio';
                btnDeletarAtivar.style.display = 'block';
                
                verParaEditarCardapio(produtoId, 1);
            });
        });

    // MOSTRAR INFORMAÇÃO DO PRODUTO QUE USUÁRIO CLICAR
    function verParaEditarCardapio(produtoId, editar) {
        fetch(`/cardapio/ver/${produtoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(produtoInfo => {
                // att menu canvas

                let produtoExistente = document.getElementById('form-produtoExistente');
                produtoExistente.value = editar;
                // se editar == 0 (add item)
                // se editar == 1 (editando item)
                // se editar == 3 (desabilitando item)
                // se editar == 4 (habilitando item)

                if (editar == 1) {
                    const btnDeletar = this.document.getElementById('btn-pre-deletar');
                    btnDeletar.setAttribute('data-id', produtoInfo.id);
                    btnDeletar.addEventListener('click', function () {
                        produtoExistente.value = 3;
                    });
                    document.querySelector('.produto-nome').value = produtoInfo.nome;

                    document.querySelector('.produto-descricao').value = produtoInfo.descricao;
                    
                    const produtoImg = document.querySelector('.produto-img');
                    produtoImg.src = produtoInfo.img;
                    const produtoImgLink = document.querySelector('.produto-img-input');
                    produtoImgLink.value = produtoInfo.img;

                    document.getElementById('form-id').value = produtoId;

                    let precoFinal = produtoInfo.preco;
                    document.querySelector('.produto-valor').value = precoFinal;

                    const opcaoTipo = document.getElementById('opcaoTipo');

                    for (const option of opcaoTipo.options) {
                        if (option.value == produtoInfo.tipo) {
                            option.selected = true;
                            break
                        }
                    }

                } else if (editar == 4) {
                    const btnDeletar = this.document.getElementById('btn-pre-deletar');
                    btnDeletar.setAttribute('data-id', produtoInfo.id);
                    btnDeletar.addEventListener('click', function () {
                        produtoExistente.value = 4;
                    });
                    produtoExistente.value = 1;
                    document.querySelector('.produto-nome').value = produtoInfo.nome;

                    document.querySelector('.produto-descricao').value = produtoInfo.descricao;
                    
                    const produtoImg = document.querySelector('.produto-img');
                    produtoImg.src = produtoInfo.img;
                    const produtoImgLink = document.querySelector('.produto-img-input');
                    produtoImgLink.value = produtoInfo.img;

                    document.getElementById('form-id').value = produtoId;

                    let precoFinal = produtoInfo.preco;
                    document.querySelector('.produto-valor').value = precoFinal;

                    const opcaoTipo = document.getElementById('opcaoTipo');

                    for (const option of opcaoTipo.options) {
                        if (option.value == produtoInfo.tipo) {
                            option.selected = true;
                            break
                        }
                    }
                }
                
                var btnConfirmar = document.getElementById('btn-confirmar-cardapio');
                btnConfirmar.innerText = 'Editar Item';

                // mostra menu canvas
                var infoCanvas = new bootstrap.Offcanvas(document.getElementById('info-offcanvas'));
                infoCanvas.show(); 
                
            })
            .catch(error => {
                console.error('Error fetching pizza info:', error);
            });
    }

    // DESABILITAR item
    var itensDesabilitados = document.querySelectorAll('.desabilitado-item');
    itensDesabilitados.forEach(function (item) {
        item.addEventListener('click', function () {
            
            // pega informação do produto pelo atributo data-id
            const produtoId = item.getAttribute('data-id');
            
            // ALTERAR TEXTO: btn que antes deletava, agora habilita
            let btnDeletarAtivar = document.getElementById('btn-pre-deletar');
            btnDeletarAtivar.innerText = 'Habilitar no cardápio';
            btnDeletarAtivar.style.display = 'block';

            verParaEditarCardapio(produtoId, 4);
        });
    });


    // ADD NOVO item
    var novoItem = document.querySelector('.novo-item');
    novoItem.addEventListener('click', function () {
        let btnDeletarDesativar = document.getElementById('btn-pre-deletar');
        btnDeletarDesativar.style.display = 'none';
        addCardapio(0);
    });

    function addCardapio(editar) {
        let produtoExistente = document.getElementById('form-produtoExistente');
        produtoExistente.value = editar;

        const produtoImg = document.querySelector('.produto-img');
        produtoImg.src = '../static/images/add.png';
        
        var btnConfirmar = document.getElementById('btn-confirmar-cardapio');
        btnConfirmar.innerText = 'Adicionar ao Cardápio';

        // mostra menu canvas
        var infoCanvas = new bootstrap.Offcanvas(document.getElementById('info-offcanvas'));
        infoCanvas.show(); 
    }

});