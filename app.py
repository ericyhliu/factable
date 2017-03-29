""""
    app.py

    Starts the Flask server.
"""

from flask import Flask, render_template, request
from factcheck import colors, parseArticle, analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    url = request.form['search']

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

        sentenceHighlights = ''

        for s in sentences:
            if s[1]:
                sentenceHighlights += '<span class="true">' + s[0] + ' </span>'
            else:
                sentenceHighlights += '<span class="false">' + s[0] + ' </span>'


        return render_template('search.html', verdict=verdict,
                                              verdictColor=verdictColor,
                                              confidence='{0:.2f}'.format(confidence),
                                              confidenceColor=confidenceColor,
                                              sentenceHighlights=sentenceHighlights)

if __name__ == "__main__":
    app.run(debug=True)
