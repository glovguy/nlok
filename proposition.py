

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