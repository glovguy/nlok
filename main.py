import nltk
# -*- coding: utf-8 -*-
import os

#from PrintingFunctions import *
from IntentionDetection import *


################################
## Load text provided by user ##
################################

fileName = raw_input('File Name: ')
if fileName == "":
    print "no filename given, using exampleText.txt as default"
    fileName = 'exampleText.txt'
if fileName[-3:] != "txt":
    if fileName[len(str(fileName))-4] == ".": quit("unrecognized filetype")
    print "No file extension, assuming it's a .txt file"
    fileName = fileName + ".txt"
print "Loading..."
try:
    text_file = open(fileName, "r")
except:
    try:
        print "Looking also in /TextExamples folder"
        myCWD = os.getcwd()
        fileName = myCWD + "/TextExamples/" + fileName
        print fileName
        text_file = open(fileName, "r")
    except:
        quit("ERROR FINDING FILE")
paragraphs = text_file.readlines()
print "done \n"


#################################
## Ask user for task and do it ##
#################################

print "And what would you like to do with this file?"
print "1: Print all intentional sentences"
print "2: Give the number of sentences in the entire document"
print "3: Print report on density of intentional statements in text"
print "0: Unit tests"
selectedFunction = input()


def tagAndTokenize():
    pos_tagged_paragraphs = []
    for eachParagraph in paragraphs:
        if len(eachParagraph) > 0 and eachParagraph != "\n":
            global tokens
            tokens = nltk.word_tokenize(eachParagraph)
            pos_tagged_paragraphs.append(nltk.pos_tag(tokens))
    print "\n\n"
    return pos_tagged_paragraphs


if selectedFunction == 1:
    ## 1: Print all intentional sentences
    ## Need more info
    print "Do you want to print just the intentional sentences? y/n"
    printJustIntent = raw_input()
    if printJustIntent == "no": printJustIntent = "n"
    
    ## First tokenize and tag the paragraphs
    pos_tagged_paragraphs = tagAndTokenize()
    
    for eachParagraph in pos_tagged_paragraphs:
        if printJustIntent == "n": print eachParagraph
        paragraphIntentions = DetectIntentions(eachParagraph)
        if paragraphIntentions != "":
            if printJustIntent == "n": print "Intentional Sentences:"
            print paragraphIntentions
    print "\n"
                
                
elif selectedFunction == 2:
    ## 2: Give the number of sentences in the entire document
    print "\n\n"
    mySum = 0
    for eachParagraph in paragraphs:
        mySum += countSentences(eachParagraph)
    print "Number of sentences: " + str(mySum)
    
    
elif selectedFunction == 3:
    ## 3: Print report on density of intentional statements in text
    
    ## First tokenize and tag the paragraphs
    pos_tagged_paragraphs = tagAndTokenize()
    
    density = []
    for eachParagraph in pos_tagged_paragraphs:
        print eachParagraph
        #if len(eachParagraph) > 0 and eachParagraph != "\n":
        sentenceMarkers = countSentences(eachParagraph, returnMarkers=True)
        wordlist = DetectIntentions(eachParagraph)
        print sentenceMarkers
        print wordlist
        for eachSentence in range(len(sentenceMarkers)):
            thisDensity = 0
            for eachWord in wordlist:
                if (eachWord[2] > sentenceMarkers[eachSentence-1] or eachSentence == 0) and eachWord[2] < sentenceMarkers[eachSentence]:
                    thisDensity += 1
            density.append(thisDensity)
    print density
    
    
elif selectedFunction == 0:
    ## Perform unit tests
    print "\n\n"
    ## First, test the intention density feature, since it is the most rigorous
    unitTestText = """
    "How deaf and stupid have I been!" he thought, walking swiftly along. "When someone reads a text, wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions, coincidence, and worthless hull, but he will read them, he will study and love them, letter by letter. But I, who wanted to read the book of the world and the book of my own being, I have, for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I called the visible world a deception, called my eyes and my tongue coincidental and worthless forms without substance. No, this is over, I have awakened, I have indeed awakened and have not been born before this very day."
    This is a sentence that doesn't express intention. I want this sentence to express intention..
    He started to feel that that was enough coffee for today.
    """
    density = []
    for eachParagraph in paragraphs:
        print eachParagraph
        if len(eachParagraph) > 0 and eachParagraph != "\n":
            sentenceMarkers = countSentences(eachParagraph, returnMarkers=True)
            wordlist = DetectIntentions(eachParagraph)
            print sentenceMarkers
            print wordlist
            for eachSentence in range(len(sentenceMarkers)):
                thisDensity = 0
                for eachWord in wordlist:
                    if (eachWord[2] > sentenceMarkers[eachSentence-1] or eachSentence == 0) and eachWord[2] < sentenceMarkers[eachSentence]:
                        thisDensity += 1
                density.append(thisDensity)
    print density
    
    
else:
    print "Invalid entry"


text_file.close()