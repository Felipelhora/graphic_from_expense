from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graficos_despesas.config import DB_CONFIG
from graficos_despesas.data_base.db_base import Base


class DBConnectionHandler:
    """Sqlalchemy database connection"""

    def __init__(self) -> None:
        self.__connection_string = self._get_connection_string()
        self.session = None

    def __enter__(self):
        # Inicialização do objeto
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Limpeza do objeto
        pass
    
    def _get_connection_string(self) -> str:
        try:
            return "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                                        DB_CONFIG['db_username'], 
                                        DB_CONFIG['db_password'], 
                                        DB_CONFIG['db_host'], DB_CONFIG['db_port'], DB_CONFIG['db_name'])
        except:
            raise ValueError("Problemas na conexão")

    def get_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()