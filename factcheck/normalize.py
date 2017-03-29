"""
    normalize.py

    Normalizes the true and false text dumps in
    the textDumps directory and normalizes them
    by converting them to respective text files
    that contain a sentence per line.
"""


from nltk.tokenize import sent_tokenize


trueTextDump = open('textDumps/true_text_dump.txt', 'r').read()
falseTextDump = open('textDumps/false_text_dump.txt', 'r').read()

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

print(len(trueSentences))
print(len(falseSentences))

try:
    trueTextFile = open('textNormalized/true.txt', 'w')

    for s in trueSentences:
        trueTextFile.write(s + '\n')

    trueTextFile.close()
except:
    print('[!] Error occurred writing to true.txt')

try:
    falseTextFile = open('textNormalized/false.txt', 'w')

    for s in falseSentences:
        falseTextFile.write(s + '\n')

    falseTextFile.close()
except:
    print('[!] Error occurred writing to false.txt')


