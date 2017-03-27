"""
    normalizeTextFiles.py

    Converts text dumps into text files containing
    individual sentences per line.
"""

from nltk.tokenize import sent_tokenize

trueTextDump = open('true_text_dump.txt', 'r').read()
falseTextDump = open('false_text_dump.txt', 'r').read()

trueSentences = []
falseSentences = []

for l in trueTextDump.split('\n'):
    sentences = sent_tokenize(l)

    for s in sentences:
        trueSentences.append(s)

for l in falseTextDump.split('\n'):
    sentences = sent_tokenize(l)

    for s in sentences:
        falseSentences.append(s)

print(trueSentences)
print(falseSentences)
print(len(trueSentences))
print(len(falseSentences))


try:
    print('[*] Writing to file true.txt')
    trueTextFile = open('true.txt', 'w')

    for s in trueSentences:
        trueTextFile.write(s + '\n')

    print('[*] Successfully wrote to text file.')
    trueTextFile.close()
except:
    print('[*] Error occurred writing to true.txt')

try:
    print('[*] Writing to file false.txt')
    falseTextFile = open('false.txt', 'w')

    for s in falseSentences:
        falseTextFile.write(s + '\n')

    print('[*] Successfully wrote to text file.')
    falseTextFile.close()
except:
    print('[*] Error occurred writing to false.txt')


