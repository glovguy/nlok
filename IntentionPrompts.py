import json
import nltk
from IntentionDetection import *


def save_and_quit(my_output, fileName):
    outputFileName = raw_input('what would you like to call the new filename?\n: ')
    if outputFileName == '':
        print "assuming it is the same as input, but with '.intention' appended"
        outputFileName = fileName
    elif '.intention' not in outputFileName:
        outputFileName = outputFileName + '.intention'
    output_file = open(outputFileName, 'w')
    json.dump(my_output, output_file)
    print "my_output"
    print my_output
    print "file saved as ", outputFileName
    quit('saved and quitting')


def load_file(fileName, file_type):
    import os
    print "Loading..."
    try:
        text_file = open(fileName, "r")
    except:
        try:
            print "Looking also in /TextExamples folder"
            myCWD = os.getcwd()
            fileName = myCWD + "/TextExamples/" + fileName
            text_file = open(fileName)
        except:
            quit("ERROR FINDING FILE")
    if file_type == "intention":
        raw_text = json.load(text_file)
    elif file_type == "txt":
        raw_text = text_file.readlines()
    else:
        raise Exception("unrecognized file type")
    text_file.close()
    print "done \n"
    return raw_text


def determine_file_type(fileName):
    if fileName == "":
        print "no filename given, using exampleText.txt as default"
        fileName = 'exampleText.txt'
    if fileName[-10:] == ".intention":
        file_type = "intention"
    elif fileName[-3:] == ".txt":
        file_type = "txt"
    else:
        if fileName[len(str(fileName))-4] == ".":
            quit("unrecognized filetype")
        print "No file extension, assuming it's a .txt file"
        file_type = txt
    return file_type


def prompt_setences_and_ask_intention(raw_text):
    #########################
    ## Cycle through lines ##
    #########################
    print "Okay, let's begin...\n-----\n\n"
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    my_output = []
    for eachParagraph in raw_text:
        selectedSentences = []
        if eachParagraph == '\n':
            continue
        sentenceTokens = sent_detector.tokenize(eachParagraph.strip())
        for i in 3 * range(len(eachParagraph)):  # user gets 3*number of sentences
            tally = 10
            for eachSentence in sentenceTokens:
                if tally in selectedSentences:
                    print "  * " + str(tally) + ":  " + eachSentence
                else:
                    print "    " + str(tally) + ":  " + eachSentence
                tally += 1
            userInput = raw_input('\n\nAny intentional sentences?\n Enter line number\n 0 to save and quit\n or hit return to move on:')
            if userInput == '':
                print "okay, none\n\n---\n"
                break
            elif int(userInput) == 0:
                resp = raw_input('save and quit? y/n\n: ')
                if resp == "y":
                    return my_output
            elif int(userInput) == 0:
                print "undefined"
            elif int(userInput) > 0 and int(userInput) <= tally and not int(userInput) in selectedSentences:
                selectedSentences.append(int(userInput))
            else:
                print "be nice.."
            print "\n\n"
        i = 1  # user input is 1-indexed, so this is as well
        for eachSentence in sentenceTokens:
            if i in selectedSentences:
                my_output = my_output + [eachSentence, 1]
            if i not in selectedSentences:
                my_output = my_output + [eachSentence, 0]
            i += 1


if __name__ == "__main__":
    ################################
    ## Load text provided by user ##
    ################################
    fileName = raw_input('File Name: ')
    if fileName == "":
        print "no filename given, using exampleText.txt as default"
        fileName = 'exampleText.txt'
    file_type = determine_file_type(fileName)
    raw_text = load_file(fileName, file_type)
    if file_type == txt:
        print "And what would you like to do with this file?"
        print "1: Print all intentional sentences"
        print "2: Give the number of sentences in the entire document"
        print "3: Print report on density of intentional statements in text"
        print "4: Manually enter intention data and save as .intention file"
        print "0: Unit tests"
        selectedFunction = input("\n: ")
        if selectedFunction == 1:
            ## 1: Detect and print all intentional sentences
            print_all_intentional_sentences(raw_text)
        elif selectedFunction == 2:
            ## 2: Detect the number of intentional sentences in the entire document
            total_number_of_intentional_sentences(raw_text)
        elif selectedFunction == 3:
            ## 3: Print report on density of intentional statements in text
            report_density_of_intentional_sentences(raw_text)
        elif file_type == "txt" and selectedFunction == 4:
            ## 4: User inputs to determine which sentences are intentional
            my_output = prompt_setences_and_ask_intention(raw_text)
            save_and_quit(my_output, fileName)
        elif selectedFunction == 0:
            ## 0: Perform unit tests
            unittest.main()
        else:
            print "Invalid entry"
    elif file_type == "intention":
        print "And what would you like to do with this file?"
        print "1: Print this .intention file"
        print "2: Pick up prompting where you last left off"
        selectedFunction = input("\n: ")
        if selectedFunction == 1:
            print raw_text
        elif selectedFunction == 2:
            restart_prompting(raw_text)
        else:
            print "Invalid entry"
