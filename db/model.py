import traceback
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, MetaData, ForeignKey, DateTime, Index, Boolean, func, Table, \
    SmallInteger
from sqlalchemy import text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from engine_factory import EngineFactory

Base = declarative_base()


class Wikipedia(Base):
    __tablename__ = 'wiki_pedia'
    id = Column(Integer, primary_key=True)  # auto incrementing
    doc_id = Column(Integer, index=True, unique=True, nullable=False)
    url = Column(String(128), index=True, nullable=False)
    title = Column(String(64), index=True, nullable=False)
    content = Column(LONGTEXT())

    def __init__(self, doc_id=None, url=None, title=None, content=None):
        self.doc_id = doc_id
        self.url = url
        self.title = title
        self.content = content

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return '<Wikipedia: %r: doc_id=%s >' % (self.title, self.doc_id)


if __name__ == "__main__":
    engine = EngineFactory.create_engine_to_wiki()
    metadata = MetaData(bind=engine)
    # delete all table
    # Base.metadata.drop_all(bind=engine)

    # create the table
    Base.metadata.create_all(bind=engine)
