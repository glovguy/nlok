import nltk
# -*- coding: utf-8 -*-

## Grab all the words and compute out POS tokens
SiddharthaText = "Siddhartha had started to nurse discontent in himself, he had started to feel that the love of his father and the love of his mother, and also the love of his friend, Govinda, would not bring him joy for ever and ever, would not nurse him, feed him, satisfy him. He had started to suspect that his venerable father and his other teachers, that the wise Brahmans had already revealed to him the most and best of their wisdom, that they had already filled his expecting vessel with their richness, and the vessel was not full, the spirit was not content, the soul was not calm, the heart was not satisfied. The ablutions were good, but they were water, they did not wash off the sin, they did not heal the spirit's thirst, they did not relieve the fear in his heart. The sacrifices and the invocation of the gods were excellent, but was that all? Did the sacrifices give a happy fortune? And what about the gods? Was it really Prajapati who had created the world? Was it not the Atman, He, the only one, the singular one? Were the gods not creations, created like me and you, subject to time, mortal? Was it therefore good, was it right, was it meaningful and the highest occupation to make offerings to the gods? For whom else were offerings to be made, who else was to be worshipped but Him, the only one, the Atman? And where was Atman to be found, where did He reside, where did his eternal heart beat, where else but in one's own self, in its innermost part, in its indestructible part, which everyone had in himself? But where, where was this self, this innermost part, this ultimate part? It was not flesh and bone, it was neither thought nor consciousness, thus the wisest ones taught. So, where, where was it? To reach this place, the self, myself, the Atman, there was another way, which was worthwhile looking for? Alas, and nobody showed this way, nobody knew it, not the father, and not the teachers and wise men, not the holy sacrificial songs! They knew everything, the Brahmans and their holy books, they knew everything, they had taken care of everything and of more than everything, the creation of the world, the origin of speech, of food, of inhaling, of exhaling, the arrangement of the senses, the acts of the gods, they knew infinitely much, but was it valuable to know all of this, not knowing that one and only thing, the most important thing, the solely important thing?"

KafkaText = "The first thing he wanted to do was to get up in peace without being disturbed, to get dressed, and most of all to have his breakfast. Only then would he consider what to do next, as he was well aware that he would not bring his thoughts to any sensible conclusions by lying in bed. He remembered that he had often felt a slight pain in bed, perhaps caused by lying awkwardly, but that had always turned out to be pure imagination and he wondered how his imaginings would slowly resolve themselves today. He did not have the slightest doubt that the change in his voice was nothing more than the first sign of a serious cold, which was an occupational hazard for travelling salesmen."

testText = "Siddhartha entered the chamber, where his father was sitting on a mat of bast, and stepped behind his father and remained standing there, until his father felt that someone was standing behind him. Quoth the Brahman: \'Is that you, Siddhartha? Then say what you came to say.\' Quoth Siddhartha: 'With your permission, my father. I came to tell you that it is my longing to leave your house tomorrow and go to the ascetics. My desire is to become a Samana. May my father not oppose this.\'"

BenFranklinText = "About this time I met with an odd volume of the Spectator. It was the third. I had never before seen any of them. I bought it, read it over and over, and was much delighted with it. I thought the writing excellent, and wished, if possible, to imitate it. With this view I took some of the papers, and, making short hints of the sentiment in each sentence, laid them by a few days, and then, without looking at the book, try'd to compleat the papers again, by expressing each hinted sentiment at length, and as fully as it had been expressed before, in any suitable words that should come to hand. Then I compared my Spectator with the original, discovered some of my faults, and corrected them. But I found I wanted a stock of words, or a readiness in recollecting and using them, which I thought I should have acquired before that time if I had gone on making verses; since the continual occasion for words of the same import, but of different length, to suit the measure, or of different sound for the rhyme, would have laid me under a constant necessity of searching for variety, and also have tended to fix that variety in my mind, and make me master of it. Therefore I took some of the tales and turned them into verse; and, after a time, when I had pretty well forgotten the prose, turned them back again. I also sometimes jumbled my collections of hints into confusion, and after some weeks endeavored to reduce them into the best order, before I began to form the full sentences and compleat the paper. This was to teach me method in the arrangement of thoughts. By comparing my work afterwards with the original, I discovered many faults and amended them; but I sometimes had the pleasure of fancying that, in certain particulars of small import, I had been lucky enough to improve the method of the language, and this encouraged me to think I might possibly in time come to be a tolerable English writer, of which I was extremely ambitious. My time for these exercises and for reading was at night, after work or before it began in the morning, or on Sundays, when I contrived to be in the printing-house alone, evading as much as I could the common attendance on public worship which my father used to exact of me when I was under his care, and which indeed I still thought a duty, thought I could not, as it seemed to me, afford time to practise it."

