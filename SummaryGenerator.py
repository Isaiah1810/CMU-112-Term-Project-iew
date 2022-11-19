import nltk
from nltk.tokenize import *
import string
fileName = open('givingTree.txt', encoding='utf8')
file = fileName.read()
text = file.lower()
result = ''
for c in text:
    if c == '\n':
        c = ' '
        result += ' '
    else:
        result += c
textWords = word_tokenize(result)
textSents = sent_tokenize(result)
def vectorizeSentance(set, L):
    result = dict()
    for elem in set:
        result[elem] = 0
    for elem in set:
        if elem in L:
            result[elem] += 1
    resultList = []
    for elem in result:
        resultList.append(result[elem])
    return resultList
def magnitude(L):
    sumL = 0
    for num in L:
        sumL += num**2
    return sumL**0.5
def dotProduct(L1, L2):
    product = 0
    for i in range(len(L1)):
        product += L1[i]*L2[i]
    return product
def compareSentances(L1, L2):
    wordsSet = set((L1 + L2))
    L1List = vectorizeSentance(wordsSet, L1)
    L2List = vectorizeSentance(wordsSet, L2)
    mag1 = magnitude(L1List)
    mag2 = magnitude(L2List)
    dProduct = dotProduct(L1List, L2List)
    return dProduct/(mag1*mag2)
similarityList = []
for i in range(len(textSents)):
    simSum = 0
    for j in range(len(textSents)):
        if i == j:
            continue
        else:
            simSum += compareSentances(textSents[i],textSents[j])/len(textSents)
    similarityList.append((textSents[i], simSum))
#From https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#mergesort 
def quickSort(L):
    if (len(L) < 2):
        return L
    else:
        first = L[0]  # pivot
        rest = L[1:]
        lo = [x for x in rest if x[1] < first[1]]
        hi = [x for x in rest if x[1] >= first[1]]
        return quickSort(lo) + [first] + quickSort(hi)
summaryList = quickSort(similarityList)
print(summaryList[-1:-5:-1])