from collections import namedtuple
from language import Sentence, Word

def tense(word):
    return {
        word.tag in ["VBD", "VBN"]: PAST_TENSE_WORD,
        word.tag in ["VBP", "VBZ", "VBG"]: PRESENT_TENSE_WORD,
        }.get(True, None)

def modalVerb(word):
    return word.tag == "MD"

def verbTense(sent):
    return {
        PAST_TENSE_WORD in [w.tense() for w in sent.words]: PAST_TENSE_SENTENCE,
        PRESENT_TENSE_WORD in [w.tense() for w in sent.words]: PRESENT_TENSE_SENTENCE,
        True in [w.modalVerb() for w in sent.words]: FUTURE_TENSE_SENTENCE,
        }.get(True, None)

WordTenseBase = namedtuple('WordTenseBase', 'name')
PAST_TENSE_WORD = WordTenseBase('past')
PRESENT_TENSE_WORD = WordTenseBase('present')
FUTURE_TENSE_WORD = WordTenseBase('future')

SentenceTenseBase = namedtuple('WordTenseBase', 'name')
PAST_TENSE_SENTENCE = SentenceTenseBase('past')
PRESENT_TENSE_SENTENCE = SentenceTenseBase('present')
FUTURE_TENSE_SENTENCE = SentenceTenseBase('future')


if __name__ != "__main__":
    wordInvariants = [tense, modalVerb]
    sentInvariants = [verbTense]
    for inv in wordInvariants:
        setattr(Word, inv.__name__, inv)
    for inv in sentInvariants:
        setattr(Sentence, inv.__name__, inv)
