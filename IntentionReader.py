import nltk

if __name__ == "__main__":
    ################################
    ## Load text provided by user ##
    ################################
    import os
    fileName = raw_input('File Name: ')
    if fileName == "":
        print "no filename given, using exampleText.txt as default"
        fileName = 'exampleText.txt'
    if fileName[-3:] != "txt":
        if fileName[len(str(fileName))-4] == ".": quit("unrecognized filetype")
        print "No file extension, assuming it's a .txt file"
        fileName = fileName + ".txt"
    print "Loading..."
    try:
        text_file = open(fileName, "r")
    except:
        try:
            print "Looking also in /TextExamples folder"
            myCWD = os.getcwd()
            fileName = myCWD + "/TextExamples/" + fileName
            print fileName
            text_file = open(fileName, "r")
        except:
            quit("ERROR FINDING FILE")
    paragraphs = text_file.readlines()
    print "done \n"
    #########################
    ## Cycle through lines ##
    #########################
    print "Okay, let's begin...\n---\n\n"
    for eachParagraph in paragraphs:
        selectedSentences = []
        while eachParagraph != '\n':
            tokens = nltk.word_tokenize(eachParagraph)
            index = 0
            prevIndex = 0
            tally = 1
            for eachToken in tokens:
                index += 1
                if eachToken == "." or eachToken == "?" or eachToken == "!" or eachToken == ";":
                    if tally in selectedSentences:
                        print "  * " + str(tally) + ":  " + str(' '.join(tokens[prevIndex:index]))
                    else:
                        print "    " + str(tally) + ":  " + str(' '.join(tokens[prevIndex:index]))
                    tally += 1
                    prevIndex = index
            userInput = raw_input('\nAny intentional sentences?\nEnter number or hit return to move on:')
            if userInput == '':
                print "okay, none\n\n---\n"
                break
            elif int(userInput) == 0:
                print "undefined"
            elif int(userInput) > 0 and int(userInput) <= tally and not int(userInput) in selectedSentences:
                selectedSentences.append(int(userInput))
            else:
                print "be nice.."
            print "\n\n"
