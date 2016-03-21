from nltk import word_tokenize, pos_tag, RegexpParser, Tree


class Word(object):
    'Understands the atomic composition of letters'
    def __init__(self, word):
        self.text = word[0]
        self.tag = word[1]

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text and self.tag == other.tag)

    def is_verb(self):
        return self.tag[0] == 'V'

    def is_noun(self):
        return self.tag[0] == 'N'

    def is_belief_verb(self):
        beliefVerbs = [
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
            "thought", "think"
        ]
        return (str.lower(self.text) in beliefVerbs and self.is_verb()) is True

    def is_attitude_verb(self):
        attitudeVerbs = [
            "want", "wanted", "wants", "wish",
            "wishes", "wished", "consider", "considers",
            "considered", "desire", "desires", "desired", "hope",
            "hoped", "hopes", "aspire", "aspired", "aspires",
            "fancy", "fancied", "fancies", "care", "cares",
            "cared", "like", "likes", "liked"
        ]
        return str.lower(self.text) in attitudeVerbs and self.is_verb()

    def is_a_being_verb(self):
        isWords = ["is", "was", "were", "are"]
        return str.lower(self.text) in isWords

    def is_belief_nonverb(self):
        beliefNonVerbs = [
            "belief", "beliefs", "knowledge",
            "perception", "perceptions", "memory", "memories",
            "suspicion", "suspicions", "assumption", "assumptions",
            "presupposition", "presuppositions", "suppositions",
            "supposition", "conclusion", "conclusions",
            "understanding", "judgment", "doubt", "doubts"
        ]
        return str.lower(self.text) in beliefNonVerbs and not self.is_verb()

    def is_attitude_nonverb(self):
        attitudeNonVerbs = [
            "desire", "desires", "wants", "want", "wish", "wishes",
            "hope", "hopes", "aspirations", "aspiration", "fancy",
            "fancies", "care", "cares", "longing"
        ]
        return str.lower(self.text) in attitudeNonVerbs and not self.is_verb()

    def __hash__(self):
        return hash(frozenset(self.text))


class Sentence(object):
    'Understands series of words that forms a complete thought'
    def __init__(self, text):
        self.text = text
        tokenList = word_tokenize(text)
        self.POStags = pos_tag(tokenList)
        self.words = []
        for eachWord in self.POStags:
            self.words.append(Word(eachWord))
        self.chunks = []

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text)

    def __hash__(self):
        return hash(frozenset(self.text))

    def contains_belief_verb(self):
        return True in [eachWord.is_belief_verb() for eachWord in self.words]

    def contains_attitude_verb(self):
        return True in [eachWord.is_attitude_verb() for eachWord in self.words]

    def contains_a_being_verb(self):
        return True in [eachWord.is_a_being_verb() for eachWord in self.words]

    def parse_with_grammar(self, grammar):
        self.chunkedSentence = RegexpParser(grammar).parse(self.POStags)
        return self

    def contains_chunk_with_belief_or_attitude_word(self):
        allSubtrees = [x for x in self.chunkedSentence if type(x) == Tree]
        flattenedSubtrees = [x.flatten().leaves() for x in allSubtrees]
        listOfAllWordsInSubtrees = [Word(x) for sublist in flattenedSubtrees for x in sublist]
        return True in [x.is_belief_nonverb() or x.is_attitude_nonverb() for x in listOfAllWordsInSubtrees]


if __name__ == '__main__':
    import unittest
    from unitTests import test_language_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_language_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)
