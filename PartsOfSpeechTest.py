import nltk
# -*- coding: utf-8 -*-

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import re


## Define a function that prints a sentence when given a word with its location in the tokens list.
## Pass it something like ('word', 'tag', number)
## it searches on either side for closing punctuation
def ReturnSentence(word, capitalize = True, taggedVersion = False):
    ## Find where the sentence starts
    startDisp = 0
    while tokens[word[2]+startDisp][0] != "." and tokens[word[2]+startDisp][0] != ";" and tokens[word[2]+startDisp][0] != "!" and tokens[word[2]+startDisp][0] != "?":
        startDisp = startDisp - 1
    startDisp = startDisp + 1
    
    ## Find where the sentence ends
    endDisp = 0
    while tokens[word[2]+endDisp][0] != "." and tokens[word[2]+endDisp][0] != ";" and tokens[word[2]+endDisp][0] != "!" and tokens[word[2]+endDisp][0] != "?":
        endDisp = endDisp + 1
    endDisp = endDisp + 1
    
    ## Smash the sentence together into a human-readable string or isolated tagged sentence
    sentence = []
    if taggedVersion == False:
        for i in range(endDisp - startDisp):
            if startDisp == -i and capitalize == True:
                sentence.append(str.upper(str(tokens[word[2]+startDisp+i])))  # Capitalize the word passed to the function
            else:
                sentence.append(tokens[word[2]+startDisp+i])
        sentence = ' '.join(sentence)
        ## The above process adds unnecessary spaces before punctuation.
        ## Let's remove those.
        sentence = sentence.replace(" .", ".")
        sentence = sentence.replace(" ,", ",")
        sentence = sentence.replace(" !", "!")
        sentence = sentence.replace(" ;", ";")
        sentence = sentence.replace(" :", ":")
        sentence = sentence.replace(" ?", "?")
        sentence = sentence.replace(" 's", "'s")
        sentence = sentence.replace(" 'd", "'d")
        sentence = sentence.replace(" 've", "'ve")
        sentence = sentence.replace(" n't", "n't")
    elif taggedVersion == True:
        for i in range(endDisp - startDisp):
            if startDisp == -i and capitalize == True:
                # Capitalize the word passed to the function
                appendThis = (str.upper(pos_tagged_tokens[word[2]+startDisp+i][0]), pos_tagged_tokens[word[2]+startDisp+i][1])
                sentence.append(appendThis)
            else:
                sentence.append(pos_tagged_tokens[word[2]+startDisp+i])
    
    return sentence


## Grab all the words and compute out POS tokens
SiddharthaText = "Siddhartha had started to nurse discontent in himself, he had started to feel that the love of his father and the love of his mother, and also the love of his friend, Govinda, would not bring him joy for ever and ever, would not nurse him, feed him, satisfy him. He had started to suspect that his venerable father and his other teachers, that the wise Brahmans had already revealed to him the most and best of their wisdom, that they had already filled his expecting vessel with their richness, and the vessel was not full, the spirit was not content, the soul was not calm, the heart was not satisfied. The ablutions were good, but they were water, they did not wash off the sin, they did not heal the spirit's thirst, they did not relieve the fear in his heart. The sacrifices and the invocation of the gods were excellent, but was that all? Did the sacrifices give a happy fortune? And what about the gods? Was it really Prajapati who had created the world? Was it not the Atman, He, the only one, the singular one? Were the gods not creations, created like me and you, subject to time, mortal? Was it therefore good, was it right, was it meaningful and the highest occupation to make offerings to the gods? For whom else were offerings to be made, who else was to be worshipped but Him, the only one, the Atman? And where was Atman to be found, where did He reside, where did his eternal heart beat, where else but in one's own self, in its innermost part, in its indestructible part, which everyone had in himself? But where, where was this self, this innermost part, this ultimate part? It was not flesh and bone, it was neither thought nor consciousness, thus the wisest ones taught. So, where, where was it? To reach this place, the self, myself, the Atman, there was another way, which was worthwhile looking for? Alas, and nobody showed this way, nobody knew it, not the father, and not the teachers and wise men, not the holy sacrificial songs! They knew everything, the Brahmans and their holy books, they knew everything, they had taken care of everything and of more than everything, the creation of the world, the origin of speech, of food, of inhaling, of exhaling, the arrangement of the senses, the acts of the gods, they knew infinitely much, but was it valuable to know all of this, not knowing that one and only thing, the most important thing, the solely important thing?"

