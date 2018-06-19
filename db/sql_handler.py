# _*_ coding: utf-8 _*_
import logging
import time
import traceback

from flask import request

from db.engine_factory import EngineFactory


class SQLHandler():
    def __init__(self, session=None):
        self.session = session

    def get_session(self):
        if not self.session:
            self.session = EngineFactory.create_session()

        return self.session

    def add_wikipedia(self, wiki_id, url, title, content):
        session = self.get_session()
        result = session.execute("SELECT * FROM wiki_pedia WHERE doc_id=:param", {"param": wiki_id}).first()
        if result is None:
            session.execute(
                "insert into wiki.wiki_pedia(wiki_pedia.doc_id,wiki_pedia.url,wiki_pedia.title,wiki_pedia.content) value(:param1,:param2,:param3,:param4)",
                {"param1": wiki_id, "param2": url, "param3": title, "param4": content})
            session.commit()
        return {'wiki_id': wiki_id}
