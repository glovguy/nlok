import json
import nltk
from language import Sentence, Word
# -*- coding: utf-8 -*-


def detect_nonverb_beliefs_and_attitudes(sentence):
    if sentence.contains_a_being_verb() is False: return False
    ## "(PRP) (belief/attitude) is..."
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_belief_or_attitude_word()


def find_all_that_words(POSTaggedSentence):
    index = 0
    THATWordsFound = []
    for eachTaggedWord in originalTaggedText:
        if str.lower(eachTaggedWord[0]) == "that":
            word = wordPickedFromPOStaggedSentence(eachTaggedWord[0], eachTaggedWord[1], index)
            THATWordsFound.append(word)
        index += 1
    return THATWordsFound


def detect_intention_using_that_clauses(POSTaggedSentence):
    THATWordsFound = find_all_that_words(POSTaggedSentence)
    if THATWordsFound is []:
        return []
    phenomenalVerbs = [
        "feel", "feels", "thought", "think"
    ]
    ## "(VB) that ..."
    for thatWord in THATWordsFound:
        ## First, apply a grammar
        grammar = r"""
          TP: {<VB.|VB><IN>}
        """
        myParser = nltk.RegexpParser(grammar)
        result = myParser.parse(GrabSentence(thatWord, taggedVersion=True, capitalize=False))
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
    return True


def is_sentence_intentional(sentence):
    ############################################################
    ## Returns a sentence when given a word with its location ##
    ############################################################
    return sentence.contains_belief_verb() or \
        sentence.contains_attitude_verb() or \
        detect_nonverb_beliefs_and_attitudes(sentence)
    detect_nonverb_beliefs_and_attitudes(sentence)
    detect_intention_using_that_clauses(sentence)
    raise Exception


def print_all_intentional_sentences(raw_text):
    tokens = IntentionDetection.tokenize_each_sentence(raw_text)
    pos_tagged_paragraphs = IntentionDetection.pos_tag_each_tokenized_sentence(tokens)
    for eachParagraph in pos_tagged_paragraphs:
        print eachParagraph
        paragraphIntentions = IntentionDetection.DetectIntentions(eachParagraph)
        if paragraphIntentions != "":
            print "Intentional Sentences:"
            print paragraphIntentions
    print "\n"


def total_number_of_intentional_sentences(raw_text):
    print "\n\n"
    mySum = 0
    # Use this sentence separator from nltk instead of whatever stupid method I was using.
    '''sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    print('\n-----\n'.join(sent_detector.tokenize(text.strip())))'''
    # outline:
    # cut text into sentences
    # cycle through each sentence
    #     ask if each sentence is intentional or not
    #     keep a running total
    # return total
    for eachParagraph in raw_text:
        mySum += countSentences(eachParagraph)
    print "Number of sentences: " + str(mySum)


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


def report_density_of_intentional_sentences(raw_text):
    tokens = tokenize_each_sentence(raw_text)
    pos_tagged_paragraphs = pos_tag_each_tokenized_sentence(tokens)
    density = []
    for eachParagraph in pos_tagged_paragraphs:
        print "eachParagraph"
        print eachParagraph
        print "\n"
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
    myfile = open('outputDensity.intention', 'r+')
    json.dump(density, myfile)


def tokenize_each_sentence(paragraphs):
        tokens = []
        for eachParagraph in paragraphs:
            if len(eachParagraph) > 0 and eachParagraph != "\n":
                eachToken = nltk.word_tokenize(eachParagraph)
                tokens.append(eachToken)
        return tokens


def pos_tag_each_tokenized_sentence(tokens):
        pos_tagged_paragraphs = []
        for eachToken in tokens:
            eachTaggedSentence = nltk.pos_tag(tokens)
            pos_tagged_paragraphs.append(eachTaggedSentence)
        return pos_tagged_paragraphs

if __name__ == '__main__':
    import unittest
    from unitTests import test_detection_functions
    suite = unittest.TestLoader().loadTestsFromTestCase(test_detection_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)
