# Intention Detection

The goal behind this project is to see if I can build a program that will recognize intentional sentences, which are sentences describing the beliefs, desires, and actions of some person or group of people.

The aim is not to digest or understand the sentences, its goal is simply to label them.

## Intentional sentences

Intention can be roughly thought of as causal descriptions. They are part of our understanding of other minds, or more specifically about willfulness. (This is not to be confused with Bretano’s “intentionality”, which describes the nature of our mental states to be “directed at” some object.)

There are three types of sentences that are grouped under the category of intentional:

1. Descriptions of actions
2. descriptions of intent
3. and descriptions of future plans

It should be obvious that these are closely related, [though the exact way that they are is up for philosophical debate.](http://plato.stanford.edu/entries/intention/)

## What to look for

To recognize sentences which carry intent, we need a way of recognizing when a sentence has that sort of content. First, let’s consider sentences describing intent, which Davidson calls a “primary reason”.

> A primary reason consists of a belief and an attitude, but it is generally otiose to mention both. (Davidson)

In speech we only ever overtly say either the belief or attitude associated with some intent, the other description is typically left as implicit. These two halves are called “beliefs” and “attitudes” by Davidson.

An example of a belief:
> If you tell me you are easing the jib because you think that will stop the main from backing, I don’t need to be told you want to stop the main from backing […] (Davidson)
In this case, knowledge about the effect easing a job has on the main backing is all one needs to understand the intent behind someone’s actions. It is implicit in their description that they don’t want the main to back.

An example of attitude:
> […] if you say you are biting your thumb at me because you want to insult me, there is no point in adding that you think that by biting your thumb at me you will insult me. (Davidson)
In this case, your intention is perfectly well translated by explaining what your attitude is. It’s not necessary to explain that you believe your action will accomplish that goal.

So, all we have to do is write a program that recognizes these two sorts of sentences.

### Statements of belief

This appears to be the easier one. If the statement is about belief, it should have a verb in it that is a rough synonym for belief: believe, know, perceive, notice, remember, and other synonyms and all conjugations of these verbs.