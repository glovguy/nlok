import unittest
from IntentionDetection import *
from IntentionPrompts import *
from language import *
from nltk import Tree


class test_functions_in_IntentionPrompts(unittest.TestCase):
    def test_determine_file_type(self):
        self.assertEqual(determine_file_type("jldsnfkjds.json"), 'json')
        self.assertEqual(determine_file_type("intent.n.json"), 'json')
        self.assertEqual(determine_file_type("exampleText.txt"), "txt")


class test_language_objects(unittest.TestCase):
    def test_comparisons(self):
        self.assertEqual(Word("Coffee", 'NN'), Word("Coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee.").words[3], Word("coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee."), Sentence("I want that coffee."))
        self.assertEqual(Sentence("I want that coffee."), Sentence(u"I want that coffee."))

    def test_string_conversions(self):
        p1 = Passage("I like coffee. I also like listening to music.")
        s1 = Sentence("I like coffee.")
        w1 = Word("fancy")
        self.assertEqual(str(p1), "I like coffee. I also like listening to music.")
        self.assertEqual(str(s1), "I like coffee.")
        self.assertEqual(str(w1), "fancy")

    def test_tags(self):
        self.assertTrue(Sentence("I want that coffee.").words[1].is_type('verb'))
        self.assertEqual(Word("Coffee", 'NN').tag, 'NN')
        self.assertEqual(Word(u"Coffee", u'NN').tag, u'NN')

    def test_word_verb_tests(self):
        self.assertEqual(False, Word("Coffee", 'NN').is_type('belief', 'verb'))
        self.assertEqual(True, Word('want', 'VBP').is_type('attitude', 'verb'))
        self.assertEqual(False, Word('want', 'VBP').is_type('belief', 'verb'))
        self.assertEqual(True, Word('think', 'VBP').is_type('belief', 'verb'))
        self.assertEqual(False, Word('think', 'VBP').is_type('attitude', 'verb'))
        self.assertEqual(False, Word('coffee', 'NN').is_type('attitude', 'verb'))
        self.assertEqual(True, Word(u'think', u'VBP').is_type('belief', 'verb'))

    def test_word_nonverb_tests(self):
        self.assertEqual(False, Word("Coffee", 'NN').is_type('belief', 'nonverb'))
        self.assertEqual(True, Word('Wants', 'NN').is_type('attitude', 'nonverb'))
        self.assertEqual(False, Word('Wants', 'NN').is_type('belief', 'nonverb'))
        self.assertEqual(True, Word('Belief', 'NN').is_type('belief', 'nonverb'))
        self.assertEqual(False, Word('think', 'VBP').is_type('attitude', 'nonverb'))
        self.assertEqual(False, Word('coffee', 'NN').is_type('attitude', 'nonverb'))

    def test_contains_belief_verb(self):
        self.assertEqual(False, Sentence("I want that coffee.").contains_word_type('belief', 'verb'))
        self.assertEqual(True, Sentence("I think that coffee is good.").contains_word_type('belief', 'verb'))

    def test_contains_attitude_verb(self):
        self.assertEqual(True, Sentence("I want that coffee.").contains_word_type('attitude', 'verb'))
        self.assertEqual(False, Sentence("I think that coffee is good.").contains_word_type('attitude', 'verb'))

    def test_contains_a_being_verb(self):
        self.assertEqual(True, Sentence("That is some delicious coffee.").contains_word_type('being', 'verb'))
        self.assertEqual(False, Sentence("I don't want that much coffee.").contains_word_type('being', 'verb'))

    def test_tense_feature(self):
        self.assertEqual(True, Word("wanted").is_type("past_tense"))
        self.assertEqual(False, Word("wants").is_type("past_tense"))
        self.assertEqual(True, Word("wants").is_type("present_tense"))
        self.assertEqual(True, Sentence("I am eating.").feature_set()['present_tense'])
        self.assertEqual(False, Sentence("I am eating.").feature_set()['past_tense'])
        self.assertEqual(True, Sentence("I ran earlier today.").feature_set()['past_tense'])
        self.assertEqual(False, Sentence("I ran earlier today.").feature_set()['present_tense'])
        self.assertEqual(True, Sentence("I will eat later after 7pm.").feature_set()['future_tense'])
        self.assertEqual(False, Sentence("I will eat later after 7pm.").feature_set()['past_tense'])

    def test_words_of_type(self):
        self.assertEqual([Word("want")], Sentence("I want coffee.").words_of_type('verb'))

    def test_is_synonym_of(self):
        self.assertEqual(True, Word("believe").is_synonym_of(Word("think")))
        self.assertEqual(True, Word("think").is_synonym_of(Word("believe")))
        self.assertEqual(False, Word("cupcake").is_synonym_of(Word("believe")))

    def test_parse_with_grammar(self):
        grammar = r"""
          NP: {<DT|PP\$>?<JJ>*<NN>}
        """
        mys = Sentence("Rapunzel let down her long golden hair.").parse_with_grammar(grammar)
        self.assertEqual(('long', 'JJ'), mys.chunkedSentence[4][0])
        self.assertEqual(Tree, type(mys.chunkedSentence[4]))

    def test_paragraph_init(self):
        p1 = Passage("I like coffee. I also like listening to music.")
        s1 = Sentence("I like coffee.")
        s2 = Sentence("I also like listening to music.")
        self.assertEqual(p1.sentences, [s1, s2])

    def test_count_sentences(self):
        p1 = Passage("""But I, who wanted to read the book of the world and the book of my own being, I have,\
         for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I\
         called the visible world a deception, called my eyes and my tongue coincidental and worthless forms\
         without substance. No, this is over, I have awakened, I have indeed awakened and have not been born\
         before this very day."
        This is a sentence that doesn't express intention. I want this sentence to express intention..
        He started to feel that that was enough coffee for today.""")
        self.assertEqual(p1.count_sentences(), 5)

    def test_intentional_sentences_density(self):
        p1 = Passage("""But I, who wanted to read the book of the world and the book of my own being, I have,\
         for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I
         called the visible world a deception, called my eyes and my tongue coincidental and worthless forms
         without substance. No, this is over, I have awakened, I have indeed awakened and have not been born
         before this very day."
        This is a sentence that doesn't express intention. I want this sentence to express intention..
        He started to feel that that was enough coffee for today.""")
        self.assertEqual(p1.sentence_density_of_type(is_sentence_intentional), [True, False, False, True, True])

    def test_feature_set(self):
        s1 = Sentence("It is raining today.")
        s2 = Sentence("I also like listening to music.")
        self.assertEqual(True, s1.feature_set()['contains_being_verb'])
        self.assertEqual(False, s1.feature_set()['contains_that'])
        self.assertEqual(True, s2.feature_set()['present_tense'])

    def test_contains_grammar_with_word_type(self):
        grammar = r"""
            Test: {<VB.|VB>}
          """
        mys = Sentence("Rapunzel let down her long golden hair.").parse_with_grammar(grammar)
        noParse = Sentence("This sentence will not be parsed.")
        self.assertEqual(True, mys.contains_grammar_with_word_type(grammar, 'verb'))
        self.assertEqual(False, noParse.contains_grammar_with_word_type(grammar, 'attitude'))


