import unittest
from IntentionDetection import *
from IntentionPrompts import *
from language import *


class test_functions_in_IntentionPrompts(unittest.TestCase):
    def test_determine_file_type(self):
        self.assertEqual(determine_file_type("jldsnfkjds.intention"), 'intention')
        self.assertEqual(determine_file_type("intent.n.intention"), 'intention')
        self.assertEqual(determine_file_type("exampleText.txt"), "txt")


class test_language_objects(unittest.TestCase):
    def test_comparisons(self):
        self.assertEqual(Word("Coffee", 'NN'), Word("Coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee.").words[3], Word("coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee."), Sentence("I want that coffee."))

    def test_tags(self):
        self.assertTrue(Sentence("I want that coffee.").words[1].is_verb())
        self.assertEqual(Word("Coffee", 'NN').tag, 'NN')

    def test_word_verb_tests(self):
        self.assertEqual(False, Word("Coffee", 'NN').is_belief_verb())
        self.assertEqual(True, Word('want', 'VBP').is_attitude_verb())
        self.assertEqual(False, Word('want', 'VBP').is_belief_verb())
        self.assertEqual(True, Word('think', 'VBP').is_belief_verb())
        self.assertEqual(False, Word('think', 'VBP').is_attitude_verb())
        self.assertEqual(False, Word('coffee', 'NN').is_attitude_verb())

    def test_word_nonverb_tests(self):
        self.assertEqual(False, Word("Coffee", 'NN').is_belief_nonverb())
        self.assertEqual(True, Word('Wants', 'NN').is_attitude_nonverb())
        self.assertEqual(False, Word('Wants', 'NN').is_belief_nonverb())
        self.assertEqual(True, Word('Belief', 'NN').is_belief_nonverb())
        self.assertEqual(False, Word('think', 'VBP').is_attitude_nonverb())
        self.assertEqual(False, Word('coffee', 'NN').is_attitude_nonverb())

    def test_contains_belief_verb(self):
        self.assertEqual(False, Sentence("I want that coffee.").contains_belief_verb())
        self.assertEqual(True, Sentence("I think that coffee is good.").contains_belief_verb())

    def test_contains_attitude_verb(self):
        self.assertEqual(True, Sentence("I want that coffee.").contains_attitude_verb())
        self.assertEqual(False, Sentence("I think that coffee is good.").contains_attitude_verb())

    def test_contains_a_being_verb(self):
        self.assertEqual(True, Sentence("That is some delicious coffee.").contains_a_being_verb())
        self.assertEqual(False, Sentence("I don't want that much coffee.").contains_a_being_verb())

    def test_parse_with_grammar(self):
        grammar = r"""
          NP: {<DT|PP\$>?<JJ>*<NN>}
        """
        mys = Sentence("Rapunzel let down her long golden hair.").parse_with_grammar(grammar)
        self.assertEqual(('long', 'JJ'), mys.chunkedSentence[4][0])
        self.assertEqual(Tree, type(mys.chunkedSentence[4]))


class test_detection_functions(unittest.TestCase):
    def test_detect_nonverb_beliefs_and_attitudes(self):
        s1 = Sentence('My belief is that this coffee is the best in Manhattan.')
        s2 = Sentence('My dog is very obedient.')
        self.assertEqual(True, detect_nonverb_beliefs_and_attitudes(s1))
        self.assertEqual(False, detect_nonverb_beliefs_and_attitudes(s2))

    def test_detect_intention_using_that_clauses(self):
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        self.assertEqual(True, detect_intention_using_that_clauses(s4))

#     def test_each_function_returns_correct_file_type(self):
#         testText = """ljkndf gnkjfdg fdgdflkngdfgfdlkgf.gd dlkgdfg[fdg\
#         klfdg fglk.g,fd/,gdfgpojdfg lmdfg ,./dfg,/ dsf';dsff;'f\
#         Hotdogs\
#         """
#         returnedValue1 = detect_verb_beliefs_and_attitudes(testText)
#         returnedValue2 = detect_nonverb_beliefs_and_attitudes(testText)
#         self.assertEqual(type(returnedValue1), type(['', 1]))
#         self.assertEqual(type(returnedValue2), type(['', 1]))

    def test_is_sentence_intentional(self):
        s1 = Sentence('"How deaf and stupid have I been!" he thought, walking swiftly along.')
        s2 = Sentence("This is a sentence that doesn't express intention.")
        s3 = Sentence('I want this sentence to express intention..')
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        self.assertEqual(True, is_sentence_intentional(s1))
        self.assertEqual(False, is_sentence_intentional(s2))
        self.assertEqual(True, is_sentence_intentional(s3))
        self.assertEqual(True, is_sentence_intentional(s4))

#     def test_count_sentences(self):
#         unitTestText = """
#         "How deaf and stupid have I been!" he thought, walking swiftly along. "When someone reads a text,\
#          wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions,\
#          coincidence, and worthless hull, but he will read them, he will study and love them, letter by\
#          letter. But I, who wanted to read the book of the world and the book of my own being, I have,\
#          for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I\
#          called the visible world a deception, called my eyes and my tongue coincidental and worthless forms\
#          without substance. No, this is over, I have awakened, I have indeed awakened and have not been born\
#          before this very day."
#         This is a sentence that doesn't express intention. I want this sentence to express intention..
#         He started to feel that that was enough coffee for today.
#         """

#         density = []
#         for eachParagraph in unitTestText:
#             print eachParagraph
#             if len(eachParagraph) > 0 and eachParagraph != "\n":
#                 sentenceMarkers = countSentences(eachParagraph, returnMarkers=True)
#                 wordlist = DetectIntentions(eachParagraph)
#                 print sentenceMarkers
#                 print wordlist
#                 for eachSentence in range(len(sentenceMarkers)):
#                     thisDensity = 0
#                     for eachWord in wordlist:
#                         if (eachWord[2] > sentenceMarkers[eachSentence-1] or eachSentence == 0) and eachWord[2] < sentenceMarkers[eachSentence]:
#                             thisDensity += 1
#                     density.append(thisDensity)
#         print density
#         self.assertTrue

if __name__ == '__main__':
    unittest.main(verbosity=1)
