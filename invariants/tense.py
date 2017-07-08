import sys
from language import Sentence, Word

def tense(word):
    return {
        word.tag in ["VBD", "VBN"]: PastTense,
        word.tag in ["VBP", "VBZ", "VBG"]: PresentTense,
        }.get(True, None)

def modalVerb(word):
    return word.tag == "MD"

def verbTense(sent):
    return {
        PastTense in [w.tense() for w in sent.words]: PastTense,
        PresentTense in [w.tense() for w in sent.words]: PresentTense,
        True in [w.modalVerb() for w in sent.words]: FutureTense,
        }.get(True, None)


class WordTenseBase(object):
    pass

class PastTense(WordTenseBase):
    name = 'past'

class PresentTense(WordTenseBase):
    name = 'present'

class FutureTense(WordTenseBase):
    name = 'future'

wordInvariants = [tense, modalVerb]

class SentenceTenseBase(object):
    pass

class PastTense(SentenceTenseBase):
    name = 'past'

class PresentTense(SentenceTenseBase):
    name = 'present'

class FutureTense(SentenceTenseBase):
    name = 'future'

sentInvariants = [verbTense]


if __name__ != "__main__":
    for inv in wordInvariants:
        setattr(Word, inv.__name__, inv)
    for inv in sentInvariants:
        setattr(Sentence, inv.__name__, inv)