class test_detection_functions(unittest.TestCase):
    def test_detect_nonverb_beliefs_and_attitudes(self):
        s1 = Sentence('My belief is that this coffee is the best in Manhattan.')
        s2 = Sentence('My dog is very obedient.')
        s3 = Sentence('My desire is to become a Samana.')
        self.assertEqual(True, detect_nonverb_beliefs(s1))
        self.assertEqual(False, detect_nonverb_attitudes(s1))
        self.assertEqual(False, detect_nonverb_beliefs(s2))
        self.assertEqual(True, detect_nonverb_attitudes(s3))
        self.assertEqual(False, detect_nonverb_beliefs(s3))

    def test_detect_intention_using_that_clauses(self):
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence('I think that you are mistaken.')
        self.assertEqual(True, detect_intention_using_that_clauses(s4))
        self.assertEqual(True, detect_intention_using_that_clauses(s5))

    def test_is_sentence_intentional(self):
        s1 = Sentence('"How deaf and stupid have I been!" he thought, walking swiftly along.')
        s2 = Sentence("This is a sentence that doesn't express intention.")
        s3 = Sentence('I want this sentence to express intention..')
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence(u'I want this sentence to express intention..')
        self.assertEqual(False, is_sentence_intentional(s1))
        self.assertEqual(False, is_sentence_intentional(s2))
        self.assertEqual(True, is_sentence_intentional(s3))
        self.assertEqual(True, is_sentence_intentional(s4))
        self.assertEqual(True, is_sentence_intentional(s5))
        self.assertEqual(True, is_sentence_intentional(str('I want this.')))
        self.assertEqual(True, is_sentence_intentional(u'I want this.'))

    def test_all_intentional_sentences(self):
        p1 = Passage(u'''
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
        ''')
        s1 = Sentence("I want this sentence to express intention..")
        s2 = Sentence("He started to feel that that was enough coffee for today.")
        s3 = Sentence(u'''"When someone reads a text,\
wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions,\
coincidence, and worthless hull, but he will read them, he will study and love them, letter by\
letter.''')
        self.assertTrue(s1 in p1.all_sentences_of_type(is_sentence_intentional))
        self.assertTrue(s2 in p1.all_sentences_of_type(is_sentence_intentional))
        self.assertTrue(s3 in p1.all_sentences_of_type(is_sentence_intentional))

    def test_detect_desire(self):
        s1 = Sentence('"How deaf and stupid have I been!" he thought, walking swiftly along.')
        s2 = Sentence("This is a sentence that doesn't express intention.")
        s3 = Sentence('I want this sentence to express intention..')
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence(u'I want this sentence to express intention..')
        self.assertEqual(False, sentence_indicates_desire(s1))
        self.assertEqual(False, sentence_indicates_desire(s2))
        self.assertEqual(True, sentence_indicates_desire(s3))
        self.assertEqual(True, sentence_indicates_desire(s4))
        self.assertEqual(True, sentence_indicates_desire(s5))


# class test_significance_objects(unittest.TestCase):
#     def test_intensional_set_definition(self):
#         self.assertEqual(True, Sentence("I want coffee.") in IntentionalSentences)
#         self.assertEqual(False, Sentence("It's nice out.") in IntentionalSentences)


if __name__ == '__main__':
    unittest.main(verbosity=1)
