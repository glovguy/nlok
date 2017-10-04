# Natural Language Object Kit

Object wrappers for OO development in nltk.

### Motivation

When exploring the NLTK, I found that it was helpful to create objects to write my code around. This began with the need to have one object contain both a word string as well as its part of speech tag.

Instead of referencing a word's tag with `myword[1]`, now you can write `myword.tag` and `myword[0]` with `myword.text`, which greatly improves readability.

I've added more as I needed things. For more info, please check out the code and the unit tests, as it is fully tested.

### Example

```python
>>> from language import *
>>> mys = Sentence("I wish I had some coffee.")
>>> mys.feature_set()
{'present_tense': True, 'future_tense': False, 'contains_that': False, 'past_tense': True, 'contains_being_verb': False, 'contains_attitude_verb': True, 'contains_belief_verb': False}
>>> myw = mys.words[1]
>>> myw.feature_set()
{'being': False, 'future_tense': False, 'noun': False, 'belief': False, 'attitude': True, 'past_tense': False, 'verb': True, 'present_tense': True, 'nonverb': False}
>>> myw.is_synonym_of("want")  # uses wordnet to determine synonyms
True
```