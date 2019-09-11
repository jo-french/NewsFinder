# NewsFinder
Tool to scrape the news.

## Aim

NewsFinder is a tool that scrapes the latest political articles in The Guardian* and provides easily accessed headlines, URLs, and short summaries of the articles. The idea originated with the recent surge in political news around Brexit with the aim to make it easier and more efficient to check for political updates (in terms of headlines and article summaries).

## Summarise News Articles

Run the code SummariseDocs.py to generate summaries of the latest political news in the same order as the articles are listed in the NewsFinder object. This uses the TextRank algorithm (using nltk and networkx) individually on each article and produces 5 sentence summaries. At the time of writing, the mean article length was 20.14 sentences (to be very precise!) so this should reduce the time required to read the articles, or any selected article from the headlines list, to a quarter of the original time (should this be your aim).

## Using the Tool

The tool is very straightforward. At the moment, run the NewsFinder.py code to generate the NewsFinder object. Alternatively, running SummariseDocs.py will generate the newsfinder object in the process of generating article summaries. This object allows for the following commands:

```python
NewsFinder.headlines
```
lists the current headlines.

```python
NewsFinder.urls
```
gives the URLs of the articles.


```python
NewsFinder.subtitles
```
lists the article subtitles.


```python
NewsFinder.firstparagraphs
```
gives the first two paragraphs of the articles.


```python
NewsFinder.articlesummaries
```
summarises the information stored about the articles.

All but the article summaries are enumerated. Thus, for example, one can use `NewsFinder.headlines` to see the headlines of the latest articles, see that article 0 is interesting, and retrieve the information on article 0 using `NewsFinder.articlesummaries[0]`.

##SummariseDocs.py

The list of summaries is `Summaries`. It may be useful to print them all following the corresponding headlines or to print one using
```python
print(NewsFinder.headlines[i])
print(Summaries[i])
```


*Other newspapers are available!
