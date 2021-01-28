#!/usr/bin/python3
import sys
import os.path
import re

#-------------------------------------------------------------------------------------------------------------------#
# A project made to illustrate the capability to itterate through common human behaviours when choosing a password. #
#                            P.S - May be slow / unstable for longer words (Good!)                                  #
#                                       Disclaimer: Education purposes only!                                        #                                           
#-------------------------------------------------------------------------------------------------------------------#

#May be needed on some machines (Added risk!)
#sys.setrecursionlimit(2048)

mainPhrase = input("Please Input The String Your Want To Craft Into A Wordlist: ")

wordlistPath = "wordlist.txt"

# Temp files for seperation
wordlistPath_TMP = ".wordlist.tmp"
wordlistPath_TMP02 = ".wordlistNum.tmp"
wordlistPath_TMP03 = ".wordlistSym.tmp"
wordlistPath_TMP04 = ".wordlistCap.tmp"


#Exta list for complete uppercase throughput
# listVariations = [
#     "a A @", "b B 8", "c C", "d D", "e E 3", "f F", "g G", "h H", "i I ! 1",
#     "j J", "k K", "l L ! 1", "m M", "n N", "o O", "p P", "q Q", "r R", "S s 5 $",
#     "t T 7", "u U", "v V", "w W", "x X", "y Y", "z Z"
# ]

# Bindings for character combinations
listVariations = [
    "a A @", "b B ", "e E ", "i I ! ", "l L !", "o O ", "S s  $", "t T 7"
]

# List of Symbols to try to append to the end
listSymbols = ["!", "?", "@", "$", "~", "#", "%", "&"]

#Split up phrase into each character
def phraseParse(nextPhrase=""):
    if nextPhrase:
        global mainPhrase
        mainPhrase = nextPhrase #Can alter which phrase is used, for rerunning based off combinations found

    for phraseChar in mainPhrase:  #each letter in phrase
        checkRuleMatch(phraseChar) #check each char

def checkRuleMatch(charToMatch):
    for rule in listVariations: # for each rule bracket
        for ruleChar in rule: # for each char of each rule
            if ruleChar != " " and ruleChar == charToMatch:  #if the value is valid and is found in a bracket
                giveRuleBinding(charToMatch, rule) #pass found character and it's rule char

def giveRuleBinding(foundChar, matchedRule):
    for ruleChar in matchedRule: # for each char of the matched rule
        if ruleChar != " " and ruleChar != foundChar: #if potential variations are found
            checkExistence(foundChar, ruleChar) #check if this combination already exists, important for the first itterations especially

def checkExistence(foundChar, ruleChar):
    newPhrase = mainPhrase.replace(foundChar, ruleChar, 1) #create potential phrase by replacing the single occurance found
    if os.path.isfile(wordlistPath_TMP):
        f = open(wordlistPath_TMP, "r")
        for line in f:
            if line != " " and line == newPhrase: #if the combination already exists
                f.close()
                return 0 #forget it and look at the next
    newPhraseFormer(newPhrase) # ready for adding


def newPhraseFormer(newPhrase):
    f = open(wordlistPath_TMP, "a") #append mode
    f.write(newPhrase + "\n") #writing
    f.close()

    combinationProcess() # Lets see if we can find anymore combinations ~ Loops until there is nothing left new

def combinationProcess():
    if os.path.isfile(wordlistPath_TMP):
        f = open(wordlistPath_TMP, "r")
        for line in f:
            phraseParse(line.lstrip("\n")) #reruns the process passing the combination as a phrase, which cannot rewrite existing findings
        f.close()


def formatList():
    f = open(wordlistPath_TMP, 'r')
    wordlist = open(wordlistPath, 'w')
    
    for line in f.readlines():
        if re.search('\S', line.rstrip()): #Needed to trim newlines to pull it together into a nice wordlist to itterate through more
            wordlist.write(line)
    f.close()
    wordlist.close()

def appendNum():
    f = open(wordlistPath, 'r')
    f2 = open(wordlistPath_TMP02, 'a+')
    for line in f:
        if line != '\n':
            for x in range(0, 100): 
                f2.write(line.rstrip("\n") + str(x) +  "\n") #adds 0-99 to each of the existing combinations, into a new list
    f.close()

def appendSym():
    f = open(wordlistPath, 'r')
    f3 = open(wordlistPath_TMP03, 'a+')
    for line in f:
        if line != '\n':
            for x in listSymbols:
                f3.write(line.rstrip("\n") + x +  "\n") #adds each element from the above symbols list, to each of the existing combinations, into a new list


def CapPrefix():
    f = open(wordlistPath, 'r')
    f4 = open(wordlistPath_TMP04, 'a+')
    for line in f:
        if line != '\n':
            if line[0].isupper() == False:
                f4.write(line.rstrip("\n").title() + "\n") #adds a cap combination for each if it needs it, and stores in a new list


def tmpMerge(fileToAdd, wordlist): #A universal merger that is ran multiple times to unify lists. It was important to seperate lists as to not itterate on new litural content,
    originalFile = open(fileToAdd, 'r') 
    endList = open(wordlist, 'a+')

    for line in originalFile:
        endList.write(line)

def main():
    #stack order
    phraseParse()
    formatList()
    appendNum()
    tmpMerge(wordlistPath_TMP02, wordlistPath)
    appendSym()
    tmpMerge(wordlistPath_TMP03, wordlistPath)
    CapPrefix()
    tmpMerge(wordlistPath_TMP04, wordlistPath)

    #remove temp files when they are uneeded - python lists could be used instead 
    os.remove(wordlistPath_TMP)
    os.remove(wordlistPath_TMP02)
    os.remove(wordlistPath_TMP03)
    os.remove(wordlistPath_TMP04)

if __name__ == "__main__":
    main()



