#!/usr/bin/python3

import re
import sys

debug = False

def count_syllables(word):

    if debug:
        print("Debug mode is on.")

    word = word.lower().strip("!?;:.,\n\t")

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious','crucial','poem']
    exception_del = ['fortunately','unfortunately']

    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']

    pre_one = ['preach']

    syls = 0 # added syllable number
    disc = 0 # discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        if debug: print("#1")
        syls = 1
        return syls

    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtriple_1 = len(re.findall(r'[eaoui][eaoui]',word))
        if doubleAndtriple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                if debug: print("#2")
                disc+=1

    #3) discard trailing "e", except where ending is "le"

    # words which are an exception to this rule
    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while','inhale','exhale']

    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass

        elif len(re.findall(r'[eaoui][eaoui]',word[-2:])) == 1:
            # don't discard anything if the word ends in two vowels (e.g "true")
            pass

        else :
            if debug: print("#3")
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtriple = len(re.findall(r'[eaoui][eaoui]',word))
    triple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
    if doubleAndtriple + triple > 0:
        if debug: print("#4 - doubleAndtriple: {}".format(doubleAndtriple))
        if debug: print("#4 - triple: {}".format(triple))
    disc+=doubleAndtriple + triple

    #5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        if debug: print("#6")
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        if debug: print("#7")
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    if debug: print("#8")
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui" :
        if debug: print("#9 - tri")
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        if debug: print("#9 - bi")
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian" :
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            if debug: print("#10")
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui' :

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            if debug: print("#11")
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            if debug: print("#11")
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            if debug: print("#12")
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]

    if word[-3:] == "n't" :
        if word in negative :
            if debug: print("#13")
            syls+=1
        else :
            pass

    #14) Handling the exceptional words.

    if word in exception_del :
        if debug: print("#14")
        disc+=1

    if word in exception_add :
        if debug: print("#14")
        syls+=1

    # calculate the output
    return numVowels - disc + syls

if __name__ == "__main__":

    if ("-d" in sys.argv):
        debug = True

    words = sys.stdin.read().split()

    for word in words:
        print(count_syllables(word))