from nltk import word_tokenize, pos_tag, RegexpParser, Tree, sent_tokenize
from adaptors.WordnetAdaptor import WnSynonyms


class Word(object):
    """Understands the atomic composition of letters"""
    def __init__(self, text, tag=None):
        if isinstance(text, tuple) or isinstance(text, list) and tag is None:
            tag = text[1]
            text = text[0]
        if tag is None: tag = pos_tag([text])[0][1]
        self.text = text
        self.tag = str(tag)

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
            self.text.lower() == other.text.lower()

    def __hash__(self):
        return hash(self.text)

    def __str__(self):
        return self.text

    def is_type(self, *features):
        if isinstance(features[0], tuple): features = [e for tupl in features for e in tupl]
        return False not in [self.feature_set()[f] for f in features]

    def is_synonym_of(self, other):
        if not isinstance(other, Word): other = Word(other)
        if self.tag != other.tag: return False
        synonyms = WnSynonyms(self)
        return other.text in synonyms

    def feature_set(self):
        return {
            'verb': self.tag[0] == 'V',
            'noun': self.tag[0] == 'N',
            'belief': str.lower(self.text) in BELIEF_WORDS,
            'attitude': str.lower(self.text) in ATTITUDE_WORDS,
            'being': str.lower(self.text) in BEING_WORDS,
            'nonverb': not self.tag[0] == 'V',
        }


class Sentence(object):
    """Understands series of words that forms a complete thought"""
    def __init__(self, text):
        self.text = str(text).strip()
        tokenList = word_tokenize(text)
        self.POStags = pos_tag(tokenList)
        self.words = []
        for eachWord in self.POStags:
            text = eachWord[0]
            tag = eachWord[1]
            self.words.append(Word(text, tag))
        self.chunkedSentence = []

    def __eq__(self, other):
        return isinstance(other, Sentence) and self.text == other.text

    def __hash__(self):
        return hash(frozenset(self.text))

    def __str__(self):
        return self.text

    def contains_word(self, word):
        if not isinstance(word, Word): word = Word(word)
        return True in [eachWord == word for eachWord in self.words]

    def contains_word_type(self, *wordtypes):
        return True in [eachWord.is_type(wordtypes) for eachWord in self.words]

    def words_of_type(self, *wordtypes):
        return [eachWord for eachWord in self.words if eachWord.is_type(wordtypes)]

    def parse_with_grammar(self, grammar):
        self.chunkedSentence = RegexpParser(grammar).parse(self.POStags)
        return self

    def words_in_flattened_tree(self):
        allSubtrees = [x for x in self.chunkedSentence if type(x) == Tree]
        flattenedSubtrees = [x.flatten().leaves() for x in allSubtrees]
        listOfAllWordsInSubtrees = [Word(x) for sublist in flattenedSubtrees for x in sublist]
        return listOfAllWordsInSubtrees

    def contains_grammar_with_word_type(self, grammar, *wordtypes):
        self.parse_with_grammar(grammar)
        listOfAllWordsInSubtrees = self.words_in_flattened_tree()
        return True in [x.is_type(t) for x in listOfAllWordsInSubtrees for t in wordtypes]

    def feature_set(self):
        return {
            'contains_being_verb': self.contains_word_type('being', 'verb'),
            'contains_that': self.contains_word('that'),
            'contains_belief_verb': self.contains_word_type('belief', 'verb'),
            'contains_attitude_verb': self.contains_word_type('attitude', 'verb'),
        }


class Passage(object):
    """Understands text document that is being analyzed"""
    def __init__(self, text):
        self.text = str(text).strip()
        self.sentences = [Sentence(x.strip()) for x in sent_tokenize(text)]

    def __str__(self):
        return self.text

    def all_sentences_of_type(self, sentType):
        return [x for x in self.sentences if sentType(x)]

    def count_sentences(self):
        return len(self.sentences)

    def sentence_density_of_type(self, sentType):
        return [sentType(x) for x in self.sentences]


BELIEF_WORDS = set([
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
])

ATTITUDE_WORDS = set([
    "want", "wanted", "wants", "wish",
    "wishes", "wished", "consider", "considers",
    "considered", "desire", "desires", "desired", "hope",
    "hoped", "hopes", "aspire", "aspired", "aspires",
    "fancy", "fancied", "fancies", "care", "cares",
    "cared", "like", "likes", "liked", "longing",
    "desire", "desires", "wants", "want", "wish", "wishes",
    "hope", "hopes", "aspirations", "aspiration", "fancy",
    "fancies", "care", "cares", "feel", "feels", "felt"
])

BEING_WORDS = set(["is", "was", "were", "are"])


if __name__ == '__main__':
    import unittest
    from unitTests import test_language_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_language_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)
