import json
import nltk
# -*- coding: utf-8 -*-

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import re


def DetectIntentions(originalTaggedText):
    ############################################################
    ## Returns a sentence when given a word with its location ##
    ############################################################
    def GrabSentence(word, capitalize=True, taggedVersion=False):
        ## Find where the sentence starts
        startDisp = 0
        '''print "\n\n\n"
        print word
        print originalTaggedText[word[2]+startDisp][0][0]
        print "\n\n\n"'''
        while originalTaggedText[word[2]+startDisp][0][0] != "." and originalTaggedText[word[2]+startDisp][0][0] != ";" and (originalTaggedText[word[2]+startDisp][0][0] != "!" or originalTaggedText[word[2]+startDisp+1][0][0] != '"') and originalTaggedText[word[2]+startDisp][0][0] != "?":
            startDisp -= 1
            if word[2]+startDisp < 0: break
        try:
            if not (originalTaggedText[word[2]+endDisp][0][0] == "!" and originalTaggedText[word[2]+endDisp+1][0][0] != '"'):
                print "COMBINED EXCLAMATION AND QUOTE"
                print originalTaggedText[word[2]+endDisp][1][0]
                print originalTaggedText[word[2]+endDisp+1][1][0]
        except:
            startDisp += 1
        ## Find where the sentence ends
        endDisp = 0
        while originalTaggedText[word[2]+endDisp][0][0] != "." and originalTaggedText[word[2]+endDisp][0][0] != ";" and (originalTaggedText[word[2]+endDisp][0][0] != "!" or originalTaggedText[word[2]+endDisp+1][0][0] != '"') and originalTaggedText[word[2]+endDisp][0][0] != "?":
            endDisp += 1
            try:
                originalTaggedText[word[2]+endDisp][0][0] != "."
            except:
                endDisp -= 1
                break
        endDisp += 1
        try:  # I want to remove these
            if (originalTaggedText[word[2]+endDisp][1][0] == "!" and originalTaggedText[word[2]+endDisp+1][1][0] != '"'):
                print "COMBINED EXCLAMATION AND QUOTE"
                print originalTaggedText[word[2]+endDisp][0][0]
                print originalTaggedText[word[2]+endDisp+1][0][0]
        except:
            "don't fix what ain't broke I guess"
        ## Smash the sentence together into a human-readable string or isolated tagged sentence
        sentence = []
        if taggedVersion is False:
            for i in range(endDisp - startDisp):
                if startDisp == -i and capitalize is True:
                    sentence.append(str.upper(str(originalTaggedText[word[2]+startDisp+i][0])))  # Capitalize the word passed to the function
                else:
                    sentence.append(originalTaggedText[word[2]+startDisp+i][0])
            sentence = ' '.join(sentence)
            ## The above process adds unnecessary spaces before punctuation,
            ## which we remove below.
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
            sentence = sentence.replace(" '", "'")
            sentence = sentence.replace("''", '"')
            sentence = sentence.replace("`` ", '"')
        elif taggedVersion is True:
            for i in range(endDisp - startDisp):
                if startDisp == -i and capitalize is True:
                    # Capitalize the word passed to the function
                    appendThis = [str.upper(originalTaggedText[word[2]+startDisp+i][0]), originalTaggedText[word[2]+startDisp+i][1]]
                    sentence.append(appendThis)
                else:
                    sentence.append(originalTaggedText[word[2]+startDisp+i])
        return sentence
    ###################################
    ## Detect verb beliefs/attitudes ##
    ###################################
    outputWordList = []  # This will contain all of the words we find that signal a belief/attitude is present
    ## Grab all verbs and put them in a list
    spot = 0
    verbList = []
    for tag in originalTaggedText:
        if tag[1][0] == "V":
            verb = [tag[0], tag[1], spot]
            verbList.append(verb)
        spot += 1
    ## Find any belief verbs
    beliefVerbs = ["believe", "believes", "believed", "believing", "know", "knows", "knew", "knowing", "perceive", "perceives", "perceive", "perceiving", "notice", "notices", "noticed", "noticing", "remember", "remembers", "remembered", "remembering", "imagine", "imagines", "imagined", "imagining", "suspect", "suspects", "suppose", "suspecting", "assume", "presume", "surmise", "conclude", "deduce", "understand", "understands", "understood", "understanding", "judge", "doubt", "thought"]
    verb = []
    for verb in verbList:
        for testVerb in beliefVerbs:
            if str.lower(verb[0]) == testVerb:
                outputWordList.append(verb)
    ## Find any attitude verbs
    attitudeVerbs = ["want", "wanted", "wants", "wish", "wishes", "wished", "consider", "considers", "considered", "desire", "desires", "desired", "hope", "hoped", "hopes", "aspire", "aspired", "aspires", "fancy", "fancied", "fancies", "care", "cares", "cared", "like", "likes", "liked"]
    verb = []
    for verb in verbList:
        for testVerb in attitudeVerbs:
            if str.lower(verb[0]) == testVerb:
                outputWordList.append(verb)
    #######################################
    ## Detect non-verb beliefs/attitudes ##
    #######################################
    ## Find 'is' verbs
    isWords = ["is", "was", "were", "are"]
    isVerbsFound = []
    for eachVerb in verbList:
        for testVerb in isWords:
            if str.lower(eachVerb[0]) == testVerb:
                isVerbsFound.append(eachVerb)
    beliefNonVerbs = ["belief", "beliefs", "knowledge", "perception", "perceptions", "memory", "memories", "suspicion", "suspicions", "assumption", "assumptions", "presupposition", "presuppositions", "suppositions", "supposition", "conclusion", "conclusions", "understanding", "judgment", "doubt", "doubts"]
    attitudeNonVerbs = ["desire", "desires", "wants", "want", "wish", "wishes", "hope", "hopes", "aspirations", "aspiration", "fancy", "fancies", "care", "cares", "longing"]
    ## “(PRP) (belief/attitude) is…”
    for isVerb in isVerbsFound:
        ## First, apply a grammar
        grammar = r"""
          NP: {<DT|PRP\$|NNP>?<JJ>*<NN><VB.|VB>}
        """
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(GrabSentence(isVerb, taggedVersion=True, capitalize=False))
        ## Then, extract the chunks found by the grammar
        foundChunks = []
        for eachResult in result:
            if str(eachResult).count('/') > 0:
                foundChunks.append(eachResult)
        ## Check if the subject is a belief/attitude word
        for eachChunk in foundChunks:
            for eachWord in eachChunk:
                if eachWord[1] == "NN":
                    for eachBeliefNonverb in beliefNonVerbs:
                        if str.lower(eachWord[0]) == eachBeliefNonverb:
                            verb = [isVerb[0], isVerb[1], isVerb[2]]
                            outputWordList.append(verb)
                    for eachAttitudeNonverb in attitudeNonVerbs:
                        if str.lower(eachWord[0]) == eachAttitudeNonverb:
                            verb = [isVerb[0], isVerb[1], isVerb[2]]
                            outputWordList.append(verb)
    ## Find 'that' conjunctions
    index = 0
    THATWordsFound = []
    for eachTaggedWord in originalTaggedText:
        if str.lower(eachTaggedWord[0]) == "that":
            word = [eachTaggedWord[0], eachTaggedWord[1], index]
            THATWordsFound.append(word)
        index += 1
    phenomenalVerbs = ["feel", "feels", "thought"]
    ## “(VB) that ...”
    for thatWord in THATWordsFound:
        ## First, apply a grammar
        grammar = r"""
          NP: {<VB.|VB><IN>}
        """
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(GrabSentence(thatWord, taggedVersion=True, capitalize=False))
        ## Then, extract the chunks found by the grammar
        foundChunks = []
        for eachResult in result:
            if str(eachResult).count('/') > 0:
                foundChunks.append(eachResult)
        ## Check if the subject is a belief/attitude word
        for eachChunk in foundChunks:
            for eachWord in eachChunk:
                if eachWord[1] == "VB":
                    for eachPhenomenalVerb in phenomenalVerbs:
                        if str.lower(eachWord[0]) == eachPhenomenalVerb:
                            verb = [thatWord[0], thatWord[1], thatWord[2]]
                            outputWordList.append(verb)
    functionOutput = []
    for word in outputWordList:
        functionOutput.append(GrabSentence(word))
    functionOutput = '\n'.join(functionOutput)
    return functionOutput


