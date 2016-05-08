from nltk import word_tokenize, pos_tag, RegexpParser, Tree, data, sent_tokenize
import IntentionDetection
# -*- coding: utf-8 -*-


class Word(object):
    """Understands the atomic composition of letters"""
    def __init__(self, text, tag=None):
        if type(text) == list or type(text) == tuple and tag is None:
            tag = text[1]
            text = text[0]
        self.text = unicode(text)
        self.tag = str(tag)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and unicode.lower(self.text) == unicode.lower(other.text))

    def __str__(self):
        return self.text

    def is_verb(self):
        return self.feature_set()['verb']

    def is_noun(self):
        return self.feature_set()['noun']

    def is_belief_verb(self):
        return self.feature_set()['belief'] and self.feature_set()['verb']

    def is_attitude_verb(self):
        return self.feature_set()['attitude'] and self.feature_set()['verb']

    def is_a_being_verb(self):
        return self.feature_set()['being'] and self.feature_set()['verb']

    def is_belief_nonverb(self):
        return self.feature_set()['belief'] and not self.feature_set()['verb']

    def is_attitude_nonverb(self):
        return self.feature_set()['attitude'] and not self.feature_set()['verb']

    def is_phenomenal_word(self):
        return self.feature_set()['phenomenal']

    def feature_set(self):
        return {
            'verb': self.tag[0] == 'V',
            'noun': self.tag[0] == 'N',
            'belief': unicode.lower(self.text) in BELIEF_WORDS,
            'attitude': unicode.lower(self.text) in ATTITUDE_WORDS,
            'being': unicode.lower(self.text) in BEING_WORDS
        }

    def __hash__(self):
        return hash(frozenset(self.text))


class Sentence(object):
    """Understands series of words that forms a complete thought"""
    def __init__(self, text):
        self.text = unicode(text).strip()
        tokenList = word_tokenize(text)
        self.POStags = pos_tag(tokenList)
        self.words = []
        for eachWord in self.POStags:
            text = eachWord[0]
            tag = eachWord[1]
            self.words.append(Word(text, tag))
        self.chunks = []

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text)

    def __hash__(self):
        return hash(frozenset(self.text))

    def __str__(self):
        return self.text

    def contains_word(self, word):
        return True in [eachWord == word for eachWord in self.words]

    def contains_belief_verb(self):
        return True in [eachWord.is_belief_verb() for eachWord in self.words]

    def contains_attitude_verb(self):
        return True in [eachWord.is_attitude_verb() for eachWord in self.words]

    def contains_a_being_verb(self):
        return True in [eachWord.is_a_being_verb() for eachWord in self.words]

    def contains_a_phenomenal_word(self):
        return True in [eachWord.is_phenomenal_word() for eachWord in self.words]

    def parse_with_grammar(self, grammar):
        self.chunkedSentence = RegexpParser(grammar).parse(self.POStags)
        return self

    def contains_chunk_with_belief_word(self):
        allSubtrees = [x for x in self.chunkedSentence if type(x) == Tree]
        flattenedSubtrees = [x.flatten().leaves() for x in allSubtrees]
        listOfAllWordsInSubtrees = [Word(x) for sublist in flattenedSubtrees for x in sublist]
        return True in [x.is_belief_nonverb() or x.is_belief_verb() for x in listOfAllWordsInSubtrees]

    def contains_chunk_with_attitude_word(self):
        allSubtrees = [x for x in self.chunkedSentence if type(x) == Tree]
        flattenedSubtrees = [x.flatten().leaves() for x in allSubtrees]
        listOfAllWordsInSubtrees = [Word(x) for sublist in flattenedSubtrees for x in sublist]
        return True in [x.is_attitude_nonverb() or x.is_attitude_verb() for x in listOfAllWordsInSubtrees]

    # def contains_chunk_with_phenomenal_word(self):
    #     allSubtrees = [x for x in self.chunkedSentence if type(x) == Tree]
    #     flattenedSubtrees = [x.flatten().leaves() for x in allSubtrees]
    #     listOfAllWordsInSubtrees = [Word(x) for sublist in flattenedSubtrees for x in sublist]
    #     return True in [x.is_phenomenal_word() for x in listOfAllWordsInSubtrees]


class Passage(object):
    """Understands text document that is being analyzed"""
    def __init__(self, text):
        self.text = unicode(text).strip()
        # sentence_detector = data.load('tokenizers/punkt/english.pickle')
        # sentences=nltk.sent_tokenize(sample.decode('utf-8'))
        # -*- coding: utf-8 -*-
        self.sentences = [Sentence(x.strip()) for x in sent_tokenize(text)]
        # sentence_detector.tokenize(text.strip())

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text)

    def __hash__(self):
        return hash(frozenset(self.text))

    def __str__(self):
        return self.text

    def all_intentional_sentences(self):
        return [x for x in self.sentences if IntentionDetection.is_sentence_intentional(x)]

    def count_sentences(self):
        return len(self.sentences)

    def intentional_sentences_density(self):
        return [IntentionDetection.is_sentence_intentional(x) for x in self.sentences]


BELIEF_WORDS = [
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


if __name__ == '__main__':
    import unittest
    from unitTests import test_language_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_language_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)
