from nltk.corpus import wordnet

class WnSynonyms(object):
    """Understands the interface with Wordnet synsets"""

    def __init__(self, word):
        self.text = word.text
        self.nltkTag = word.tag
        self.wnTag = self.nltk_to_wn(self.nltkTag)
        self.synsets = wordnet.synsets(self.text, pos=self.wnTag)
        self.lemmas = set([w for s in self.synsets for w in s.lemma_names()])

    def __iter__(self):
        return (l for l in self.lemmas)

    @classmethod
    def nltk_to_wn(cls, nltkTag):
        wnTag = nltkTag[0].lower()
        if wnTag == 'j': wnTag = 'a'
        return wnTag
