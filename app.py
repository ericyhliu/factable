""""
    Factable

    Submitted to MHacks 9.

    Uses natural language processing and machine
    learning to determine if a news article is
    real or fake news.

    Authors: Eric Liu (https://github.com/eliucs)
             Wes Ong (https://github.com/ongw)
             Jason Pham (https://github.com/suchaHassle)
"""

from pymongo import MongoClient
from flask import Flask, render_template, request
from factcheck import colors, parseArticle, analysis


app = Flask(__name__)

HOST = 'localhost'
PORT = 27017
client = MongoClient(HOST, PORT)
db = client.factable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    url = request.form['search']
    results = db.data.find_one({'url': url})

    if not results:
        article = parseArticle.getArticleContent(url)
        verdict, confidence, sentences = analysis.factAnalysis(article)

        if not sentences:
            return render_template('error.html')
        else:
            if not verdict:
                verdict = 'Fake'

            verdict = str(verdict)
            verdictColor = colors.verdictColor(verdict)
            confidenceColor = colors.confidenceColor(confidence)
            confidence *= 100
            confidence = '{0:.2f}'.format(confidence)
            sentenceHighlights = ''

            for s in sentences:
                if s[1]:
                    sentenceHighlights += '<span class="true">' + s[0] + ' </span>'
                else:
                    sentenceHighlights += '<span class="false">' + s[0] + ' </span>'

            # Save this data to the MongoDB database
            newCache = {'url': url,
                    'verdict': verdict,
                    'verdictColor': verdictColor,
                    'confidence': confidence,
                    'confidenceColor': confidenceColor,
                    'sentenceHighlights': sentenceHighlights}

            db.data.insert(newCache)

            return render_template('search.html',
                                   verdict=verdict,
                                   verdictColor=verdictColor,
                                   confidence=confidence,
                                   confidenceColor=confidenceColor,
                                   sentenceHighlights=sentenceHighlights)
    else:
        return render_template('search.html',
                               verdict=results['verdict'],
                               verdictColor=results['verdictColor'],
                               confidence=results['confidence'],
                               confidenceColor=results['confidenceColor'],
                               sentenceHighlights=results['sentenceHighlights'])

if __name__ == "__main__":
    app.run(debug=True)
