import spacy
from pattern.en import conjugate, PAST, PRESENT, PROGRESSIVE

nlp = spacy.load('en')

def sentence_present_prog(sent):
  myVerb = conjugate(myUglyName, tense=PRESENT, aspect=PROGRESSIVE)
  sent = re.sub(r'\sVERB\s*',
           ' is ' + myVerb + ' ',
           sent)
  sent = final_sent_polish(sent)
  return sent

def sentence_past(sent):
  myVerb = conjugate(myUglyName, tense=PAST)
  sent = re.sub(r'\sVERB\s*',
           ' ' + myVerb + ' ',
           sent)
  sent = final_sent_polish(sent)
  return sent

class Action(object):
  '''Understands a description of something that someone/something does'''

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

  def why(self, action):
    self.intention = IntWithWhich(action)
    return self.intention


class IntWithWhich(object):
  '''Understands the intent behind an action'''

  def __init__(self, action):
    if type(action) is str or type(action) is unicode:
      self.text = nlp(unicode(action)).sents.next()
    elif type(action) is spacy.tokens.Span:
      self.text = action
    elif type(action) is Action:
      self.text = action.text

  def __eq__(self, other):
    return str(self.text) == str(other.text)


class Predicate(object):
  '''Understands the action or description of a subject in a sentence'''

  def __init__(self, verb):
    self.verb = verb
    
    self.directObjects = [t for t in verb.children if t.dep_ == 'dobj']
    doText = ' '.join(str(t).lower() for dob in self.directObjects for t in dob.subtree)
    
    dativeTrees = [t for t in verb.children if t.dep_ == 'dative']
    dativeText = ' '.join(str(t).lower() for c in dativeTrees for t in c.subtree)
    
    clausalTrees = [t for t in verb.children if t.dep_ == 'xcomp']
    clausalText = ' '.join(str(t).lower() for c in clausalTrees for t in c.subtree)

    adverbTrees = [t for t in verb.children if t.dep_ == 'advmod']
    adverbText = ' '.join(str(t).lower() for c in adverbTrees for t in c.subtree)
    
    auxTokens = [t for t in verb.children if t.dep_ == 'aux']
    auxText = ' '.join(str(t).lower() for t in auxTokens)

    adverbModifierTokens = [t for t in verb.children if t.dep_ == 'npadvmod']
    adverbModifierText = ' '.join(str(t).lower() for c in adverbModifierTokens for t in c.subtree)
    
    predicateTextOrder = filter(None,[auxText, self.verb.text, dativeText, doText, adverbText, clausalText, adverbModifierText])
    self.text = unicode.strip(' '.join(predicateTextOrder))


def tense(text):
  if type(text) is spacy.tokens.doc.Doc:
    text = text.sents.next()
  elif type(text) is unicode or type(text) is str:
    text = nlp(unicode(text)).sents.next()
  tag = text.root.tag_
  if tag == 'VBD' or tag == 'VBN':
    tense = 'past'
  elif tag == 'VBP' or tag == 'VBZ' or tag == 'VBG':
    tense = 'present'
  else:
    aux = [t for t in text if t.tag_ == 'MD']
    if True in [text.root.is_ancestor(t) for t in aux]:
      tense = 'future'
  return tense


if __name__ == '__main__':
    import unittest
    import actionTests
    suite = unittest.TestLoader().loadTestsFromTestCase(actionTests.test_actions)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # while True:
    #   mys = Action(raw_input("Type a sentence: "))
    #   # print(mys.text)
    #   print("Tense: " + str(mys.tense))
    #   print("Subject: " + str(mys.subject))
    #   print("Predicate: " + str(mys.predicate.text))