# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class Database:
    def __init__(self):
        # Ajusta la URL según tu base de datos
        self.engine = create_engine('mysql+pymysql://root:@localhost/ORMDb')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine) #creacion de una sesion de trabajo
        self.session = Session()