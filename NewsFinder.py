# -*- coding: utf-8 -*-
"""

@author: Jo
"""

import pandas as pd
import numpy as np

import urllib
import bs4
from bs4 import BeautifulSoup

##Function to get article subtitles and the first two paragraphs from the article page.
def getArticleSummaries(articleURL, subheadings, firstParagraphs):
        #print(articleURL)
        articlePage = urllib.request.urlopen(articleURL)
        articlesoup = BeautifulSoup(articlePage, 'html.parser')
        articleSubheading = articlesoup.find('div', attrs={'class': 'content__standfirst'}).text.strip()
        if articlesoup.find('div', attrs={'class': 'content__article-body'}) is not None:
            FirstParagraphs = articlesoup.find('div', attrs={'class': 'content__article-body'}).findAll('p')[0:2]
        else:
            FirstParagraphs = ""
        articleFirstParagraphs = ("\n".join([p.text for p in FirstParagraphs])).strip()
        subheadings.append(articleSubheading)
        firstParagraphs.append(articleFirstParagraphs)
        return()

##Create list of article information indexable by the number next to the headline.
def createArticleLookup(headlines, urls, subtitles, firstparagraphs):
    articleLookup = []
    for i in range(len(urls)):
        article_dict = {}
        article_dict["headline"] = headlines[i]
        article_dict["url"] = urls[i]
        article_dict["subtitle"] = subtitles[i]
        article_dict["first paragraphs"] = firstparagraphs[i]
            
        articleLookup.append(article_dict)
    return(articleLookup)
     
def num(itemList):
    numberedList = list(enumerate(itemList))
    return(numberedList)
        
class NewsFinderClass:
    def __init__(self, headlines, urls, subtitles, firstparagraphs, articlesummaries):
        self.headlines = num(headlines)
        self.urls = num(urls)
        self.subtitles = num(subtitles)
        self.firstparagraphs = num(firstparagraphs)
        self.articlesummaries = articlesummaries

def fetchHTML():    

    url = 'https://www.theguardian.com/politics'

    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')

    ##Get the main articles in the top section of the page.
    mainArticles = soup.find('div', attrs={'class': 'fc-container__body'})

    ##Get the links to articles.
    a = mainArticles.findAll('a', href = True)
    
    return(a)

##Combine the functions to create the NewsFinder object.
def getTheNews():
    
    a = fetchHTML()

    #Get the article headings and urls.
    #Avoid repetitions by only adding the headings and urls if the url isn't already
    #in the url list.
    articleHeadings = []
    urlList = []
    subheadings = []
    firstParagraphs = []


    for link in a:
        if link['href'] not in urlList:
            articleHeadings.append(link.text)
            urlList.append(link['href'])

    for myArticleURL in urlList:
        getArticleSummaries(myArticleURL, subheadings, firstParagraphs)
    
    articleSummaries = createArticleLookup(articleHeadings, urlList, subheadings, firstParagraphs)
    
    NewsFinderObject = NewsFinderClass(articleHeadings, urlList, subheadings, firstParagraphs, articleSummaries)

    return(NewsFinderObject)
    
NewsFinder = getTheNews()
