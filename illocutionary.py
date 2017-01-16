import spacy
from language import tense, load_spacy
from proposition import Predicate

nlp = load_spacy()

class Statement(object):
  '''Understands a description whose propositional content is meant as true'''

  def __init__(self, text):
    doc = nlp(unicode(text))
    self.text = doc.sents.next() # Only stores first full sentence
    self.noun_chunks = doc.noun_chunks
    self.assign_tense()
    self.assign_subject()
    self.assign_predicate()

  def assign_subject(self):
    token = [t for t in self.text.root.children if t.dep_ == 'nsubj'][0]
    self.subject = [c for c in self.noun_chunks if token in c][0]

  def assign_predicate(self):
    self.predicate = Predicate(self.text.root)

  def assign_tense(self):
    self.tense = tense(self.text)

  def __eq__(self, other):
    return str(self.text) == str(other.text)


if __name__ == '__main__':
    import unittest
    import actionTests
    suite = unittest.TestLoader().loadTestsFromTestCase(actionTests.test_actions)
    unittest.TextTestRunner(verbosity=2).run(suite)
