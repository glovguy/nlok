import unittest
from time import time
print("Loading Spacy...")
t1 = time()
from actions import *
t2 = time()
print("Done in " + str(t2-t1) + " seconds")


class test_actions(unittest.TestCase):
    def test_comparisons(self):
        self.assertEqual(Action("He operated the pump"), Action("He operated the pump"))
        self.assertNotEqual(Action("I operated the pump"), Action("He operated the pump"))
        self.assertEqual(IntWithWhich("He is replacing the water"), IntWithWhich("He is replacing the water"))
        
    def test_action_intention_with_which(self):
        act1 = Action("He operated the pump")
        act2 = Action("He is replacing the water")
        int1 = IntWithWhich(act2.text)
        self.assertEqual(act1.why(act2.text), int1)

    def test_action_tense(self):
        act1 = Action("He operated the pump")
        act2 = Action("He will operate the pump")
        act3 = Action("He operates the pump")
        act4 = Action("He is operating the pump")
        self.assertEqual(act1.tense, 'past')
        self.assertEqual(act2.tense, 'future')
        self.assertEqual(act3.tense, 'present')
        self.assertEqual(act4.tense, 'present')

    def test_action_subject(self):
        act1 = Action("He operated the pump")
        act2 = Action("The mayor operated the pump")
        self.assertEqual(act1.subject.text, "He")
        self.assertEqual(act2.subject.text, "The mayor")

    def test_assign_predicate(self):
        act1 = Action("He operated the pump")
        act2 = Action("The mayor operated the pump")
        self.assertEqual(act1.predicate.text, "operated the pump")
        self.assertEqual(act1.predicate.text, act2.predicate.text)
        
    def test_aux_in_predicate(self):
        act3 = Action("He is replacing the water")
        self.assertEqual(act3.predicate.text, "is replacing the water")

    def test_adverb_in_predicate(self):
        act4 = Action("Sam smoked habitually")
        self.assertEqual(act4.predicate.text, "smoked habitually")

    def test_clausal_complement_in_predicate(self):
        act5 = Action("Roger told me to bake him a cake tomorrow")
        self.assertEqual(act5.predicate.text, "told me to bake him a cake tomorrow")

    def test_nounphrase_adverb_modifier_in_predicate(self):
        act6 = Action("Tomorrow afternoon, my family will give me a call.")
        self.assertEqual(act6.predicate.text, "will give me a call tomorrow afternoon")


if __name__ == '__main__':
    unittest.main(verbosity=1)
