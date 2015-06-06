import nltk
# -*- coding: utf-8 -*-

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import re

def DetectIntentions(originalText):

    ###################################################
    ## Grab all the words and compute out POS tokens ##
    ###################################################
    
    #returnSentence = []
    
    ## Tokenize
    global tokens
    tokens = nltk.word_tokenize(originalText)
    #print "TOKENS"
    #print tokens
    
    ## Tag the tokens
    global pos_tagged_tokens
    pos_tagged_tokens = nltk.pos_tag(tokens)
    #print "TAGGED PARAGRAPH"
    #print pos_tagged_tokens
    
    ## Named entity chunking
    #namedEntitySentence = nltk.ne_chunk(pos_tagged_tokens)
    
    ## Chunk
    #grammar = r"""
    #  NP: {<DT|PRP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
    #      {<NNP>+}                # chunk sequences of proper nouns
    #"""
    #cp = nltk.RegexpParser(grammar)
    #result = cp.parse(pos_tagged_tokens)
    #print "CHUNKED PARAGRAPH"
    #print result
    
    ############################################################
    ## Returns a sentence when given a word with its location ##
    ############################################################
    
    def GrabSentence(word, capitalize = True, taggedVersion = False):
        
        ## Find where the sentence starts
        startDisp = 0
        while tokens[word[2]+startDisp][0] != "." and tokens[word[2]+startDisp][0] != ";" and (tokens[word[2]+startDisp][0] != "!" or tokens[word[2]+startDisp+1][0] != '"') and tokens[word[2]+startDisp][0] != "?":
            startDisp -= 1
            if word[2]+startDisp < 0: break
            #try:
                #if (tokens[word[2]+endDisp][0] == "!" and tokens[word[2]+endDisp+1][0] != '"'):
                    #print "COMBINED EXCLAMATION AND QUOTE"
                    #print tokens[word[2]+endDisp][0]
                    #print tokens[word[2]+endDisp+1][0]
            #except:
                #print "end of string"
        startDisp += 1
        
        ## Find where the sentence ends
        endDisp = 0
        while tokens[word[2]+endDisp][0] != "." and tokens[word[2]+endDisp][0] != ";" and (tokens[word[2]+endDisp][0] != "!" or tokens[word[2]+endDisp+1][0] != '"') and tokens[word[2]+endDisp][0] != "?":
            endDisp += 1
            try:
                tokens[word[2]+endDisp][0] != "."
            except:
                endDisp -= 1
                break
        endDisp += 1
        #try:
            #if (tokens[word[2]+endDisp][0] == "!" and tokens[word[2]+endDisp+1][0] != '"'):
                #print "COMBINED EXCLAMATION AND QUOTE"
                #print tokens[word[2]+endDisp][0]
                #print tokens[word[2]+endDisp+1][0]
        #except:
            #print "end of string"
        
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
            sentence = sentence.replace(" '", "'")
        elif taggedVersion == True:
            for i in range(endDisp - startDisp):
                if startDisp == -i and capitalize == True:
                    # Capitalize the word passed to the function
                    appendThis = [str.upper(pos_tagged_tokens[word[2]+startDisp+i][0]), pos_tagged_tokens[word[2]+startDisp+i][1]]
                    sentence.append(appendThis)
                else:
                    sentence.append(pos_tagged_tokens[word[2]+startDisp+i])
        
        return sentence
    
    ###################################
    ## Detect verb beliefs/attitudes ##
    ###################################
    
    outputWordList = [] ## This will contain all of the words we find that signal a belief/attitude is present
    
    ## Grab all verbs and put them in a list
    spot = 0
    verbList = []
    for tag in pos_tagged_tokens:
        if tag[1][0] == "V":
            verb =  [tag[0], tag[1], spot]
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
    attitudeNonVerbs = ["desire", "desires", "wants", "want", "wish", "wishes", "hope", "hopes", "aspirations", "aspiration", "fancy", "fancies", "care", "cares", "longing", "intention", "intentions"]
    
    ## “(PRP) (belief/attitude) is…”
    for isVerb in isVerbsFound:
        ## First, apply a grammar
        grammar = r"""
          NP: {<DT|PRP\$|NNP>?<JJ>*<NN><VB.|VB>}
        """
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(GrabSentence(isVerb,taggedVersion=True,capitalize=False))
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
    for eachTaggedWord in pos_tagged_tokens:
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
        result = cp.parse(GrabSentence(thatWord,taggedVersion=True,capitalize=False))
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
    functionOutput = '\n\n'.join(functionOutput)
    return functionOutput


#####################################
## Returns the number of sentences ##
#####################################

def countSentences(text, returnMarkers = False):
    if text == "\n": return 0
    
    ## Tokenize
    tokens = nltk.word_tokenize(text)
    
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
    
    if returnMarkers == False: return len(markers)
    else: return markers

