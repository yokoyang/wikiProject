# _*_ coding: utf-8 _*_
import logging
import time
import traceback

from flask import request

from db.engine_factory import EngineFactory

import re

emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


def remove_emoji(text):
    return emoji_pattern.sub(r'', text)


class test():
    def __init__(self):
        pass


class SQLHandler():
    def __init__(self, session=None, counter=0):
        self.session = session
        self.counter = counter

    def get_session(self):
        if not self.session:
            self.session = EngineFactory.create_session()

        return self.session

    def add_wikipedia(self, wiki_id, url, title, content):
        content = remove_emoji(content)
        session = self.get_session()
        result = session.execute("SELECT * FROM wiki_pedia WHERE doc_id=:param", {"param": wiki_id}).first()
        try:
            if result is None:
                session.execute(
                    "insert into wiki.wiki_pedia(wiki_pedia.doc_id,wiki_pedia.url,wiki_pedia.title,wiki_pedia.content) value(:param1,:param2,:param3,:param4)",
                    {"param1": wiki_id, "param2": url, "param3": title, "param4": content})
                self.counter += 1
                if self.counter % 500 == 0:
                    session.commit()
            return {'wiki_id': wiki_id}
        except Exception, error:
            print(error)