tokens = nltk.word_tokenize(BenFranklinText)

#print "TOKENS"
#print tokens

pos_tagged_tokens = nltk.pos_tag(tokens)

print "TAGGED PARAGRAPH"
print pos_tagged_tokens

# This is a test for chunking. Not working yet.
#grammar = "NP: {<DT>?<JJ>*<NN>}"
#cp = nltk.RegexpParser(grammar)
#result = cp.parse(pos_tagged_tokens)
#print "CHUNKED PARAGRAPH"
#print result

## Grab all verbs and put them in a list
spot = 0
verbList = []
for tag in pos_tagged_tokens:
    if tag[1][0] == "V":
        verb =  [tag[0], tag[1], spot]
        verbList.append(verb)
    spot += 1

#print "VERB LIST"
#print verbList

def ReturnSentece(word):
    # This function prints a sentence when given a word with its location in the tokens list.
    # it searches on either side for closing punctuation
    
    # Find where the sentence starts
    startDisp = 0
    while tokens[word[2]+startDisp][0] != "." and tokens[word[2]+startDisp][0] != ";" and tokens[word[2]+startDisp][0] != "!" and tokens[word[2]+startDisp][0] != "?":
        startDisp = startDisp - 1
    startDisp = startDisp + 1
    
    # Find where the sentence ends
    endDisp = 0
    while tokens[word[2]+endDisp][0] != "." and tokens[word[2]+endDisp][0] != ";" and tokens[word[2]+endDisp][0] != "!" and tokens[word[2]+endDisp][0] != "?":
        endDisp = endDisp + 1
    endDisp = endDisp + 1
    
    # Smash the sentence together into a human-readable string
    sentence = []
    for i in range(endDisp - startDisp):
        sentence.append(tokens[word[2]+startDisp+i])
    sentence = ' '.join(sentence)
    
    # The above process adds unnecessary spaces before punctuation.
    # Let's remove those.
    sentence = sentence.replace(" .", ".")
    sentence = sentence.replace(" ,", ",")
    sentence = sentence.replace(" !", "!")
    sentence = sentence.replace(" ;", ";")
    sentence = sentence.replace(" :", ":")
    sentence = sentence.replace(" ?", "?")
    
    return sentence
    


verb = []
beliefWords = ["believe", "believes", "believed", "know", "knows", "knew", "perceive", "perceives", "perceive", "notice", "notices", "noticed", "remember", "remembers", "remembered", "consider", "considers", "considered", "think", "thinks", "thought", "imagine", "imagines", "imagined", "suspect", "suspects", "suppose", "assume", "presume", "surmise", "conclude", "deduce", "understand, judge, doubt"]

for verb in verbList:
    for testVerb in beliefWords:
        if verb[0] == testVerb:
            print "BELIEF"
            print verb
            print ReturnSentece(verb)

attitudeWords = ["want", "wanted", "wants", "wish", "wishes", "wished", "consider", "considers", "considered", "desire", "desires", "desired", "hope", "hoped", "hopes", "aspire", "aspired", "aspires", "fancy", "fancied", "fancies", "care", "cares", "cared", "like", "likes", "liked"]

verb = []
for verb in verbList:
    for testVerb in attitudeWords:
        if verb[0] == testVerb:
            print "ATTITUDE"
            print verb
            print ReturnSentece(verb)

