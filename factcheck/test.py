"""
    test.py
"""

import nltk
import random
from nltk import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC


DEBUG = True


# Open text dumps
trueText = open('true.txt', 'r')
falseText = open('false.txt', 'r')

# Extract out sentence tokens from each text dump
trueSentences = []
falseSentences = []

for l in trueText:
    trueSentences.append(l)

for l in falseText:
    falseSentences.append(l)

if DEBUG:
    print(trueSentences)
    print(falseSentences)


# Create documents and word features, save to pickle
documents = []
wordFeatures = []
allowedWordTypes = ['ADJ', 'ADV', 'VERB', 'N', 'CONJ', 'NUM', 'DET']

for s in trueSentences:
    documents.append((s, True))
    words = word_tokenize(s)
    pos = nltk.pos_tag(words)

    for w in pos:
        if w[1][0] in allowedWordTypes:
            wordFeatures.append(w[0].lower())

for s in falseSentences:
    documents.append((s, False))
    words = word_tokenize(s)
    pos = nltk.pos_tag(words)

    for w in pos:
        if w[1][0] in allowedWordTypes:
            wordFeatures.append(w[0].lower())


wordFeatures = nltk.FreqDist(wordFeatures)
wordFeatures = list(wordFeatures.keys())[:10000]

if DEBUG:
    print(wordFeatures)

savedDocuments = open('saved_documents.pickle', 'wb')
pickle.dump(documents, savedDocuments)
savedDocuments.close()

savedWordFeatures = open('saved_word_features.pickle', 'wb')
pickle.dump(wordFeatures, savedWordFeatures)
savedWordFeatures.close()


def findFeatures(document):
    words = word_tokenize(document)
    features = {}

    for w in wordFeatures:
        features[w] = (w in words)

    return features


featureSets = []

for (s, c) in documents:
    featureSets.append((findFeatures(s), c))

savedFeatureSets = open('saved_feature_set.pickle', 'wb')
pickle.dump(featureSets, savedFeatureSets)
savedFeatureSets.close()


maxAvg = 0
maxMNB = 0
maxBNB = 0
maxLReg = 0
maxSGD = 0
maxLSVC = 0


while True:
    random.shuffle(featureSets)
    print(len(featureSets))


    # Training and Testing Set
    trainingSet = featureSets[:9740]
    testingSet = featureSets[9740:]


    # Multinomial Naive Bayes Classifier
    MultinomialNBClassifier = SklearnClassifier(MultinomialNB())
    MultinomialNBClassifier.train(trainingSet)

    # Bernoulli Naive Bayes Classifier
    BernoulliNBClassifier = SklearnClassifier(BernoulliNB())
    BernoulliNBClassifier.train(trainingSet)

    # Logistic Regression Classifier
    LogisticRegressionclassifier = SklearnClassifier(LogisticRegression())
    LogisticRegressionclassifier.train(trainingSet)

    # Stochastic Gradient Descent Classifier
    StochasticGradientDescentClassifier = SklearnClassifier(SGDClassifier())
    StochasticGradientDescentClassifier.train(trainingSet)

    # LinearSVC Classifier
    LinearSVCClassifier = SklearnClassifier(LinearSVC())
    LinearSVCClassifier.train(trainingSet)

    accuracyMNB = (nltk.classify.accuracy(MultinomialNBClassifier, testingSet)) * 100
    accuracyBNB = (nltk.classify.accuracy(BernoulliNBClassifier, testingSet)) * 100
    accuracyLReg = (nltk.classify.accuracy(LogisticRegressionclassifier, testingSet)) * 100
    accuracySGD = (nltk.classify.accuracy(StochasticGradientDescentClassifier, testingSet)) * 100
    accuracyLSVC = (nltk.classify.accuracy(LinearSVCClassifier, testingSet)) * 100

    avg = (accuracyMNB + accuracyBNB + accuracyLReg + accuracySGD + accuracyLSVC) / 5

    if avg > maxAvg:
        maxAvg = avg
        maxMNB = accuracyMNB
        maxBNB = accuracyBNB
        maxLReg = accuracyLReg
        maxSGD = accuracySGD
        maxLSVC = accuracyLSVC

        saveClassifier = open('mnb.pickle', 'wb')
        pickle.dump(MultinomialNBClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('bnb.pickle', 'wb')
        pickle.dump(BernoulliNBClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('lreg.pickle', 'wb')
        pickle.dump(LogisticRegressionclassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('sgd.pickle', 'wb')
        pickle.dump(StochasticGradientDescentClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('lsvc.pickle', 'wb')
        pickle.dump(LinearSVCClassifier, saveClassifier)
        saveClassifier.close()

    print('Average: ', avg)
    print('MNB: ', accuracyMNB)
    print('BNB: ', accuracyBNB)
    print('LReg: ', accuracyLReg)
    print('SGD: ', accuracySGD)
    print('LSVC: ', accuracyLSVC)
    print()

    print('Max Average: ', maxAvg)
    print('Max MNB: ', maxMNB)
    print('Max BNB: ', maxBNB)
    print('Max LReg: ', maxLReg)
    print('Max SGD: ', maxSGD)
    print('Max LSVC: ', maxLSVC)
    print()
