import nltk
# -*- coding: utf-8 -*-

## Grab all the words and compute out POS tokens
SiddharthaText = "Siddhartha had started to nurse discontent in himself, he had started to feel that the love of his father and the love of his mother, and also the love of his friend, Govinda, would not bring him joy for ever and ever, would not nurse him, feed him, satisfy him. He had started to suspect that his venerable father and his other teachers, that the wise Brahmans had already revealed to him the most and best of their wisdom, that they had already filled his expecting vessel with their richness, and the vessel was not full, the spirit was not content, the soul was not calm, the heart was not satisfied. The ablutions were good, but they were water, they did not wash off the sin, they did not heal the spirit's thirst, they did not relieve the fear in his heart. The sacrifices and the invocation of the gods were excellent, but was that all? Did the sacrifices give a happy fortune? And what about the gods? Was it really Prajapati who had created the world? Was it not the Atman, He, the only one, the singular one? Were the gods not creations, created like me and you, subject to time, mortal? Was it therefore good, was it right, was it meaningful and the highest occupation to make offerings to the gods? For whom else were offerings to be made, who else was to be worshipped but Him, the only one, the Atman? And where was Atman to be found, where did He reside, where did his eternal heart beat, where else but in one's own self, in its innermost part, in its indestructible part, which everyone had in himself? But where, where was this self, this innermost part, this ultimate part? It was not flesh and bone, it was neither thought nor consciousness, thus the wisest ones taught. So, where, where was it? To reach this place, the self, myself, the Atman, there was another way, which was worthwhile looking for? Alas, and nobody showed this way, nobody knew it, not the father, and not the teachers and wise men, not the holy sacrificial songs! They knew everything, the Brahmans and their holy books, they knew everything, they had taken care of everything and of more than everything, the creation of the world, the origin of speech, of food, of inhaling, of exhaling, the arrangement of the senses, the acts of the gods, they knew infinitely much, but was it valuable to know all of this, not knowing that one and only thing, the most important thing, the solely important thing?"

KafkaText = "The first thing he wanted to do was to get up in peace without being disturbed, to get dressed, and most of all to have his breakfast. Only then would he consider what to do next, as he was well aware that he would not bring his thoughts to any sensible conclusions by lying in bed. He remembered that he had often felt a slight pain in bed, perhaps caused by lying awkwardly, but that had always turned out to be pure imagination and he wondered how his imaginings would slowly resolve themselves today. He did not have the slightest doubt that the change in his voice was nothing more than the first sign of a serious cold, which was an occupational hazard for travelling salesmen."

testText = "Siddhartha entered the chamber, where his father was sitting on a mat of bast, and stepped behind his father and remained standing there, until his father felt that someone was standing behind him. Quoth the Brahman: \'Is that you, Siddhartha? Then say what you came to say.\' Quoth Siddhartha: 'With your permission, my father. I came to tell you that it is my longing to leave your house tomorrow and go to the ascetics. My desire is to become a Samana. May my father not oppose this.\'"

tokens = nltk.word_tokenize(testText)

print "TOKENS"
print tokens

pos_tagged_tokens = nltk.pos_tag(tokens)

print "TAGGED PARAGRAPH"
print pos_tagged_tokens

grammar = "NP: {<DT>?<JJ>*<NN>}"

cp = nltk.RegexpParser(grammar)
result = cp.parse(pos_tagged_tokens)
print "CHUNKED PARAGRAPH"
print result

## Grab all verbs and put them in a list
spot = 0
verbList = []
for tag in pos_tagged_tokens:
    if tag[1][0] == "V":
        verb =  [tag[0], tag[1], spot]
        verbList.append(verb)
    spot += 1

print "VERB LIST"
print verbList


verb = []
lookForThese = ["believe", "believes", "believed", "know", "knows", "knew", "perceive", "perceives", "perceive", "notice", "notices", "noticed", "remember", "remembers", "remembered", "consider", "considers", "considered", "think", "thinks", "thought", "imagine", "imagines", "imagined", "suspect", "suspects", "suppose", "assume", "presume", "surmise", "conclude", "deduce", "understand"]
for verb in verbList:
    for testVerb in lookForThese:
        if verb[0] == testVerb:
            print "MATCH"
            print verb