KafkaText = "The first thing he wanted to do was to get up in peace without being disturbed, to get dressed, and most of all to have his breakfast. Only then would he consider what to do next, as he was well aware that he would not bring his thoughts to any sensible conclusions by lying in bed. He remembered that he had often felt a slight pain in bed, perhaps caused by lying awkwardly, but that had always turned out to be pure imagination and he wondered how his imaginings would slowly resolve themselves today. He did not have the slightest doubt that the change in his voice was nothing more than the first sign of a serious cold, which was an occupational hazard for travelling salesmen."

SiddharthasIntentionText = "Siddhartha entered the chamber, where his father was sitting on a mat of bast, and stepped behind his father and remained standing there, until his father felt that someone was standing behind him. Quoth the Brahman: 'Is that you, Siddhartha? Then say what you came to say.' Quoth Siddhartha: 'With your permission, my father. I came to tell you that it is my longing to leave your house tomorrow and go to the ascetics. My desire is to become a Samana. May my father not oppose this.'"

BenFranklinText = "About this time I met with an odd volume of the Spectator. It was the third. I had never before seen any of them. I bought it, read it over and over, and was much delighted with it. I thought the writing excellent, and wished, if possible, to imitate it. With this view I took some of the papers, and, making short hints of the sentiment in each sentence, laid them by a few days, and then, without looking at the book, try'd to compleat the papers again, by expressing each hinted sentiment at length, and as fully as it had been expressed before, in any suitable words that should come to hand. Then I compared my Spectator with the original, discovered some of my faults, and corrected them. But I found I wanted a stock of words, or a readiness in recollecting and using them, which I thought I should have acquired before that time if I had gone on making verses; since the continual occasion for words of the same import, but of different length, to suit the measure, or of different sound for the rhyme, would have laid me under a constant necessity of searching for variety, and also have tended to fix that variety in my mind, and make me master of it. Therefore I took some of the tales and turned them into verse; and, after a time, when I had pretty well forgotten the prose, turned them back again. I also sometimes jumbled my collections of hints into confusion, and after some weeks endeavored to reduce them into the best order, before I began to form the full sentences and compleat the paper. This was to teach me method in the arrangement of thoughts. By comparing my work afterwards with the original, I discovered many faults and amended them; but I sometimes had the pleasure of fancying that, in certain particulars of small import, I had been lucky enough to improve the method of the language, and this encouraged me to think I might possibly in time come to be a tolerable English writer, of which I was extremely ambitious. My time for these exercises and for reading was at night, after work or before it began in the morning, or on Sundays, when I contrived to be in the printing-house alone, evading as much as I could the common attendance on public worship which my father used to exact of me when I was under his care, and which indeed I still thought a duty, thought I could not, as it seemed to me, afford time to practise it."

BenSecondText = "At his house I lay that night, and the next morning reach'd Burlington, but had the mortification to find that the regular boats were gone a little before my coming, and no other expected to go before Tuesday, this being Saturday; wherefore I returned to an old woman in the town, of whom I had bought gingerbread to eat on the water, and ask'd her advice. She invited me to lodge at her house till a passage by water should offer; and being tired with my foot traveling, I accepted the invitation. She understanding I was a printer, would have had me stay at that town and follow my business, being ignorant of the stock necessary to begin with. She was very hospitable, gave me a dinner of ox-cheek with great good will, accepting only of a pot of ale in return; and I thought myself fixed till Tuesday should come. However, walking in the evening by the side of the river, a boat came by, which I found was going towards Philadelphia, with several people in her. They took me in, and, as there was no wind, we row'd all the way; and about midnight, not having yet seen the city, some of the company were confident we must have passed it, and would row no farther; the others knew not where we were; so we put toward the shore, got into a creek, landed near an old fence, with the rails of which we made a fire, the night being cold, in October, and there we remained till daylight. Then one of the company knew the place to be Cooper's Creek, a little above Philadelphia, which we saw as soon as we got out of the creek, and arriv'd there about eight or nine o'clock on the Sunday morning, and landed at the Market-street wharf."

BenThirdText = "My brother-in-law, Holmes, being now at Philadelphia, advised my return to my business; and Keimer tempted me, with an offer of large wages by the year, to come and take the management of his printing-house, that he might better attend his stationer's shop. I had heard a bad character of him in London from his wife and her friends, and was not fond of having any more to do with him. I tri'd for farther employment as a merchant's clerk; but, not readily meeting with any, I clos'd again with Keimer. I found in his house these hands: Hugh Meredith, a Welsh Pennsylvanian, thirty years of age, bred to country work; honest, sensible, had a great deal of solid observation, was something of a reader, but given to drink. Stephen Potts, a young countryman of full age, bred to the same, of uncommon natural parts, and great wit and humor, but a little idle. These he had agreed with at extream low wages per week to be rais'd a shilling every three months, as they would deserve by improving in their business; and the expectation of these high wages, to come on hereafter, was what he had drawn them in with. Meredith was to work at press, Potts at book-binding, which he, by agreement, was to teach them, though he knew neither one nor t'other. John——, a wild Irishman, brought up to no business, whose service, for four years, Keimer had purchased from the captain of a ship; he, too, was to be made a pressman. George Webb, an Oxford scholar, whose time for four years he had likewise bought, intending him for a compositor, of whom more presently; and David Harry, a country boy, whom he had taken apprentice."

