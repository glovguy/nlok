from intensional import Any, Every
from intensional import Test as With

class Literal(object):
	"""Understands the literal interpretation of a sentence"""

	def __init__(self):
		pass


setOfAllWords = [
    "believe", "believes", "believed", "believing",
    "know", "knows", "knew", "knowing", "perceive",
    "perceives", "perceive", "perceiving", "notice",
    "notices", "noticed", "noticing", "remember",
    "remembers", "remembered", "remembering",
    "imagine", "imagines", "imagined", "imagining",
    "suspect", "suspects", "suppose", "suspecting",
    "assume", "presume", "surmise", "conclude",
    "deduce", "understand", "understands",
    "understood", "understanding", "judge", "doubt",
    "thought", "think", "belief", "beliefs", "knowledge",
    "perception", "perceptions", "memory", "memories",
    "suspicion", "suspicions", "assumption", "assumptions",
    "presupposition", "presuppositions", "suppositions",
    "supposition", "conclusion", "conclusions",
    "understanding", "judgment", "doubt", "doubts",
    "thought", "think", "thought"
]

ATTITUDE_WORDS = [
    "want", "wanted", "wants", "wish",
    "wishes", "wished", "consider", "considers",
    "considered", "desire", "desires", "desired", "hope",
    "hoped", "hopes", "aspire", "aspired", "aspires",
    "fancy", "fancied", "fancies", "care", "cares",
    "cared", "like", "likes", "liked", "longing",
    "desire", "desires", "wants", "want", "wish", "wishes",
    "hope", "hopes", "aspirations", "aspiration", "fancy",
    "fancies", "care", "cares", "feel", "feels", "felt"
]

BEING_WORDS = ["is", "was", "were", "are"]


sentence_contains_attitude_verb = With(
	"x.contains_word_type('attitude', 'verb')"
	)
nounPhrase = r"""
  nounPhrase: {<DT|PRP\$|NNP><JJ>*<NN><VB.|VB>}
"""
sentence_contains_attitude_in_noun_phrase = With(
	"x.contains_grammar_with_word_type(nounPhrase, 'attitude')"
	)
thatClause = r"""
  thatClause: {<VB.|VB><IN>}
"""
sentence_contains_that_clause_with_attitude_or_belief = With(
	"sentence.contains_grammar_with_word_type(thatClause, 'attitude', 'belief')"
	)
IntentionalSentences = Any(sentence_contains_attitude_verb,
	sentence_contains_attitude_in_noun_phrase,
	sentence_contains_that_clause_with_attitude_or_belief)


if __name__ == '__main__':
    import unittest
    from unitTests import test_significance_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_significance_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)