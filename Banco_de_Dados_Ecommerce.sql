CREATE DATABASE ecommerce_db;
USE ecommerce_db;

CREATE TABLE produtos (
	id_produtos INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR (225)  NOT NULL,
    preco DECIMAL(10,2)  NOT NULL,
    descricao TEXT  NOT NULL,
    estoque INT NOT NULL
);

CREATE TABLE clientes (
id_cliente INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR (225)  NOT NULL,
telefone  VARCHAR (20)  NOT NULL
);

CREATE TABLE pedidos (
id_pedidos INT AUTO_INCREMENT PRIMARY KEY,
id_cliente INT  NOT NULL,
id_produtos INT  NOT NULL,
quantidade INT  NOT NULL,
FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
FOREIGN KEY (id_produtos) REFERENCES produtos(id_produtos)
);

