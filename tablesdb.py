import sqlite3

from sqlalchemy import create_engine, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


class Base(DeclarativeBase):
    pass


conn = sqlite3.connect("diversos/db/dbpharm.db", check_same_thread=False)


class Itens(Base):
    __tablename__ = "item_sales"
    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(String(20), nullable=False)
    name = mapped_column(String(30), nullable=False)
    count = mapped_column(Integer, nullable=False)
    presentation = mapped_column(String(15), nullable=False)
    value = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Item(id={self.id!r}, name={self.name!r}, count={self.count!r},"
            f"presentation{self.presentation}, value={self.value})"
        )


class User(Base):
    __tablename__ = "user_account"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False)
    fullname = mapped_column(String)
    addresses = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.metadata.create_all(engine)


def create_table():
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    presetation TEXT,
    count INTEGER,
    timestamp TEXT,
    value FLOAT)
    """
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS produtos (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       codigo TEXT,
       name TEXT,
       description TEXT,
       presetation TEXT,
       count INTEGER,
       laboratorio TEXT,
       generico TEXT,
       lote TEXT,
       validade TEXT,
       value FLOAT)
       """
    )

    # c.execute("""ALTER TABLE produtos ADD COLUMN description TEXT""")

    conn.commit()
