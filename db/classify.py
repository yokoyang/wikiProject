#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 此文件仅提供text进行基于word2vec的特征抽取的类，并且提供NLP相关的处理办法

import gensim
import logging
import os
from collections import defaultdict
import sys
import re
from scipy import sparse
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt

month = {'January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augest', 'September', 'October', 'November',
         'December',
         'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'June.', 'July.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'}
week = {'Monday', "Tuesday", "Wednesday", 'Thursday', 'Friday', 'Saturday', 'Sunday',
        'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'}


class TextClassification(object):
    document = []

    def __init__(self, rootdir=None):
        # start logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        # read all files in the root dir
        r = os.walk(rootdir)
        for parent, dirnames, filenames in r:
            for filename in filenames:
                fullpath = os.path.join(parent, filename)
                with open(fullpath, "r", encoding='UTF-8', errors="ignore") as f:
                    self.document.append(f.read())

    @staticmethod
    def divideIntoWords(documents):
        '''
        Preprocessing
        @paragraph:document = [text1,...]
        cut the documents into words
        cut the paragraph into sentence,and then cut the sentence into words, after that, delete words in stop list
        use "NUM" replace all the numbersand use "DATE" replace all the date
        '''
        texts = []
        stoplist = set('for a of the and to in the'.split())
        for doc in documents:
            new_doc = []
            paragraphs = doc.split("\n| ")
            for p in paragraphs:
                sentences = re.split("[#，。‘’·`“”》《；：…&-——_$.!?:\"<>,\'\t|()-+*/%]", p)
                for s in sentences:
                    words = s.split()
                    for w in words:
                        if w.isdigit():
                            new_doc.append("NUM")
                        elif w in month or w in week:
                            new_doc.append("DATE")
                        elif w in stoplist:
                            continue
                        else:
                            new_doc.append(w.lower())
            texts.append(new_doc)
        '''
        #delete the words which appear only once
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1] for text in texts]
        '''
        return texts

    @staticmethod
    def getDictionary(texts):
        # return a dictionary, this class is imported from gensim, we can use .token2id get some informations likes[{"keyword":ID},...]
        return gensim.corpora.Dictionary(texts)

    @staticmethod
    def TF_IDF(dictionary, text):
        # transfer text to vectors, the result has format likes [(ID,appear_times),...]
        return dictionary.doc2bow(text.lower().split())

    '''
    def trainModel(self,doc):
        #train model for classcifying
        #input: different doc [...]

    '''

    def sparse2mar(s, l):
        m = []
        j = 0
        i = 0
        for i in range(0, len(s)):
            while j < s[i][0]:
                m.append(0)
                j += 1
            m.append(s[i][1])
            i += 1
        while i < l:
            m.append(0)
            i += 1
        return m


'''		
if __name__ == "__main__":
	traindata = "../data"
	model = TextClassification(traindata)
	#print(model.document)
	texts = model.deleteStoplist(model.document)
	dic = model.getDictionary(texts)
	dic.save("../model/dict")
	print(type(dic))
	corpus_list = [dic.doc2bow(text) for text in texts]
	#print(corpus_list)
	gensim.corpora.MmCorpus.serialize('../model/corpuse.mm', corpus_list)
	corpus_tfidf = []
	tfidfModel = gensim.models.TfidfModel(corpus=corpus_list, id2word={}, dictionary=dic)
	tfidfModel.save("../model/tfidf.model")
	corpus_tfidf = tfidfModel[corpus_list]
	dia = len(tfidfModel.idfs)
	m = []
	for item in corpus_list:
		m.append(sparse2mar(item,dia))
	#print(m)
	corpus_tfidf.save("../model/data.tfidf") 
	tfidf = gensim.models.TfidfModel.load("../model/data.tfidf") 
	#print(tfidfModel.dfs) 
	#print(tfidfModel.idfs)
'''

