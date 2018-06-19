import MySQLdb
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
print metadata


class EngineFactory:
    @staticmethod
    def create_engine_to_wiki():
        engine = create_engine("mysql+pymysql://root:root@10.141.221.73/wiki?charset=utf8", encoding='utf-8',
                               echo=True)
        return engine

    @staticmethod
    def create_session(engine=None):
        if engine is None:
            engine = EngineFactory.create_engine_to_wiki()

        Session = sessionmaker(bind=engine, autocommit=False)
        session = Session()
        return session


class ConnectionFactory:
    @staticmethod
    def create_cursor_for_jdk_importer():
        conn = MySQLdb.connect(
            host='10.141.221.73',
            port=3306,
            user='root',
            passwd='root',
            db='fdroid',
            charset="utf8"
        )
        cur = conn.cursor()
        return cur

    @staticmethod
    def create_cursor_by_knowledge_table(knowledge_table):
        conn = MySQLdb.connect(
            host=knowledge_table.ip,
            port=3306,
            user='root',
            passwd='root',
            db=knowledge_table.schema,
            charset="utf8"
        )
        cur = conn.cursor()
        return cur

    @staticmethod
    def create_cursor_for_android_importer():
        conn = MySQLdb.connect(
            host='10.141.221.75',
            port=3306,
            user='root',
            passwd='root',
            db='knowledgeGraph',
            charset="utf8"
        )
        cur = conn.cursor()
        return cur
