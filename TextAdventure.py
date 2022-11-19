import nltk
from nltk.tokenize import *
from nltk.corpus import stopwords
import string
import random
import sys
#THINGS TO DO-------------------------------------------------------------------
#ADD GRAMAR STRUCTURING
#ALLOW FOR UNKNOWN WORDS
fileName = open('paper.txt', encoding='utf8')
file = fileName.read()
text = file
result = ''
for c in text:
    if c == '\n':
        c = ' '
        result += ' '
    else:
        result += c.lower()
def removeStops(L):
    result = []
    for i in range(len(L)):
        if (L[i] in string.punctuation or L[i] == '\''):
            pass
        else:
            result.append(L[i])
    return result

textWords = word_tokenize(result)
textWords = removeStops(textWords)

def createLookupDict(words):
    lookupDict = dict()
    for i in range(len(words)):
         lookupDict[words[i]] = dict()
    for j in range(len(words)-1):
        if words[j+1] not in lookupDict[words[j]]:
            lookupDict[words[j]][words[j+1]] = 1
        else:
            lookupDict[words[j]][words[j+1]] += 1
    return lookupDict

def createBigramLookupDict(words):
    lookupDict = dict()
    for i in range(len(words)-1):
        lookupDict[words[i]+ ' '+words[i+1]] = dict()
    for j in range(len(words)-2):
        currentKey = words[j] + ' ' + words[j+1]
        if words[j+2] not in lookupDict[currentKey]:
            lookupDict[currentKey][words[j+2]] = 1
        else:
            lookupDict[currentKey][words[j+2]] += 1
    return lookupDict
#From https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
def merge(a, start1, start2, end):
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and (a[index1][1] > a[index2][1]))):
            aux[i] = a[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]
def mergeSort(a):
    n = len(a)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(a, start1, start2, end)
        step *= 2
#Takes in a dictionary in the lookupDictionary and returns the dict ordered
#by the second item in the tuples
def dictToOrderedList(d):
    dictList = []
    for key in d.keys():
        dictList.append((key, d[key]))
    mergeSort(dictList)    
    return dictList
#Takes in a string of word(s) and outputs the parts of speech that could come
#afterwords    
def nextPOS(word):
    posDict = dict()
    posList = ['CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
               'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
               'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
               'WDT', 'WP', 'WRB']
    pass
#Takes a single word and searches the bigramLookupDictionary and finds a bigram
#that includes the word. If nothings is found, returns none
def findBigram(bigramDict, word):
    bigramList = list(bigramDict.keys())
    for bigram in bigramList:
        if word in bigram:
            return bigram
    return None
#Takes in a unigramLookupDict, a starting word, and the number of words.
#handles cases of unknown words as well
def generateSentance(lookupDict, startingWord, n):
    if startingWord.lower() not in lookupDict:
        return None
    else:
        result = startingWord.lower() + ' '
        currentWord = startingWord.lower()
        for i in range(n):
            wordList = dictToOrderedList(lookupDict[currentWord])
            newWord = wordList[-1][0]
            result += newWord + ' '
            currentWord = newWord
    return result
#Takes in a bigramLookupDict, the unigramLookupDict, a starting word, and the 
#amount of words. Uses stupidbackoff and calls generate sentence if the word
#isn't a bigram 
def bigramGenerateSentance(lookupDict, unigramDict, startingWord, n):
    result = startingWord.lower() + ' '
    currentWord = startingWord.lower()
    for i in range(n):
        bigram = findBigram(lookupDict, currentWord)
        if bigram != None:
            currentWord = bigram
            wordList = dictToOrderedList(lookupDict[currentWord])
            newWord = wordList[-1][0]
            result += newWord + ' '
            for elem in lookupDict.keys():
                if newWord in elem:
                    currentWord = elem
                    break
        else:
            result += generateSentance(unigramDict, currentWord, 1) + ' '
    return result

bigramLookupDict = createBigramLookupDict(textWords)
lookupDict = createLookupDict(textWords)
print(bigramGenerateSentance(bigramLookupDict,lookupDict,
                             'misinformation', 15))
# print(generateSentance(lookupDict, 'misinformation', 5))
