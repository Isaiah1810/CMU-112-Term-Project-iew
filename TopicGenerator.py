import nltk
from nltk.tokenize import *
from nltk.corpus import stopwords
import string
fileName = open('speech_sounds.txt', encoding='utf8')
file = fileName.read()
text = file
result = ''
for c in text:
    if c == '\n':
        c = ' '
        result += ' '
    else:
        result += c
def removeStops(L):
    result = []
    for i in range(len(L)):
        if (L[i].lower() in stopwords.words('english') or L[i] in string.punctuation or
            L[i] == '\''):
            pass
        else:
            result.append(L[i])
    return result

textWords = word_tokenize(result)
textWords = removeStops(textWords)
tokenized = nltk.pos_tag(textWords)
def getProperList(L):
    properList = []
    for i in range(len(L)):
        if L[i][1] == 'NNP':
            properList.append(L[i][0])
    return properList

def getFrequencies(L):
    freqDict = dict()
    for item in L:
        freqDict[item] = 0
    for item in L:
        freqDict[item] += 1
    return freqDict
def sortFreqDict(d):
    dictList = list(d.items())
    dictList.sort(key=getScore)
    return dictList
def getScore(item):
    return item[1]
print(sortFreqDict(getFrequencies(tokenized)))

                