"""
    colors.py

    Determines the color to be rendered
    in the web application.
"""


def verdictColor(x):
    if x == 'True':
        return 'color: #008000;'
    return 'color: #FF0000;'


def confidenceColor(x):
    if x > 0.9:
        return 'color: #008000;'
    elif x > 0.8:
        return 'color: #198c19;'
    elif x > 0.7:
        return 'color: #329932;'
    elif x > 0.6:
        return 'color: #4ca64c;'
    elif x > 0.5:
        return 'color: #66b266;'
    elif x > 0.4:
        return 'color: #ff0000;'
    elif x > 0.3:
        return 'color: #e50000;'
    elif x > 0.2:
        return 'color: #cc0000;'
    elif x > 0.1:
        return 'color: #b20000;'
    else:
        return 'color: #990000;'


def sentenceColor(x):
    if x:
        return 'color: #008000;'
    return 'color: #FF0000;'
