"""
    generate.py

    From the normalized text files true.txt and false.txt,
    this module builds up the feature set by taking the
    most frequent 10,000 words in the true and false datasets
    filtered by only considering adjectives, adverbs,
    verbs, nouns, conjunctions, numerals and determinants,
    and then trains the five classifiers used: Multinomial
    Naive Bayes, Bernoulli Naive Bayes, Logistic Regression,
    Stochastic Gradient Descent and Linear Support Vector
    Machine.
"""


import nltk
import pickle
import random
from nltk import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC


# Open the normalized true and false datasets
# and append each line to the trueSentences and
# falseSentences lists.
trueSentences = []
falseSentences = []

try:
    trueText = open('textNormalized/true.txt', 'r')
    falseText = open('textNormalized/false.txt', 'r')

    for line in trueText:
        trueSentences.append(line)

    for line in falseText:
        falseSentences.append(line)
except Exception as e:
    print('[!] Error occurred when reading from text files.')


# Label each sentence in each of trueSentences and
# falseSentences as True or False respectively
# in a tuple, then append to documents. Tokenize
# words in each sentence and only add unique, allowed
# word types into wordFeatures.
documents = []
wordFeatures = []
allowedWordTypes = ['ADJ', 'ADV', 'VERB', 'N',
                    'CONJ', 'NUM', 'DET']

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


# Feature sets are built up by iterating through
# each element in documents and checking if the
# sentence contains words that are contained in
# wordFeatures
featureSets = []
for (s, c) in documents:
    featureSets.append((findFeatures(s), c))

savedFeatureSets = open('saved_feature_set.pickle', 'wb')
pickle.dump(featureSets, savedFeatureSets)
savedFeatureSets.close()


# Trains each of the five classifiers up to 50 times
# after randomly shuffling the feature sets, takes
# the best accuracy result recorded, and saves
# classifiers to .pickle files
maxAvg = 0
maxMNB = 0
maxBNB = 0
maxLReg = 0
maxSGD = 0
maxLSVC = 0

for i in range(50):
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

    average = (accuracyMNB + accuracyBNB + accuracyLReg + accuracySGD + accuracyLSVC) / 5

    if average > maxAvg:
        maxAvg = average
        maxMNB = accuracyMNB
        maxBNB = accuracyBNB
        maxLReg = accuracyLReg
        maxSGD = accuracySGD
        maxLSVC = accuracyLSVC

        saveClassifier = open('trainedClassifiers/mnb.pickle', 'wb')
        pickle.dump(MultinomialNBClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('trainedClassifiers/bnb.pickle', 'wb')
        pickle.dump(BernoulliNBClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('trainedClassifiers/lreg.pickle', 'wb')
        pickle.dump(LogisticRegressionclassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('trainedClassifiers/sgd.pickle', 'wb')
        pickle.dump(StochasticGradientDescentClassifier, saveClassifier)
        saveClassifier.close()

        saveClassifier = open('trainedClassifiers/lsvc.pickle', 'wb')
        pickle.dump(LinearSVCClassifier, saveClassifier)
        saveClassifier.close()

    print('Average: ', average)
    print('MNB: ', accuracyMNB)
    print('BNB: ', accuracyBNB)
    print('LReg: ', accuracyLReg)
    print('SGD: ', accuracySGD)
    print('LSVC: ', accuracyLSVC, '\n')
    print('Max Average: ', maxAvg)
    print('Max MNB: ', maxMNB)
    print('Max BNB: ', maxBNB)
    print('Max LReg: ', maxLReg)
    print('Max SGD: ', maxSGD)
    print('Max LSVC: ', maxLSVC, '\n')
