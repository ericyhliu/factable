"""
    parseArticle.py

    Uses the Newspaper API to efficiently retrieve
    article content, however if that does not work,
    manually overrides by using BeautifulSoup to
    parse out only p content.
"""


import requests
from bs4 import BeautifulSoup
from newspaper import Article


def getArticleContent(query):
    try:
        article = Article(url=query.strip(' '), language='en')
        article.download()
        article.parse()
        return article.text
    except Exception:
        article = ''
        r = requests.get(query)
        soup = BeautifulSoup(r.text, "html.parser")
        for this_div in soup.find_all("p"):
            article += this_div.get_text()
        return article
