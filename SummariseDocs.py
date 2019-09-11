# -*- coding: utf-8 -*-
"""

@author: Jo
"""

##The TextRank method used here was adapted from:
#https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/

import pandas as pd
import numpy as np

import urllib
import bs4
from bs4 import BeautifulSoup
import re
import nltk

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx


import NewsFinder
from NewsFinder import NewsFinder


########################
# Get article text
########################


articleTextList = []

for articleURL in NewsFinder.urls:
    articlePage = urllib.request.urlopen(articleURL[1])
    articlesoup = BeautifulSoup(articlePage, 'html.parser')
    if articlesoup.find(attrs={'class':'content__article-body'}) is not None:
        articleText = articlesoup.find(attrs={'class':'content__article-body'}).text
    else:
        #Some articles are not articles but lists of events or other content. We are not
        #interested in those.
        articleText = ""
    articleTextList.append(articleText)

########################
# Clean the text
########################
    
for i in range(len(articleTextList)):
    articleTextList[i] = articleTextList[i].split("\n\n\nTopics")[0].strip()

sentencesList = []
for article in articleTextList:
    paragraphs = article.split("\n")
    sentences = [sen for paragraph in paragraphs for sen in sent_tokenize(paragraph)]
    sentencesList.append(sentences)
    

#Print small words that don't form part of the article, e.g. 'Facebook'. This is to understand
#any problems relating to them.
for article in sentencesList:
    for sentence in article:
        if len(sentence.split())>0 and len(sentence.split()) <3:
            print(sentence)
         
##Find text from links to other articles or social media within the main text. We will remove this.            
interruptions = [s for a in sentencesList for s in a if len(s.split()) <3 and len(s.split())>0]
setOfInterruptions = set([s.strip() for s in interruptions])

##There are sometimes links to other articles, e.g. above "Read more". However, these are related
#to the main article so need not be removed.

##Remove blank lines and interruptions. This will be our list of articles from which to extract
#summary sentences.
sentencesList = [[s.strip() for s in article if s.strip() not in [" ", ""] and s.strip() not in setOfInterruptions] for article in sentencesList]


#################################
# Process the text into vectors
#################################

##Load GloVe embeddings.
word_embeddings = {}
f = open('../GloVe/glove.6B/glove.6B.100d.txt', encoding='utf-8')

for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype = 'float32')  
    word_embeddings[word] = coefs
f.close()         

stopwords = stopwords.words('english')

##Remove very common words and punctuation.
def removeStopwordsPunctuation(sen):
    sen_lower = re.sub("[^a-zA-Z]", " ", sen).lower()
    sen_new = " ".join([i for i in sen_lower.split() if i not in stopwords])
    return(sen_new)

clean_sentences = [[removeStopwordsPunctuation(s) for s in article] for article in sentencesList]


########################
# TextRank Algorithm
########################

##Create separate similarity matrices for each article to rank the sentences per article.

##Create sentence vectors as the means of the word vectors of the words within the sentences.
def createSentenceVectors(article):
    sentence_vectors = []
    for sen in article:
        if len(sen) != 0:
            sen_v = sum([word_embeddings.get(w, np.zeros((100,))) for w in sen.split()])/(len(sen.split()) + 0.001)
        else:
            sen_v = np.zeros((100,))
        sentence_vectors.append(sen_v)
    return(sentence_vectors)

article_vectors = [createSentenceVectors(a) for a in clean_sentences]

##Create similarity matrices.
def createSimilarityMatrix(vectors):
    sim_mat = np.zeros([len(vectors), len(vectors)])
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            if i != j:
                sim_mat[i,j] = cosine_similarity(vectors[i].reshape(1,100), vectors[j].reshape(1,100))[0,0]        
    return(sim_mat)
    
articleMatrices = [createSimilarityMatrix(v) for v in article_vectors]

nx_graphs = [nx.from_numpy_array(sim_mat) for sim_mat in articleMatrices]

scores = [nx.pagerank(nx_graph) for nx_graph in nx_graphs]

##Sort sentences by second value in tuple.
def sortsens(sens):   
    sens.sort(key = lambda x: x[1], reverse = True)  
    return sens 

##Return the sentences to their original order after the top five have been selected.
def unsortsens(sens):   
    sens.sort(key = lambda x: x[0])  
    return sens   

#Create ranked lists of the sentences.
ranked_sentences = []
for i in range(len(sentencesList)):
    sentencelist = sentencesList[i]
    scorelist = scores[i]
    #ranked_sentences.append(sorted(((scorelist[j], s) for j, s in enumerate(sentencelist)), reverse = True))
    sortedsens = sortsens([(j, scorelist[j], s) for j, s in enumerate(sentencelist)])
    ranked_sentences.append(sortedsens)


########################
# Create Summaries
########################


TopFive = [rankedsens[0:5] for rankedsens in ranked_sentences]
TopFive = [unsortsens(rankedsens) for rankedsens in TopFive]

#Extract the sentences to form summaries.
Summaries = [[sen[2] for sen in sens] for sens in TopFive]

##Show summaries of all the articles.
for i in range(len(NewsFinder.headlines)):
    print(NewsFinder.headlines[i])
    print(Summaries[i])