#####################################
## Returns the number of sentences ##
#####################################

def countSentences(tokens, returnMarkers=False):
    #if text == "\n": return 0
    ## Tokenize
    #tokens = nltk.word_tokenize(text)
    ## Find where sentences start
    markers = []
    findDisp = 0
    for eachToken in tokens:
        if eachToken == "." or eachToken == ";" or eachToken == "!" or eachToken == "?":
            markers.append(findDisp)
        findDisp += 1
    if markers == []:
        markers.append(len(tokens))
    elif markers[len(markers)-1] != len(tokens)-1:
        markers.append(len(tokens))
    if returnMarkers is False:
        return len(markers)
    else:
        return markers


if __name__ == "__main__":
    ##  If loaded alone, will run the below interface
    ##  If loaded in shell program, will load without executing anything
    ################################
    ## Load text provided by user ##
    ################################
    import os
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
        '''if selectedFunction == 1:
        ## 1: Print all intentional sentences
        print "Do you want to print just the intentional sentences? y/n"
        printJustIntent = raw_input()
        for eachParagraph in paragraphs:
            if printJustIntent == "n": print eachParagraph
            if len(eachParagraph) > 0 and eachParagraph != "\n":
                paraIntentions = DetectIntentions(eachParagraph)
                if paraIntentions != "":
                    print "Intentional Sentences:"
                    print paraIntentions'''
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
            print "eachParagraph"
            print eachParagraph
            print "\n"
            #if len(eachParagraph) > 0 and eachParagraph != "\n":
            sentenceMarkers = countSentences(eachParagraph, returnMarkers=True)
            wordlist = DetectIntentions(eachParagraph)
            print "sentenceMarkers:"
            print sentenceMarkers
            print "wordlist:"
            print wordlist
            print "\n"
            for eachSentence in range(len(sentenceMarkers)):
                thisDensity = 0
                for eachWord in wordlist:
                    if (eachWord[2] > sentenceMarkers[eachSentence-1] or eachSentence == 0) and eachWord[2] < sentenceMarkers[eachSentence]:
                        thisDensity += 1
                density.append(thisDensity)
        print "density"
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
        myfile = open('outputDensity.intention', 'r+')
        json.dump(density, myfile)
    else:
        print "Invalid entry"
    text_file.close()
