from nltk import word_tokenize, pos_tag


class Tag(object):
    'Understands part of speech for words'
    def __init__(self, label):
        self.label = label

    def is_verb(self):
        return self.label[0] == 'V'

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.label == other.label)

    def __hash__(self):
        return hash(frozenset(self.label))


class Word(object):
    'Understands the atomic composition of letters'
    def __init__(self, word):
        self.text = word[0]
        self.tag = Tag(word[1])

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text and self.tag == other.tag)

    def __hash__(self):
        return hash(frozenset(self.text))


class Sentence(object):
    'Understands series of words that forms a complete thought'
    def __init__(self, text):
        self.text = text
        tokenList = word_tokenize(text)
        POStags = pos_tag(tokenList)
        self.wordList = []
        for eachWord in POStags:
            self.wordList.append(Word(eachWord))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.text == other.text)

    def __hash__(self):
        return hash(frozenset(self.text))

if __name__ == '__main__':
    import unittest
    from unitTests import test_language_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_language_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # mySentence = Sentence("I want that coffee.")
    # print mySentence.text
    # print mySentence.wordList[2].text
