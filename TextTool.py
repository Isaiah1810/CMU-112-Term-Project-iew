from cmu_112_graphics import *
import nltk
from nltk import pos_tag
from nltk.tokenize import *
from nltk.corpus import stopwords
import string
import random
buttonList = []
################################################################################
#
#                               Screen Classes
#
################################################################################
class AppMode:
    def __init__(self):
        pass
#Defines the title screen class. Includes Buttons to go to the other screen
class TitleScreen(AppMode):
    def __init__(self, app):
        self.app = app
        self.topicButton = Button(app.width//6, 5*app.height//6, app.width//7, 
                                  app.height//8, 'Topic Generator', 
                                  self.toTopicGenerator)
        self.summaryButton = Button(3*app.width//6, 5*app.height//6, 
                                    app.width//7, app.height//8, 
                                   'Summary Generator', self.toSummaryGenerator)
        self.textAdventureButton = Button(5*app.width//6, 5*app.height//6, 
                                          app.width//7, app.height//8, 
                                         'Text Generator', self.toTextAdventure)
        self.importButton = Button(3*app.width//6, 4*app.height//6, 
                                   app.width//7, app.height//8, 'Import Text', 
                                   self.importText)
        self.buttons = [self.topicButton, self.summaryButton, 
                        self.textAdventureButton, self.importButton]
        self.importPopup = False
        # self.text = open('Frankenstein.txt', encoding='utf8')
#Button Functions###############################################################
    def toTopicGenerator(self, app):
        if app.text != None:
            changeScreen(app, TopicScreen(app))
        else:
            self.importPopup = True
    def toSummaryGenerator(self, app):
        if app.text != None:    
            changeScreen(app, SummaryScreen(app))
        else:
            self.importPopup = True
    def toTextAdventure(self, app):
        if app.text != None:
            changeScreen(app, TextAdventure(app))
        else:
            self.importPopup = True
    def importText(self, app):
        changeScreen(app, ImportScreen(app))
