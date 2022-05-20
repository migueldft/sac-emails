#!/usr/bin/env python3

import os
import subprocess
import sys

import re
from unidecode import unidecode
import pandas as pd
import nltk

nltk.download('stopwords')
# nltk.download('rslp')

from sklearn.base import BaseEstimator, TransformerMixin

class NLTKPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    # Auxiliar functions
    def stopword_remover(self, text):
        remove_from_stopword_list = ['não', 'mais', 'foi', 'será', 'quando', 'tive', 'mas', 'até'] # são stopwords, mas contribuem para o sentido do texto
        add_to_stopword_list = ['pois']
        stop_words = nltk.corpus.stopwords.words('portuguese')
        stop_words.extend(add_to_stopword_list)
        for i in remove_from_stopword_list:
            stop_words.remove(i)
        words = [w for w in text.split() if not w in stop_words]
        text = ' '.join(words)
        return text 

    def useless_terms_remover(self, text):
        useless_terms = ['bom dia', 'boa tarde', 'boa noite', 'tudo bem', 'olá', 'td bem']
        for term in useless_terms:
            text = re.sub(term, '', text)
        return text

    def extra_subs(self, text):
        dictionary = {
            ' n ': ' não ',
            ' q ': ' que ', 
            'ngm': 'ninguém',
            'mto': 'muito',
            'vcs': 'vocês',
            'certinho': 'certo',
            ' pro ': ' para o ',
            ' mail ': ' email ',
            'emails': 'email',
            'markt': 'market',
            'nesse site': 'dafiti',
            'nessa loja': 'dafiti',
            'informar que': 'dizer que',
            'https www reclameaqui br': 'reclame aqui',
            'vcs': 'voces',
            ' pra ': ' para ',
            'mercadoria': 'pedido',
            'mais deu': 'mas deu',
            'saber do': 'saber sobre',
            'empresa ': 'dafiti ',
            ' ver comentarios': ' ler comentarios',
            'produto': 'pedido',
            ' compra ': ' pedido ',
            'fazer compra': 'fazer pedido',
            'mudar': 'trocar',
            'receber': 'chegar',
            'entregar': 'chegar',          
            'até hoje': 'até agora',
            'mandar': 'enviar',
            'obg': 'obrigado',
            'obrigada': 'obrigado'
        }
        for key in dictionary.keys():
            text = text.replace(key, dictionary[key])
        return text

    def transform(self, X):
        # text cleaning
        X = X.apply(str.lower)
        X = X.apply(self.stopword_remover)
        X = X.str.replace(r' +', ' ', regex=True)
        X = X.str.replace(r'\n', ' ', regex=True)
        X = X.str.replace(r'\t', ' ', regex=True)
        X = X.str.replace('r$', '', regex=False)
        X = X.str.replace(r'[^a-zÀ-ÿ ]+', '', regex=True)
        X = X.apply(self.useless_terms_remover)
        X = X.apply(self.extra_subs)

        # # lema
        # subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'pt_core_news_md'])
        # nlp = spacy.load('pt_core_news_md')
        # nlp.max_length = 5000000
        # docs = X.to_list()
        # lemmatized_docs = []
        # print('Starting Lemma')
        # for doc in nlp.pipe(docs, batch_size=8, n_process=8, disable=["parser", "ner"]):
        #     sentece = []
        #     for word in doc:
        #         if ((word.pos_ == 'VERB') or (word.pos_ == 'ADJ')):
        #             sentece.append(word.lemma_) # lemma
        #         else:
        #             sentece.append(word.orth_) # original
        #     sent = ' '.join(sentece)    
        #     lemmatized_docs.append(sent)
        # X = pd.Series(lemmatized_docs)

        X = X.apply(unidecode)

        # # Stemming
        # print('Starting Stemming')
        # stemmer = nltk.stem.RSLPStemmer()
        # stemmed_docs = []
        # for sentence in lemmatized_docs:
        #     new_sentence = []
        #     for word in sentence.split():
        #         new_sentence.append(stemmer.stem(word))
        #     stemmed_docs.append(' '.join(new_sentence))

        # X = pd.Series(stemmed_docs) # back to series

        return X