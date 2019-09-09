# NewsFinder
Tool to scrape the news.

## Aim

NewsFinder is a tool that scrapes the latest political articles in The Guardian* and provides easily accessed headlines, URLs, and short summaries of the articles. The idea originated with the recent surge in political news around Brexit with the aim to make it easier and more efficient to check for political updates (in terms of headlines and article summaries).

## Using the Tool

The tool is very straightforward. At the moment, run the code to generate the NewsFinder object. This object allows for the following commands:

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


*Other newspapers are available!
