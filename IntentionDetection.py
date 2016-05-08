# -*- coding: utf-8 -*-


def detect_nonverb_beliefs(sentence):
    ## "(PRP) (belief) is..."
    if sentence.contains_word_type('being', 'verb') is False: return False
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_belief_word()


def detect_nonverb_attitudes(sentence):
    ## "(PRP) (attitude) is..."
    if sentence.contains_word_type('being', 'verb') is False: return False
    grammar = r"""
      IntentionObjectPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_attitude_word()


def detect_intention_using_that_clauses(sentence):
    ## "(VB) that ..."
    if sentence.contains_word('that') is False: return False
    grammar = r"""
      ThatClause: {<VB.|VB><IN>}
    """
    sentence.parse_with_grammar(grammar)
    return sentence.contains_chunk_with_belief_word() or \
        sentence.contains_chunk_with_attitude_word()


def is_sentence_intentional(sentence):
    return sentence.contains_word_type('belief', 'verb') or \
        sentence.contains_word_type('attitude', 'verb') or \
        detect_nonverb_beliefs(sentence) or \
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