## Tokenize
tokens = nltk.word_tokenize(BenFranklinText)
#print "TOKENS"
#print tokens

## Tag the tokens
pos_tagged_tokens = nltk.pos_tag(tokens)
print "TAGGED PARAGRAPH"
print pos_tagged_tokens

## I can name entities if I'd like
#namedEntitySentence = nltk.ne_chunk(pos_tagged_tokens)

## Chunk
#grammar = r"""
#  NP: {<DT|PRP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
#      {<NNP>+}                # chunk sequences of proper nouns
#"""
#cp = nltk.RegexpParser(grammar)
#result = cp.parse(pos_tagged_tokens)
#print "CHUNKED PARAGRAPH"
#print result

###################################
## Detect verb beliefs/attitudes ##
###################################

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
    
## Find any belief verbs
beliefVerbs = ["believe", "believes", "believed", "believing", "know", "knows", "knew", "knowing", "perceive", "perceives", "perceive", "perceiving", "notice", "notices", "noticed", "noticing", "remember", "remembers", "remembered", "remembering", "think", "thinks", "thought", "thinking", "imagine", "imagines", "imagined", "imagining", "suspect", "suspects", "suppose", "suspecting", "assume", "presume", "surmise", "conclude", "deduce", "understand", "understands", "understood", "understanding", "judge", "doubt"]
verb = []
for verb in verbList:
    for testVerb in beliefVerbs:
        if str.lower(verb[0]) == testVerb:
            print "BELIEF"
            print verb
            print ReturnSentence(verb)

## Find any attitude verbs
attitudeVerbs = ["want", "wanted", "wants", "wish", "wishes", "wished", "consider", "considers", "considered", "desire", "desires", "desired", "hope", "hoped", "hopes", "aspire", "aspired", "aspires", "fancy", "fancied", "fancies", "care", "cares", "cared", "like", "likes", "liked"]
verb = []
for verb in verbList:
    for testVerb in attitudeVerbs:
        if str.lower(verb[0]) == testVerb:
            print "ATTITUDE"
            print verb
            print ReturnSentence(verb)

#######################################
## Detect non-verb beliefs/attitudes ##
#######################################

## Find 'is' verbs
isWords = ["is", "was", "were", "are"]
isVerbsFound = []
for eachVerb in verbList:
    for testVerb in isWords:
        if str.lower(eachVerb[0]) == testVerb:
            isVerbsFound.append(eachVerb)

beliefNonVerbs = ["belief", "beliefs", "knowledge", "perception", "perceptions", "memory", "memories", "suspicion", "suspicions", "assumption", "assumptions", "presupposition", "presuppositions", "suppositions", "supposition", "conclusion", "conclusions", "understanding", "judgment", "doubt", "doubts"]
attitudeNonVerbs = ["desire", "desires", "wants", "want", "wish", "wishes", "hope", "hopes", "aspirations", "aspiration", "fancy", "fancies", "care", "cares"]

## “(PRP) (belief/attitude) is…”
for isVerb in isVerbsFound:
    ## First, apply a grammar
    grammar = r"""
      NP: {<DT|PRP\$|NNP>?<JJ>*<NN><VB.|VB>}
    """
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(ReturnSentence(isVerb,taggedVersion=True,capitalize=False))
    ## Then, extract the chunks found by the grammar
    foundChunks = []
    for eachResult in result:
        if str(eachResult).count('/') > 0:
            foundChunks.append(eachResult)
    #print "CHUNKS PRINT"
    #print foundChunks
    ## Check if the subject is a belief/attitude word
    for eachChunk in foundChunks:
        for eachWord in eachChunk:
            if eachWord[1] == "NN":
                for eachBeliefNonverb in beliefNonVerbs:
                    if str.lower(eachWord[0]) == eachBeliefNonverb:
                        print "FOUND A BELIEF"
                        print eachWord[0]
                        verb = [eachWord[0], eachWord[1], isVerb[2]]
                        print ReturnSentence(verb)
                for eachAttitudeNonverb in attitudeNonVerbs:
                    if str.lower(eachWord[0]) == eachAttitudeNonverb:
                        print "FOUND AN ATTITUDE"
                        print eachWord[0]
                        verb = [eachWord[0], eachWord[1], isVerb[2]]
                        print ReturnSentence(verb)