#Drawing function for class#####################################################    
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height, fill='#FFCCCB')
        self.topicButton.draw(app, canvas)
        self.summaryButton.draw(app, canvas)
        self.textAdventureButton.draw(app, canvas)
        self.importButton.draw(app, canvas)
        if self.importPopup:
            canvas.create_text(app.width//2, app.height//2, text='Please import a file!', font='Roboto 20 bold')
        canvas.create_text(app.width//2, app.height//6, text="Welcome to Terrific Text Tool (1)Twelve!", font = 'Times 30 bold')
        canvas.create_text(app.width//2, app.height//3, text=f'Imported file is: {app.textFileName}', font='Roboto 20')
#All subscreens include back buttons
#Defines the Topic Generator Screen Class
class TopicScreen(AppMode):
    def __init__(self, app):
        print('Initializing Topic Screen...')
        self.app = app
        self.text = self.cleanText(app.text)
        self.taggedText = nltk.pos_tag(self.text)
        self.freqDict = self.getFrequencies(self.taggedText)
        self.nounList, self.nounFreqs  = self.getNounList(self.freqDict)
        self.backButton = Button(5*app.width//6, 4*app.height//6, 
                                          app.width//7, app.height//8, 
                                          'Back', self.toTitleScreen)
        self.nounButton = Button(app.width//6, 7*app.height//8, app.width//7,
                                 app.height//8, 'Nouns', self.nounFilter)
        self.verbButton = Button(2*app.width//6, 7*app.height//8,
                                 app.width//7, app.height//8, 'Verbs', self.verbFilter)
        self.adjButton = Button(3*app.width//6, 7*app.height//8, app.width//7, 
                                app.height//8, 'Adjectives', self.adjFilter)
        self.advButton = Button(4*app.width//6, 7*app.height//8, app.width//7,
                                app.height//8, 'Adverbs', self.advFilter)
        self.clearFilterButton = Button(5*app.width//6, 7*app.height//8,
                                        app.width//7, app.height//8, 'Clear Filter',
                                        self.clearWordFilter)
        self.graphScreenButton = Button(app.width//2, 4*app.height//6, 
                                        app.width//7, app.height//8, 'Graph', self.toGraphScreen)
        self.buttons = [self.backButton, self.nounButton, self.verbButton, 
                        self.adjButton, self.advButton, self.clearFilterButton,
                        self.graphScreenButton]
        self.wordList = self.getWordList(self.freqDict)
        self.topicWords = self.getTopWords(self.wordList)
        self.topicNouns = self.getTopWords(self.nounList)
        self.verbList, self.verbFreqs = self.getVerbList(self.freqDict)
        self.topicVerbs = self.getTopWords(self.verbList)
        self.adjList, self.adjFreqs = self.getAdjList(self.freqDict)
        self.topicAdjs = self.getTopWords(self.adjList)
        self.advList, self.advFreqs = self.getAdvList(self.freqDict)
        self.topicAdvs = self.getTopWords(self.advList)
        self.currentWords = self.topicWords
        self.currentList = self.freqDict
#Removes extra unwanted newline charcters     
    def cleanText(self, text):
        result = ''
        for c in text:
            if c == '\n':
                # c = ' '
                result += ' '
            else:
                result += c
        return self.removeStops(word_tokenize(result))
#Removes stop words from text(ie common words like 'and, or but' etc.)
    def removeStops(self, text):
        result = []
        for i in range(len(text)):
            if (text[i].lower() in stopwords.words('english') or text[i] in 
                string.punctuation or not text[i].isalnum()):
                pass
            else:
                result.append(text[i])
        return result
#Takes in a list of words and outputs a list of tuples of words with the values 
#being each word's frequencies
    def getFrequencies(self, L):
        freqDict = dict()
        for item in L:
            freqDict[item] = 0
        for item in L:
            freqDict[item] += 1
        dictList = list(freqDict.items())
        dictList.sort(key=self.getScore)
        return dictList
#Key function for sorting function above
    def getScore(self, item):
        return item[1]
#Takes in the freqency List and Outputs a Sorted List of just the words
    def getWordList(self, L):
        wordList = []
        for i in range(len(L)):
            wordList.append(L[i][0][0])
        return wordList
#Takes in a freq list. Returns the list of nouns and a frequency list of nouns.
    def getNounList(self, L):
        nounSet = set()
        nounSet.add('NN')
        nounSet.add('NNP')
        nounSet.add('NNS')
        properList = []
        nounList = []
        for i in range(len(L)):
            if L[i][0][1] in nounSet:
                properList.append(L[i][0][0])
                nounList.append((L[i][0], L[i][1]))
        return properList, nounList
#Takes in a frequency list, and outputs a list of adjectives, and a frequency 
#list of just adjectives
    def getAdjList(self, L):
        adjSet = set()
        adjSet.add('JJ')
        adjSet.add('JJR')
        adjSet.add('JJS')
        adjList = []
        adjFreqs = []
        for i in range(len(L)):
            if L[i][0][1] in adjSet:
                adjList.append(L[i][0][0])
                adjFreqs.append((L[i][0], L[i][1]))
        return adjList, adjFreqs
#Takes in a frequency list, and outputs a list of adverbs, and a frequency 
#list of just adverbs
    def getAdvList(self, L):
        advSet = set()
        advSet.add('RB')
        advSet.add('RBR')
        advSet.add('RBS')
        advList = []
        advFreqs = []
        for i in range(len(L)):
            if L[i][0][1] in advSet:
                advList.append(L[i][0][0])
                advFreqs.append((L[i][0], L[i][1]))
        return advList, advFreqs
#Takes in the frequency list, and returns a list of all the verbs, and a freq
#list of all the verbs
    def getVerbList(self, L):
        verbList = []
        verbSet = set()
        verbSet.add('VBD')
        verbSet.add('VB')
        verbSet.add('VBG')
        verbSet.add('VBN')
        verbSet.add('VBP')
        verbSet.add('VBZ')
        verbFreqs = []
        for i in range(len(L)):
            if L[i][0][1] in verbSet:
                verbList.append(L[i][0][0])
                verbFreqs.append((L[i][0], L[i][1]))
        return verbList, verbFreqs
#Takes in a frequency-ordered list of words, returns the most frequent words
    def getTopWords(self, L):
        if len(L) >= 10:
            s = ''
            for item in L[-1:-10:-1]:
                s += item +','+' '
            return s
        else:
            s = ''
            for item in L[0:len(L)]:
                s += item +','+' '
            return s
#Button Function################################################################
    def toTitleScreen(self, app):
        changeScreen(app, TitleScreen(app))
    def toGraphScreen(self, app):
        app.currentScreen = GraphScreen(app, self.currentList)
    def clearWordFilter(self, app):
        self.currentWords = self.topicWords
        self.currentList = self.freqDict
    def nounFilter(self, app):
        self.currentWords = self.topicNouns
        self.currentList = self.nounFreqs
    def verbFilter(self, app):
        self.currentWords = self.topicVerbs
        self.currentList = self.verbFreqs
    def adjFilter(self, app):
        self.currentWords = self.topicAdjs
        self.currentList = self.adjFreqs
    def advFilter(self, app):
        self.currentWords = self.topicAdvs
        self.currentList = self.advFreqs
#Draw Function##################################################################
    def drawButtons(self, app, canvas):
        for button in self.buttons:
            button.draw(app, canvas)
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0,app.width, app.height, fill='cyan')
        self.drawButtons(app, canvas)
        canvas.create_text(app.width//2, app.height//8, 
                           text='Your Top Words Are:', font='Roboto 30')
        canvas.create_text(app.width//2, app.height//4, text=self.currentWords,
                           font='Roboto 24')           


class GraphScreen():
    def __init__(self, app, data):
        self.data = data
        self.backButton = Button(5*app.width//6, 4*app.height//6, 
                                                app.width//7, app.height//8, 
                                                'Back', self.toTopicScreen)
        self.buttons = [self.backButton]
        self.numDataPoints = 10
        self.xData = data[-1:-self.numDataPoints-1: -1]
        self.graph = Graph(app.width//3, 2*app.height//5, app.width//2, 
                           app.height//2)
        self.graph.setXData(self.xData)
        if len(data) < 10:
            sliderMax = len(data)
        else:
            sliderMax = 10
        self.redSlider = Slider(5*app.width//6, 1*app.height//16, app.width//6, 0, 255)
        self.redSlider.color = 'red'
        self.greenSlider = Slider(5*app.width//6, 2*app.height//16, app.width//6, 0, 255)
        self.greenSlider.color = 'green'
        self.blueSlider = Slider(5*app.width//6, 3*app.height//16, app.width//6, 0, 255)
        self.blueSlider.color = 'blue'
        self.dataSlider = Slider(app.width//2, 7*app.height//8, app.width//3, 1, sliderMax)
        self.sliders = [self.dataSlider, self.redSlider, self.greenSlider,
                        self.blueSlider]
        self.red = 0
        self.green = 0
        self.blue = 0
    def updateSliders(self):
        self.updateDataPoints()
        self.updateColorSliders()
    def updateDataPoints(self):
        if self.dataSlider.currentVal < 1:
            self.dataSlider.currentVal = 2
        if self.data[-1:-self.dataSlider.currentVal:-1] == []:
            return
        self.xData = self.data[-1:-self.dataSlider.currentVal:-1]
        self.graph.xData = self.xData
    def updateColorSliders(self):
        self.red = self.redSlider.currentVal
        self.green = self.greenSlider.currentVal
        self.blue = self.blueSlider.currentVal
#Hex Color Conversion from https://www.cs.cmu.edu/~112/notes/notes-graphics.html 
        self.graph.setColor(f'#{self.red:02x}{self.green:02x}{self.blue:02x}')
    def toTopicScreen(self, app):
        changeScreen(app, TopicScreen(app))
    def drawButtons(self, app, canvas):
        for button in self.buttons:
            button.draw(app, canvas)
    def drawSliders(self, app, canvas):
        for slider in self.sliders:
            slider.draw(app, canvas)
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0,app.width, app.height, fill='cyan')
        canvas.create_text(app.width//2, 10*app.height//13, text='Data Points Slider',
                           font='Roboto 20')
        self.drawButtons(app, canvas)
        self.drawButtons(app, canvas)
        self.graph.draw(app, canvas)
        self.drawSliders(app, canvas)

#Defines the Summary Screen Class
class SummaryScreen(AppMode):
    def __init__(self, app):
        self.app = app
        print('Initializing Summary Screen')
        self.backButton = Button(5*app.width//6, 4*app.height//6, 
                                                app.width//7, app.height//8, 
                                                'Back', self.toTitleScreen)
        self.buttons = [self.backButton]
        self.sents = self.cleanText(app.text)
        self.simList = self.getSimList(self.sents)
        self.numSumSents = 10
        self.sumList = self.simList[-1:-self.numSumSents:-1]
        self.summary = self.getSummary(self.sumList)
        self.slider = Slider(app.width//2, 5*app.height//6, app.width//3, 2, 11)
        self.slider.currentVal = 2
        # print(self.summary)
#Removes unwanted newline characters from text and returns a list of sentances
    def cleanText(self, text):
        result = ''
        for c in text:
            if c == '\n':
                c = ' '
                result += ' '
            else:
                result += c
        return sent_tokenize(result)
#Takes in a set containing the shared words of two different sentances, and also
#takes in one of those two sentances. Returns a list with same len as set of 
#the frequency of each word of the set in the sentance
    def vectorizeSentance(self, set, L):
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
#Takes in a list(representing a vector) and finds the magnitude of the set
    def magnitude(self, L):
        sumL = 0
        for num in L:
            sumL += num**2
        return sumL**0.5
#Takes in two lists(vectors) and returns the dot product of the two sets
    def dotProduct(self, L1, L2):
        product = 0
        for i in range(len(L1)):
            product += L1[i]*L2[i]
        return product
#Takes in two sentances, vectorizes both sentances using their shared set, 
#and uses a cosine similarity formula to calculate relation with each other
    def compareSentances(self, L1, L2):
        wordsSet = set((L1 + L2))
        L1List = self.vectorizeSentance(wordsSet, L1)
        L2List = self.vectorizeSentance(wordsSet, L2)
        mag1 = self.magnitude(L1List)
        mag2 = self.magnitude(L2List)
        dProduct = self.dotProduct(L1List, L2List)
        return dProduct/(mag1*mag2)
#Takes in a list of sentances. Compares every sentance with every other sentance
#returns list of tuples containing each sentance and their average similarity
#scores, along with sorting the list based off of the scores

    def getSimList(self, textSents):
        similarityList = []
        for i in range(len(textSents)):
            simSum = 0
            for j in range(len(textSents)):
                if i == j:
                    continue
                else:
                    simSum += (self.compareSentances(textSents[i],
                               textSents[j])/len(textSents))
            similarityList.append((textSents[i], simSum))
        return self.quickSort(similarityList)
#Takes the 4 most similar sentances and adds them together to create summary   
    def getSummary(self, L):
        sumList = L
        summary = ''
        for item in sumList:
            summary += item[0] + ' '
        return summary
#From https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#mergesort
#A modified version of the quick sort algorithm that sorts based off of the
#average similarity scores in the list
    def quickSort(self,L):
        if (len(L) < 2):
            return L
        else:
            first = L[0]  # pivot
            rest = L[1:]
            lo = [x for x in rest if x[1] < first[1]]
            hi = [x for x in rest if x[1] >= first[1]]
            return self.quickSort(lo) + [first] + self.quickSort(hi)
    def textWrap(self, s):
        result = ''
        for i in range(len(s.split())):
            if i % 26 == 0 and i != 0:
                result += s.split()[i] + '\n'
            else:
                result += s.split()[i] + ' '
        return result
    def updateSliders(self):
        self.numSumSents = self.slider.currentVal 
        self.sumList = self.simList[-1:-self.numSumSents:-1]
#Button Function################################################################
    def toTitleScreen(self, app):
        changeScreen(app, TitleScreen(app))
#Drawing function###############################################################
    def drawSummary(self, app, canvas):
        margin = app.height//8
        for i in range(len(self.sumList)):
            canvas.create_text(app.width//2, i*app.height//20+margin, text=self.textWrap(self.sumList[i][0]), justify='center')
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill='#CBC3E3')
        self.backButton.draw(app, canvas)
        self.drawSummary(app, canvas)
        canvas.create_text(app.width//2, app.height//14, text='Generated Summary:', font=
                           'Roboto 30')
        self.slider.draw(app, canvas)
        canvas.create_text(app.width//2, 9*app.height//10, text='Increase or Decrease Number of Sentances in Summary', font='Roboto 15')
        # canvas.create_text(app.width//2, app.height//4, 
        #                    text=f'Summary: {self.textWrap(self.summary)}')
#Defines the Text Adventure Screen Class
class TextAdventure(AppMode):
    def __init__(self, app):
        self.app = app
        print('Initializing TextAdventure')
        self.backButton = Button(5*app.width//6, 4*app.height//6, 
                                                app.width//7, app.height//8, 
                                                'Back', self.toTitleScreen)
        self.textBox = TextBox(app.width//2, 5*app.height//6, 2*app.width//3,
                               app.height//6)
        self.textBox.setHeader('')
        self.buttons = [self.backButton]
        self.textWords = self.cleanText(app.text)
        self.posTagged = pos_tag(self.textWords)
        self.lookupDict = self.createLookupDict(self.textWords)
        self.currentStory = ''
#Removes unwanted newline characters and returns a list of each word in the text
    def cleanText(self, text):
        result = ''
        for c in text:
            if c == '\n':
                c = ' '
                result += ' '
            else:
                result += c
        return self.removeStops(word_tokenize(result))
#Removes stop words(ie 'and, but, the, or' etc.)
    def removeStops(self, text):
        result = []
        for i in range(len(text)):
            if (text[i].lower() in stopwords.words('english') or text[i] in 
                string.punctuation or text[i] == '\''):
                pass
            else:
                result.append(text[i])
        return result
#Takes in a list of words and returns the lookup dictionary for the markov chain
#Currently only uses 1 ngram for lookup and stores each followup's frequency
    def createLookupDict(self,words):
        lookupDict = dict()
        for i in range(len(words)):
            lookupDict[words[i]] = dict()
        for j in range(len(words)-1):
            if words[j+1] not in lookupDict[words[j]]:
                lookupDict[words[j]][words[j+1]] = 1
            else:
                lookupDict[words[j]][words[j+1]] += 1
        return lookupDict
#From https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
#A modified version of the merge sort algorithm for sorting by frequency of each
#follow-up word in the markov chain lookup dictionary. Helper function
    def merge(self,a, start1, start2, end):
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
#Merge Sort Wrapper function used above
    def mergeSort(self,a):
        n = len(a)
        step = 1
        while (step < n):
            for start1 in range(0, n, 2*step):
                start2 = min(start1 + step, n)
                end = min(start1 + 2*step, n)
                self.merge(a, start1, start2, end)
            step *= 2
#Takes in a dictionary and returns a sortedlist of tuples containing each 
#key-value pair. Sorted based off of frequency(value)
    def dictToOrderedList(self, d):
        dictList = []
        for key in d.keys():
            dictList.append((key, d[key]))
        self.mergeSort(dictList)    
        return dictList
#Finds a bigram that contains the inputed word. Currently unused as bigram 
#generation isn't currently implemented in this version
    def findBigram(bigramDict, word):
        bigramList = list(bigramDict.keys())
        for bigram in bigramList:
            if word in bigram:
                return bigram
        return None
#Takes in a lookup dictionary, the starting word, and number of words generated
#returns a generated sentance starting with starting word with some randomness
    def generateSentance(self,lookupDict, startingWord, n):
        if startingWord.lower() not in lookupDict:
            nextPos = self.nextPOS(startingWord)
            possibleWords = []
            for item in self.posTagged:
                if item[1] in nextPos:
                    possibleWords.append(item[0])
            newWord = possibleWords[random.randrange(len(possibleWords))]
            result = startingWord + ' '+ newWord.lower() + ' '
            currentWord = newWord.lower()
        else:
            result = startingWord.lower() + ' '
            currentWord = startingWord.lower()
        for i in range(n):
            wordList = self.dictToOrderedList(lookupDict[currentWord])
            newWord = wordList[random.randrange(0, len(wordList))][0]
            result += newWord + ' '
            currentWord = newWord
        return result
#Takes in a string of word(s) and outputs the parts of speech that could not go
#afterwords.
#Note: Most of this function is attempting to define grammar rules
    def nextPOS(self, word):
        posDict = dict()
        posList = ['CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB']
        for item in posList:
            posDict[item] = set()
        posDict['CC'].update('CC', 'POS')
        posDict['CD'].update('CD', 'POS')
        posDict['DT'].update('CC', 'DT','POS' )
        posDict['EX'].update('EX', 'POS')
        posDict['IN'].update('CC', 'CD', 'EX', 'IN', 'LS', 
                        'MD','NNS', 'PDT', 'POS', 'RB', 'RBR', 'RBS', 'RP', 'TO', 
                        'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ','WDT', 'WP',
                        'WRB')
        posDict['JJ'].update('CC', 'CD', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'PDT', 'POS', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['JJR'].update('CC', 'CD', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'PDT', 'POS', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['JJS'].update('CC', 'CD', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'PDT', 'POS', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['MD'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VBG', 'VBD', 'VBN', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['NN'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'TO', 'UH', 
                'WDT', 'WP', 'WRB')
        posDict['NNP'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'TO', 'UH', 
                'WDT', 'WP', 'WRB')
        posDict['NNS'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'TO', 'UH', 
                'WDT', 'WP', 'WRB')
        posDict['PDT'].update('DT', 'POS')
        posDict['POS'].update('POS')
        posDict['PRP'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$',
                'RP', 'TO', 'UH',
                'WDT', 'WP', 'WRB')
        posDict['PRP$'].update('CC', 'CD', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                        'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
                'RBS', 'RP', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['RB'].update('POS')
        posDict['RBR'].update('POS')
        posDict['RP'].update('CC', 'CD','EX', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
                'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR',
                'RBS', 'TO', 'UH', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ',
                'WDT', 'WP', 'WRB')
        posDict['TO'].update('POS')
        posDict['UH'].update('POS')
        posDict['VB'].update('POS')
        posDict['VBD'].update('POS')
        posDict['VBG'].update('POS')
        posDict['VBN'].update('POS')
        posDict['VBP'].update('POS')
        posDict['VBZ'].update('POS')
        posDict['WDT'].update('POS', 'WDT', 'WP')
        posDict['WP'].update('POS', 'WDT', 'WP')
        posDict['WRB'].update('POS', 'WRB')
        wordPOS = pos_tag([word])[0][1]
        result = set()
        if word[0].isalnum():
            for item in posList:
                if item not in posDict[wordPOS]:
                    result.add(item)
        else:
            for item in posList:
                result.add(item)
        return result
#Button Function################################################################    
    def toTitleScreen(self,app):
        changeScreen(app, TitleScreen(app))
#Drawing Function###############################################################
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill='#90EE90')
        self.backButton.draw(app, canvas)
        self.textBox.draw(app, canvas)
        canvas.create_text(app.width//2, app.height//15, text='Free Text Generator', font='Roboto 30')
        canvas.create_text(app.width//2, app.height//9+len(self.
                           currentStory.splitlines())*app.height/90, 
                           text=self.currentStory)
#Defiens the Import Text File Screen Class
class ImportScreen(AppMode):
    def __init__(self, app):
        self.backButton = Button(5*app.width//6, 4*app.height//6, 
                                                app.width//7, app.height//8, 
                                                'Back', self.toTitleScreen)
        self.textBox = TextBox(app.width//2, 4*app.height//5, app.width//2,
                                   app.height//5)
        self.textBox.setHeader('')
        self.fileImported = False
        self.badImport = False
        self.buttons = [self.backButton]
#Button Function################################################################
    def toTitleScreen(self, app):
        changeScreen(app, TitleScreen(app))
#Drawing Function###############################################################
    def drawImportMessage(self, app, canvas):
        if self.fileImported:
            canvas.create_text(app.width//2, 2*app.height//3, text=f'{self.textBox.storedText} was successfully imported!', font='Roboto 15')
        elif self.badImport:
            canvas.create_text(app.width//2, 2*app.height//3, text='Invalid filename. Please try again!', font='Roboto 15')
    def draw(self, app, canvas):
        canvas.create_rectangle(0,0, app.width, app.height, fill='pink')
        canvas.create_text(app.width//2, app.height//4, font='Roboto 30', text='Import Your File')
        canvas.create_text(app.width//2, 2*app.height//5, font='Roboto 15', text='Type the file you want to import. Make sure to include the file extension!')
        canvas.create_text(app.width//2, app.height//2, font='Roboto 15', text='Press enter to import')
        self.drawImportMessage(app, canvas)
        self.backButton.draw(app, canvas)
        self.textBox.draw(app, canvas)
################################################################################
#
#                               App Object Classes
#
################################################################################
#Parent class for app object(TextBoxes and Buttons). Currently unuesed
class AppObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#Defines the Class for the Text Box Object that Gathers User Input
class TextBox(AppObject):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.header = "Dummy Header, Please set"
        self.font = 'Roboto 20'
        self.input = ''
        self.storedText = ''
        self.inputIndex = 0
    def getHeader(self):
        return self.header
    def setHeader(self, s):
        self.header = s
#Adds user input to input variable. If enter was pressed. Stores text for use
    def getUserInput(self, key):
        if len(key) == 1:
            self.input += key
        elif key == 'Backspace':
            self.input = self.input[0:-1]
        elif key == 'Space':
            self.input += ' '
        elif key == 'Enter':
            if self.input.isspace():
                return
            self.storeText()
#Stores inputed text
    def storeText(self):
        self.storedText = self.input
        self.input = ''
#Drawing Function###############################################################
    def draw(self, app, canvas):
        x0, x1 = self.x-self.width//2, self.x+self.width//2
        y0, y1 = self.y-self.height//2, self.y+self.height//2
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text(self.x, self.y-self.height//4, text=self.header)
        canvas.create_text(self.x, self.y+self.height//4, text=self.input, font=self.font)
#Defines the Class for the Button Object that allows for a function when clicked
class Button(AppObject):
    def __init__(self, x, y, width, height, text, function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.function = function
        self.pressed = False
        buttonList.append(self)
#Takes in the app and an x and y, checks if the button was pressed
#Calls the button's function if pressed
    def checkPressed(self, app, x, y):
        if (x >= self.x-self.width//2 and x <= self.x+self.width//2 and y >= 
            self.y-self.height//2 and y <= self.y+self.height//2):
            self.pressed = True
            self.function(app)
        else:
            self.pressed = False
#Drawing Function###############################################################
    def draw(self, app, canvas):
        x0, x1 = self.x-self.width//2, self.x+self.width//2
        y0, y1 = self.y-self.height//2, self.y+self.height//2
        if self.pressed == True:
            canvas.create_rectangle(x0,y0,x1,y1, fill='blue')
        else:
            canvas.create_rectangle(x0,y0,x1,y1, fill='yellow')
        canvas.create_text(self.x, self.y, text=self.text)

class Graph(AppObject):
    def __init__(self, x ,y, width, height):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.yValNums = 5
        self.graphColor = 'Blue'
    def setXData(self, data):
        self.xData = data
    def setYValNums(self, n):
        self.yValNums = n
    def setColor(self, color):
        self.graphColor = color
    def scaleY(self):
        maxVal = self.xData[0][1]
        for val in self.xData:
            if val[1] > maxVal:
                maxVal = val[1]
        self.maxVal = maxVal
    def drawBar(self, canvas, x0, x1, val):
        y0 = self.y+self.height//2
        y1 = y0 - self.height*(val/self.maxVal)
        canvas.create_rectangle(x0,y0,x1,y1,fill=self.graphColor)
        canvas.create_text((x0+x1)/2,y1 - self.height//8, text=int(val))
    def drawDataPoints(self, canvas):
        self.scaleY()
        margin = self.width//len(self.xData) + 1/4 * self.width//len(self.xData)
        for i in range(len(self.xData)):
            x0 = self.x - self.width//2 + (i)*self.width//len(self.xData) + margin//2
            x1 = self.x - self.width//2 + (i+1)*self.width//len(self.xData)
            self.drawBar(canvas, x0, x1, self.xData[i][1])
            canvas.create_text((x0+x1)/2, self.y+self.height//2 +self.height//8,
                               text=str(self.xData[i][0][0]), font='Roboto 10')
    def drawGrid(self, canvas):
        for i in range(self.yValNums+1):
            num = i*self.maxVal//self.yValNums
            y = self.y + self.height//2 - (i*self.height//self.yValNums) 
            canvas.create_line(self.x-self.width//2-self.width//15, y, 
                               self.x-self.width//2+self.width//15, y)
            canvas.create_text(self.x-self.width//2-self.width//8, y, text=num)
    def draw(self, app, canvas):
        self.drawDataPoints(canvas)
        self.drawGrid(canvas)
        canvas.create_rectangle(self.x-self.width//2, self.y-self.height//2,
                               self.x+self.width//2, self.y+self.height//2)

class Slider(AppObject):
    def __init__(self, x, y, len, minVal, maxVal):
        self.x = x
        self.y = y
        self.len = len
        self.minVal = minVal
        self.maxVal = maxVal
        self.currentVal = 0
        self.curRatio = 0
        self.curValX = self.x - len//2 + self.currentVal/self.maxVal*self.len
        self.color = 'black'
    def updateValue(self,x, y):
        if (x <= self.curValX + self.len//6 and 
            x >= self.curValX - self.len//6 and y >= self.y - self.len//6 and
            y <= self.y + self.len//6):
            if x > self.x + self.len//2:
                x = self.x +self.len//2
            elif x < self.x - self.len//2:
                x = self.x - self.len//2
            self.curValX = x
            self.curRatio = (self.curValX - self.x+self.len//2)/self.len
            self.currentVal = int(self.curRatio * self.maxVal)
            if self.currentVal < self.minVal:
                self.currentVal = self.minVal
    def drawLine(self, canvas):
        canvas.create_line(self.x-self.len//2, self.y, self.x+self.len//2,
                           self.y)
    def drawPointer(self, canvas):
        canvas.create_oval(self.curValX-self.len//15, self.y-self.len//15,
                           self.curValX+self.len//15, self.y+self.len//15, 
                           fill=self.color)
    def draw(self, app, canvas):
        self.drawLine(canvas)
        self.drawPointer(canvas)
################################################################################
#
#                              App Functions
#
################################################################################
def appStarted(app):
    app.titleScreen = TitleScreen(app)
    app.currentScreen = app.titleScreen
    app.text = None
    app.textFileName = ' '
#Changes the Screen to the target screen
def changeScreen(app, targetMode):
    app.currentScreen = targetMode

def mousePressed(app, event):
    for button in app.currentScreen.buttons:
        button.checkPressed(app, event.x, event.y)

def mouseDragged(app, event):
    if isinstance(app.currentScreen, GraphScreen):
        for slider in app.currentScreen.sliders:
            slider.updateValue(event.x, event.y)
    elif isinstance(app.currentScreen, SummaryScreen):
        app.currentScreen.slider.updateValue(event.x, event.y)

def mouseReleased(app, event):
    app.sliderDrag = False

def keyPressed(app, event):
    cursc = app.currentScreen
    if isinstance(cursc, ImportScreen):
        cursc.textBox.getUserInput(event.key)
        if cursc.textBox.storedText != '' and event.key == 'Enter':
            try: 
                app.text = open(cursc.textBox.storedText, 
                                encoding='utf8').read()
                app.textFileName = cursc.textBox.storedText
            except:
                cursc.textBox.header = ''
                cursc.textBox.storedText = ''
                cursc.badImport = True
                app.text = None
                app.textFileName = ' '
            else:
                # cursc.textBox.header = ('File succesfully imported! ' +
                #                   f'Imported File = {cursc.textBox.storedText}') 
                cursc.fileImported = True
                cursc.badImport = False
    elif isinstance(app.currentScreen, TextAdventure):
        cursc.textBox.getUserInput(event.key)
        if cursc.textBox.input.isspace():
            return
        if event.key == 'Enter':
            cursc.currentStory += ('\n' + cursc.generateSentance(cursc.lookupDict, 
                                  cursc.textBox.storedText.split()[0], 
                                  random.randrange(7,15)))
            if len(cursc.currentStory.splitlines()) > 21:
                result = ''
                for i in range(1, len(cursc.currentStory.splitlines())):
                    result += cursc.currentStory.splitlines()[i] + '\n'
                cursc.currentStory = result.strip()

def timerFired(app):
    if isinstance(app.currentScreen, GraphScreen) or isinstance(app.currentScreen, SummaryScreen):
        app.currentScreen.updateSliders()
    

def redrawAll(app, canvas):
    app.currentScreen.draw(app, canvas)

def startApp():
    width = 1280
    height = 697
    runApp(width=width, height=height)

startApp()