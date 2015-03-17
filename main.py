import nltk
# -*- coding: utf-8 -*-
import os

from PrintingFunctions import *
from IntentionDetection import *


################################
## Load text provided by user ##
################################

fileName = raw_input('File Name: ')
if fileName == "": fileName = 'exampleText.txt'
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

#######################
## Ask user for task ##
#######################

print "And what would you like to do with this file?"
print "1: Print all intentional sentences"
print "2: Give the number of sentences in the entire document"
print "3: Print report on density of intentional statements in text"
selectedFunction = input()
print "\n"

if selectedFunction == 1:
    ## 1: Print all intentional sentences
    for eachParagraph in paragraphs:
        print eachParagraph
        if len(eachParagraph) > 0 and eachParagraph != "\n":
            print "Intentional Sentences:"
            print DetectIntentions(eachParagraph)
elif selectedFunction == 2:
    ## 2: Give the number of sentences in the entire document
    mySum = 0
    for eachParagraph in paragraphs:
        mySum += countSentences(eachParagraph)
    print "Number of sentences: " + str(mySum)
elif selectedFunction == 3:
    ## 3: Print report on density of intentional statements in text
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