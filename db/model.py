import traceback
from math import ceil
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, MetaData, ForeignKey, DateTime, Index, Boolean, func, Table, \
    SmallInteger
from sqlalchemy import text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from engine_factory import EngineFactory
from word2vec import TextClassification

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

    @staticmethod
    def getNumOf(session):
        result = session.execute("SELECT count(wiki_pedia.id) FROM wiki_pedia").first()
        return result[0]

    @staticmethod
    def searchPageOf(session, page_size, page_index):
        result = session.query(Wikipedia).limit(page_size).offset((page_index) * page_size)
        return result

    @staticmethod
    def searchById(session, _id):
        result = session.query(Wikipedia).filter_by(id=_id).first()
        return result

    @staticmethod
    def searchByDocId(session, _doc_id):
        result = session.query(Wikipedia).filter_by(doc_id=_doc_id).first()
        return result

    @staticmethod
    def searchByTitle(session, _title):
        result = session.query(Wikipedia).filter_by(title=_title).first()
        return result

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return '<Wikipedia: %r: doc_id=%s >' % (self.title, self.doc_id)


if __name__ == "__main__":
    engine = EngineFactory.create_engine_to_wiki()
    # metadata = MetaData(bind=engine)
    session = EngineFactory.create_session(engine)
    # list = Wikipedia.searchPageOf(session,1000)
    totalnum = Wikipedia.getNumOf(session)
    print(totalnum)
    # get dictionary from docs
    dictionary = TextClassification.getDictionary([["computer", "science"]])
    for ii in range(0, ceil(totalnum / 1000)):
        doc_list = Wikipedia.searchPageOf(session, 1000, ii)
        print(type(doc_list))
        documents = []
        for doc in doc_list:
            documents = documents + TextClassification.divideIntoWords([doc.content])
        dic = TextClassification.getDictionary(documents)
        print(dic)
        dic_transfer = dictionary.merge_with(dic)
    dictionary.filter_extremes(no_below=5)
    dictionary.save("../model/dict")

    # translate the files to vecters and inform .data file for TF-IDF model
    '''
    vec = []
    for ii in range(0,ceil(totalnum/1000)):
        doc_list = Wikipedia.searchPageOf(session,1000,ii)
        print(type(doc_list))
        documents = []
        for doc in doc_list:
            documents = documents + TextClassification.divideIntoWords([doc.content])
        dic = TextClassification.getDictionary(documents)
        print(dic)
        dic_transfer = dictionary.merge_with(dic)
    dictionary.filter_extremes(no_below=5) 
    dictionary.save("../model/dict")
    '''

    # create the table
    '''
    Base.metadata.create_all(bind=engine)
    metadata = MetaData(bind=engine)
    '''