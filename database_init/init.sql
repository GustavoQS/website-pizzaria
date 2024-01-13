CREATE DATABASE pizzaria_database;
USE pizzaria_database;
CREATE TABLE cardapio (
	id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(50),
    nome VARCHAR(100),
    descricao VARCHAR(255),
    img VARCHAR(255),
    preco DECIMAL(6, 2), 
    habilitado TINYINT DEFAULT 1,
    INDEX (id)
);
CREATE TABLE pedidos (
	pedidoId VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(50),
    tel VARCHAR(15),
    cep VARCHAR(15),
    rua VARCHAR(50),
    num VARCHAR(10),
    obsEnd VARCHAR(255),
    valorT DECIMAL(6, 2),
    pagamento VARCHAR(25),
    dataHora DATETIME,
    preparado TINYINT DEFAULT 0,
    entregue TINYINT DEFAULT 0,
    cancelado TINYINT DEFAULT 0,
    INDEX (pedidoId)
);
CREATE TABLE itensPedidos (
	pedidoId VARCHAR(255),
    itemId INT,
    qnt INT,
    valor DECIMAL(6, 2),
    obsItem VARCHAR(255),
    FOREIGN KEY (itemId) REFERENCES cardapio(id),
    FOREIGN KEY (pedidoId) REFERENCES pedidos(pedidoId),
    INDEX (pedidoId)
);
CREATE TABLE funcionarios (
	id INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(25),
    senha VARCHAR(255),
    ultimoAcesso DATETIME,
    nivel INT DEFAULT 0
);
INSERT INTO funcionarios (usuario, senha, nivel) VALUES ('adm', 'scrypt:32768:8:1$UanzztExrryQNy9C$4547ef209445dd158a819740d7b1b603feb8c7ff5b871d37862fd50b8e0069c8aaacbf2ba7cd5246e60ff07affa52095470dccf0cde3e38027a812e300f390ff', 10);
