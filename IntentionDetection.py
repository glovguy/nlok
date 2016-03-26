# import json
# import nltk
from language import Word
# -*- coding: utf-8 -*-


def detect_nonverb_beliefs_and_attitudes(sentence):
    ## "(PRP) (belief/attitude) is..."
    if sentence.contains_a_being_verb() is False: return False
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_belief_or_attitude_word()


def detect_intention_using_that_clauses(sentence):
    ## "(VB) that ..."
    if sentence.contains_word(Word('that')) is False: return False
    grammar = r"""
      ThatClause: {<VB.|VB><IN>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_phenomenal_word()


def is_sentence_intentional(sentence):
    return sentence.contains_belief_verb() or \
        sentence.contains_attitude_verb() or \
        detect_nonverb_beliefs_and_attitudes(sentence) or \
        detect_intention_using_that_clauses(sentence)
    raise Exception


if __name__ == '__main__':
    import unittest
    from unitTests import test_detection_functions
    suite = unittest.TestLoader().loadTestsFromTestCase(test_detection_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)
