document.addEventListener('DOMContentLoaded', function () {

    var loginAdm = document.getElementById('login-adm');
    loginAdm.addEventListener('click', function () {
        let usuario = document.getElementById('usuario');
        usuario.value = 'adm';
        let senha = document.getElementById('senha');
        senha.value = 'adm';
    });

});