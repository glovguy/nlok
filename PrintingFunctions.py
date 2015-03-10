import nltk
# -*- coding: utf-8 -*-

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import re

from IntentionDetection import *

## Define a function that prints a sentence when given a word with its location in the tokens list
def PrintSentence(word, capitalize = True, taggedVersion = False):
    ## Find where the sentence starts
    startDisp = 0
    while tokens[word[2]+startDisp][0] != "." and tokens[word[2]+startDisp][0] != ";" and tokens[word[2]+startDisp][0] != "!" and tokens[word[2]+startDisp][0] != "?":
        startDisp = startDisp - 1
    startDisp = startDisp + 1
    
    ## Find where the sentence ends
    endDisp = 0
    while tokens[word[2]+endDisp][0] != "." and tokens[word[2]+endDisp][0] != ";" and tokens[word[2]+endDisp][0] != "!" and tokens[word[2]+endDisp][0] != "?":
        endDisp = endDisp + 1
    endDisp = endDisp + 1
    
    ## Smash the sentence together into a human-readable string or isolated tagged sentence
    sentence = []
    if taggedVersion == False:
        for i in range(endDisp - startDisp):
            if startDisp == -i and capitalize == True:
                sentence.append(str.upper(str(tokens[word[2]+startDisp+i])))  # Capitalize the word passed to the function
            else:
                sentence.append(tokens[word[2]+startDisp+i])
        sentence = ' '.join(sentence)
        ## The above process adds unnecessary spaces before punctuation.
        ## Let's remove those.
        sentence = sentence.replace(" .", ".")
        sentence = sentence.replace(" ,", ",")
        sentence = sentence.replace(" !", "!")
        sentence = sentence.replace(" ;", ";")
        sentence = sentence.replace(" :", ":")
        sentence = sentence.replace(" ?", "?")
        sentence = sentence.replace(" 's", "'s")
        sentence = sentence.replace(" 'd", "'d")
        sentence = sentence.replace(" 've", "'ve")
        sentence = sentence.replace(" n't", "n't")
    elif taggedVersion == True:
        for i in range(endDisp - startDisp):
            if startDisp == -i and capitalize == True:
                # Capitalize the word passed to the function
                appendThis = (str.upper(pos_tagged_tokens[word[2]+startDisp+i][0]), pos_tagged_tokens[word[2]+startDisp+i][1])
                sentence.append(appendThis)
            else:
                sentence.append(pos_tagged_tokens[word[2]+startDisp+i])
    
    return sentence