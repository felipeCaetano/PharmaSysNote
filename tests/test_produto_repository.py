import unittest
import sqlite3  # Substitua pelo seu módulo de conexão ao banco de dados
from backend.produto_dao import Produto, ProdutoRepository


class TestProduto(unittest.TestCase):
    def test_produto_creation(self):
        produto = Produto(
            codigo="123",
            name="Produto ABC",
            description="Descrição do produto",
            value=10.99,
            count=50,
            laboratorio="Laboratório XYZ",
            generico=False,
            lote="L123",
            validade="2023-12-31",
            presentation="Apresentação do produto",
        )

        self.assertEqual(produto.codigo, "123")
        self.assertEqual(produto.name, "Produto ABC")
        # Adicione mais asserções conforme necessário


class TestProdutoRepository(unittest.TestCase):
    def setUp(self):
        # Configurar um banco de dados de teste
        self.conn = sqlite3.connect(":memory:")
        self.produto_repository = ProdutoRepository(self.conn)

    def test_insert_and_get_produto(self):
        novo_produto = Produto(
            codigo="123",
            name="Produto ABC",
            description="Descrição do produto",
            value=10.99,
            count=50,
            laboratorio="Laboratório XYZ",
            generico=False,
            lote="L123",
            validade="2023-12-31",
            presentation="Apresentação do produto",
        )

        # Testar inserção
        self.produto_repository.insert_produto(novo_produto)

        # Testar busca
        resultados = self.produto_repository.get_produto_by_code_or_name("123")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0][1], "Produto ABC")
        # Adicione mais asserções conforme necessário

    def tearDown(self):
        # Fechar a conexão ao banco de dados de teste
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
