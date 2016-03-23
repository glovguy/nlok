import json
import nltk
from language import Sentence, Word, Paragraphs


def detect_nonverb_beliefs_and_attitudes(sentence):
    if sentence.contains_a_being_verb() is False: return False
    ## "(PRP) (belief/attitude) is..."
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_belief_or_attitude_word()


def detect_intention_using_that_clauses(sentence):
    if sentence.contains_word(Word('that')) is False: return False
    ## "(VB) that ..."
    ## First, apply a grammar
    grammar = r"""
      ThatClause: {<VB.|VB><IN>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_phenomenal_word()


def is_sentence_intentional(sentence):
    ############################################################
    ## Returns a sentence when given a word with its location ##
    ############################################################
    return sentence.contains_belief_verb() or \
        sentence.contains_attitude_verb() or \
        detect_nonverb_beliefs_and_attitudes(sentence) or \
        detect_intention_using_that_clauses(sentence)
    raise Exception


# def all_intentional_sentences(rawText):
#     allText = Paragraphs(rawText)
#     pos_tagged_paragraphs = IntentionDetection.pos_tag_each_tokenized_sentence(tokens)
#     for eachParagraph in pos_tagged_paragraphs:
#         print eachParagraph
#         paragraphIntentions = IntentionDetection.DetectIntentions(eachParagraph)
#         if paragraphIntentions != "":
#             print "Intentional Sentences:"
#             print paragraphIntentions
#     print "\n"


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


if __name__ == '__main__':
    import unittest
    from unitTests import test_detection_functions
    suite = unittest.TestLoader().loadTestsFromTestCase(test_detection_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)
