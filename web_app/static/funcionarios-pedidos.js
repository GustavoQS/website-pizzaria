document.addEventListener('DOMContentLoaded', function () {
    // PAGINA COZINHA
    const btnsCozinha = document.querySelectorAll('.finalizar-cozinha');
    btnsCozinha.forEach( function (btnCozinha) {
        btnCozinha.addEventListener('click', function () {
            const idPedidoCozinha = btnCozinha.getAttribute('data-id');
            finalizarCozinha(idPedidoCozinha, 1)
        });
    });

    const btnsCancelarCozinha = document.querySelectorAll('.cancelar-cozinha');
    btnsCancelarCozinha.forEach( function (btnCancelarCozinha) {
        btnCancelarCozinha.addEventListener('click', function () {
            const idPedidoCozinha = btnCancelarCozinha.getAttribute('data-id');
            finalizarCozinha(idPedidoCozinha, 0)
        });
    });

    function finalizarCozinha(orderId, finalizado) {
        fetch('/pedidos/cozinha', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: orderId, preparado: finalizado }),
        })
        .then(() => {
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
    }

    // PAGINA ENTREGA
    const btnsEntrega = document.querySelectorAll('.finalizar-entrega');
    btnsEntrega.forEach( function (btnEntrega) {
        btnEntrega.addEventListener('click', function () {
            const idPedidoEntrega = btnEntrega.getAttribute('data-id');
            finalizarEntrega(idPedidoEntrega)
        });
    });

    function finalizarEntrega(orderId) {
        fetch(`/pedidos/entrega`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: orderId }),
        })
        .then(() => {
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
    }

    // TODAS PAGINAS COM /funcionarios
    
    // Função para reiniciar a página
    function refreshPage() {
        location.reload();
    }
    // reinicia a cada X milisegundos
    setInterval(refreshPage, 10000);

    const cardPedido = document.querySelectorAll('.card-pedido');
    for (let i=0; i < cardPedido.length; i+=2) {
        const cardum = cardPedido[i];
        const carddois = cardPedido[i + 1];

        const maxH = Math.max(cardum.clientHeight, carddois.clientHeight);
        
        cardum.style.height = `${maxH}px`;
        carddois.style.height = `${maxH}px`;
    }


});