import unittest
from IntentionDetection import *
from IntentionDetection import *


class test_functions_in_IntentionPrompts(unittest.TestCase):
    def test_determine_file_type(self):
        # from IntentionPrompts import determine_file_type
        self.assertEqual(determine_file_type("jldsnfkjds.intention"), 'intention')
        self.assertEqual(determine_file_type("intent.n.intention"), 'intention')
        self.assertEqual(determine_file_type("exampleText.txt"), "txt")


class test_language_objects(unittest.TestCase):
    def test_sentence(self):
        self.assertEqual

class test_detection_functions(unittest.TestCase):
    def test_each_function_returns_correct_file_type(self):
        testText = """ljkndf gnkjfdg fdgdflkngdfgfdlkgf.gd dlkgdfg[fdg\
        klfdg fglk.g,fd/,gdfgpojdfg lmdfg ,./dfg,/ dsf';dsff;'f\
        Hotdogs\
        """
        returnedValue1 = detect_verb_beliefs_and_attitudes(testText)
        returnedValue2 = detect_nonverb_beliefs_and_attitudes(testText)
        self.assertEqual(type(returnedValue1), type(['', 1]))
        self.assertEqual(type(returnedValue2), type(['', 1]))

    def test_detect_verb_beliefs_and_attitudes(self):
        test1 = '"How deaf and stupid have I been!" he thought, walking swiftly along.'
        returnedValue1 = detect_verb_beliefs_and_attitudes(test1)
        self.assertEqual(returnedValue1[1], [1])

    def test_count_sentences(self):
        unitTestText = """
        "How deaf and stupid have I been!" he thought, walking swiftly along. "When someone reads a text,\
         wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions,\
         coincidence, and worthless hull, but he will read them, he will study and love them, letter by\
         letter. But I, who wanted to read the book of the world and the book of my own being, I have,\
         for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I\
         called the visible world a deception, called my eyes and my tongue coincidental and worthless forms\
         without substance. No, this is over, I have awakened, I have indeed awakened and have not been born\
         before this very day."
        This is a sentence that doesn't express intention. I want this sentence to express intention..
        He started to feel that that was enough coffee for today.
        """

        density = []
        for eachParagraph in unitTestText:
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
        self.assertTrue
