import datetime

from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, \
    DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    value = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    laboratorio = Column(String)
    generico = Column(Boolean, nullable=False)
    lote = Column(String)
    validade = Column(DateTime)
    presentation = Column(String)


class ProdutoRepository:
    def __init__(self, engine):
        self.engine = engine

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_produto(self, produto):
        try:
            self.session.add(produto)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_produto_by_code_or_name(self, search_value):
        return self.session.query(Produto).filter(
            (Produto.codigo == search_value) | (Produto.name == search_value)
        ).all()


if __name__ == '__main__':
    # Exemplo de utilização
    engine = create_engine('sqlite:///:memory:')
    produto_repository = ProdutoRepository(engine)

    novo_produto = Produto(
        codigo="123",
        name="Produto ABC",
        description="Descrição do produto",
        value=10.99,
        count=50,
        laboratorio="Laboratório XYZ",
        generico=False,
        lote="L123",
        validade=datetime.datetime(2023, 12, 31),
        presentation="Apresentação do produto",
    )

    produto_repository.insert_produto(novo_produto)

    resultados = produto_repository.get_produto_by_code_or_name("123")
    print(resultados)
