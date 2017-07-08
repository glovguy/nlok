import unittest
from language import *
from invariants.tense import *
from nltk import Tree
from nltk.corpus import verbnet as vn


class test_language_objects(unittest.TestCase):
    def test_comparisons(self):
        self.assertEqual(Word("Coffee", 'NN'), Word("Coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee.").words[3], Word("coffee", 'NN'))
        self.assertEqual(Sentence("I want that coffee."), Sentence("I want that coffee."))
        self.assertEqual(Sentence("I want that coffee."), Sentence("I want that coffee."))

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
        self.assertEqual(Word("Coffee", 'NN').tag, 'NN')

    def test_word_verb_tests(self):
        self.assertEqual(False, Word("Coffee", 'NN').is_type('belief', 'verb'))
        self.assertEqual(True, Word('want', 'VBP').is_type('attitude', 'verb'))
        self.assertEqual(False, Word('want', 'VBP').is_type('belief', 'verb'))
        self.assertEqual(True, Word('think', 'VBP').is_type('belief', 'verb'))
        self.assertEqual(False, Word('think', 'VBP').is_type('attitude', 'verb'))
        self.assertEqual(False, Word('coffee', 'NN').is_type('attitude', 'verb'))
        self.assertEqual(True, Word('think', 'VBP').is_type('belief', 'verb'))

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
        self.assertEqual(True, Word("believe", tag="VB").is_synonym_of(Word("think", tag="VB")))
        self.assertEqual(True, Word("think", tag="VB").is_synonym_of(Word("believe", tag="VB")))
        self.assertEqual(False, Word("cupcake").is_synonym_of(Word("believe")))

    # def test_is_synonym_of_checks_pos(self):
    #     self.assertEqual(False, Word("believe", tag="VB").is_synonym_of(Word("think", tag="NN")))
    #     self.assertEqual(True, Word("believe", tag="VB").is_synonym_of(Word("think")))

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

    # Uses pattern to add grammatical mood to feature set
    def test_sentence_mood_features(self):
        s1 = Sentence("Robert wants some coffee after that meeting.")
        s2 = Sentence("Call her tomorrow.")
        s3 = Sentence("I wish that I were a fast runner.")
        s4 = Sentence("If I feel well, I will sing.")
        self.assertEqual(True, s1.feature_set()['indicative_mood'])
        self.assertEqual(True, s2.feature_set()['imperative_mood'])
        self.assertEqual(False, s2.feature_set()['indicative_mood'])
        self.assertEqual(True, s3.feature_set()['subjunctive_mood'])
        self.assertEqual(True, s4.feature_set()['conditional_mood'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
