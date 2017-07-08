from language import Sentence, Word

def Tense(word):
    return {
        word.tag in ["VBD", "VBN"]: PastTense,
        word.tag in ["VBP", "VBZ", "VBG"]: PresentTense,
        }.get(True, None)

def ModalVerb(word):
    return word.tag == "MD"

def VerbTense(sent):
    return {
        PastTense in [w.Tense() for w in sent.words]: PastTense,
        PresentTense in [w.Tense() for w in sent.words]: PresentTense,
        True in [w.ModalVerb() for w in sent.words]: FutureTense,
        }.get(True, None)


class TenseBase(object):
    pass

class PastTense(TenseBase):
    name = 'past'

class PresentTense(TenseBase):
    name = 'present'

class FutureTense(TenseBase):
    name = 'future'


if __name__ != "__main__":
    wordInvariants = [Tense, ModalVerb]
    for inv in wordInvariants:
        setattr(Word, inv.__name__, inv)
    sentInvariants = [VerbTense]
    for inv in sentInvariants:
        setattr(Sentence, inv.__name__, inv)
