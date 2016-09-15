# -*- coding: utf-8 -*-
from language import Sentence


def detect_nonverb_beliefs(sentence):
    ## "(PRP) (belief) is..."
    if sentence.contains_word_type('being', 'verb') is False: return False
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    return sentence.contains_grammar_with_word_type(grammar, 'belief')


def detect_nonverb_attitudes(sentence):
    ## "(PRP) (attitude) is..."
    if sentence.contains_word_type('being', 'verb') is False: return False
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    return sentence.contains_grammar_with_word_type(grammar, 'attitude')


def detect_intention_using_that_clauses(sentence):
    ## "(VB) that ..."
    if sentence.contains_word('that') is False: return False
    grammar = r"""
      ThatClause: {<VB.|VB><IN>}
    """
    return sentence.contains_grammar_with_word_type(grammar, 'attitude', 'belief')


def is_sentence_intentional(sentence):
    if sentence.__class__ is not Sentence: sentence = Sentence(sentence)
    return sentence.contains_word_type('attitude', 'verb') or \
        detect_nonverb_attitudes(sentence) or \
        detect_intention_using_that_clauses(sentence)


def sentence_indicates_desire(sentence):
    return sentence.contains_word_type('attitude', 'verb') or \
        detect_nonverb_attitudes(sentence)


def sentence_indicates_belief(sentence):
    return sentence.contains_word_type('desire', 'verb') or \
        detect_nonverb_beliefs(sentence) or \
        detect_intention_using_that_clauses(sentence)


if __name__ == '__main__':
    import unittest
    from unitTests import test_detection_functions
    suite = unittest.TestLoader().loadTestsFromTestCase(test_detection_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)
