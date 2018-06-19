import MySQLdb
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
print metadata


class EngineFactory:
    @staticmethod
    def create_engine_to_wiki():
        engine = create_engine("mysql+pymysql://root:root@10.141.221.73/wiki?charset=utf8", encoding='utf-8',
                               echo=False)
        return engine

    @staticmethod
    def create_session(engine=None):
        if engine is None:
            engine = EngineFactory.create_engine_to_wiki()

        Session = sessionmaker(bind=engine, autocommit=False)
        session = Session()
        return session

