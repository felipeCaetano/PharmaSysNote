from sqlalchemy import create_engine, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


class Base(DeclarativeBase):
    pass


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


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