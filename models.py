from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base() #clase base de la que se hereda las clases modelo


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)    #mapeado
    nombre = Column(String(50), nullable=False)     #mapeado
    email = Column(String(100), unique=True)       #mapeado
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan") # relacion cliente y pedido



class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    producto = Column(String(100))
    cantidad = Column(Integer)
    cliente = relationship("Cliente", back_populates="pedidos")