"""
    testurl.py

    Uses factcheck to test on a URL
    in the console.
"""


import requests
from bs4 import BeautifulSoup
from newspaper import Article
import factcheck
from django.core.exceptions import ValidationError
from django.forms import URLField


def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False
    return True

while (True):
    inp = input('Enter a link: ')

    if inp == 'q':
        exit()

    if validate_url(inp):
        try:
            article = Article(url=inp.strip(' '), language='en')
            article.download()
            article.parse()
            print(article.text)
            print(factcheck.factAnalysis(article.text))
        except Exception:
            article = ''
            r = requests.get(inp)
            soup = BeautifulSoup(r.text, "html.parser")
            for this_div in soup.find_all("p"):
                article += this_div.get_text()
            print(article)
            if not article:
                print('Invalid URL')
            else:
                print(factcheck.factAnalysis(article))
    else:
        print(factcheck.factAnalysis(inp))