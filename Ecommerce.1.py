import mysql.connector

class Produto:
    def _init_(self, id_produtos, nome, preco, descricao, estoque):
        self.id_produtos = id_produtos
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.estoque = estoque

class Cliente:
    def _init_(self, id_cliente, nome, telefone):
        self.id_cliente = id_cliente
        self.nome = nome
        self.telefone = telefone

class Pedido:
    def _init_(self, id_pedidos, id_cliente, id_produtos, quantidade):
        self.id_pedidos = id_pedidos
        self.id_cliente = id_cliente
        self.id_produtos = id_produtos
        self.quantidade = quantidade

class SistemaDeEcommerce:
    def _init_(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="he182555@",
            database="ecommerce_db"
        )
        self.cursor = self.conexao.cursor()
        self.pedidos_realizados = []

    def adicionar_produto(self, produto):
        sql = (
            "INSERT INTO produtos (nome, preco, descricao, estoque) "
            "VALUES (%s, %s, %s, %s)"
        )
        valores = (produto.nome, produto.preco, produto.descricao, produto.estoque)
        self.cursor.execute(sql, valores)
        self.conexao.commit()
        print('Produto adicionado com sucesso')

    def listar_produtos(self):
        produtos = []
        self.cursor.execute("SELECT id_produtos, nome, preco, descricao, estoque FROM produtos")
        for (id_produtos, nome, preco, descricao, estoque) in self.cursor:
            produto = Produto(id_produtos, nome, preco, descricao, estoque)
            produtos.append(produto)
        return produtos

    def adicionar_cliente(self, cliente):
        sql = (
            "INSERT INTO clientes (nome, telefone) "
            "VALUES (%s, %s)"
        )
        valores = (cliente.nome, cliente.telefone)
        self.cursor.execute(sql, valores)
        self.conexao.commit()
        cliente_id = self.cursor.lastrowid
        cliente.id_cliente = cliente_id
        print('Cliente adicionado com sucesso.')

    def adicionar_pedido(self, id_cliente, id_produtos, quantidade):
        # Verifica se o produto existe
        self.cursor.execute(
            "SELECT id_produtos FROM produtos WHERE id_produtos = %s",
            (id_produtos,)
        )
        resultado_produto = self.cursor.fetchone()
        if not resultado_produto:
            print(f"Produto com ID {id_produtos} não encontrado. Não foi possível adicionar o pedido.")
            return

        # Insere o pedido
        sql = (
            "INSERT INTO pedidos (id_cliente, id_produtos, quantidade) "
            "VALUES (%s, %s, %s)"
        )
        valores = (id_cliente, id_produtos, quantidade)
        self.cursor.execute(sql, valores)
        self.conexao.commit()
        pedido_id = self.cursor.lastrowid
        pedido = Pedido(pedido_id, id_cliente, id_produtos, quantidade)
        self.pedidos_realizados.append(pedido)
        print('Pedido adicionado com sucesso.')

    def listar_pedidos(self):
        for pedido in self.pedidos_realizados:
            print(f"Pedido ID: {pedido.id_pedidos} - Cliente ID: {pedido.id_cliente} - Produto ID: {pedido.id_produtos} - Quantidade: {pedido.quantidade}")

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()

def coletar_dados_produto():
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    descricao = input("Digite a descrição do produto: ")
    estoque = int(input("Digite a quantidade em estoque do produto: "))
    return Produto(None, nome, preco, descricao, estoque)

def coletar_dados_cliente():
    nome = input("Digite o nome do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    return Cliente(None, nome, telefone)

def coletar_dados_pedido():
    id_cliente = int(input("Digite o ID do cliente: "))
    id_produto = int(input("Digite o ID do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    return id_cliente, id_produto, quantidade

if _name_ == "_main_":
    sistema = SistemaDeEcommerce()

    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Adicionar cliente")
        print("4. Realizar pedido")
        print("5. Listar pedidos realizados")
        print("6. Sair")
        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            produto = coletar_dados_produto()
            sistema.adicionar_produto(produto)
        elif opcao == "2":
            produtos = sistema.listar_produtos()
            for produto in produtos:
                print(f"ID: {produto.id_produtos} - Nome: {produto.nome} - Preço: R${produto.preco} - Estoque: {produto.estoque}")
        elif opcao == "3":
            cliente = coletar_dados_cliente()
            sistema.adicionar_cliente(cliente)
        elif opcao == "4":
            id_cliente, id_produto, quantidade = coletar_dados_pedido()
            sistema.adicionar_pedido(id_cliente, id_produto, quantidade)
        elif opcao == "5":
            print("\nPedidos Realizados:")
            sistema.listar_pedidos()
        elif opcao == "6":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    sistema.fechar_conexao()