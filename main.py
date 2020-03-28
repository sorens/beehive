#!/usr/bin/env python3

import sys
import argparse
import os

# debug print function
def debug_log(output, *args):
    message = "DEBUG => "
    for a in args:
        message += a
    print(message, file=output)

def output_log(output, *args):
    message = ""
    for a in args:
        message += a
    print(message, file=output)

# Score points to increase your rating.
# 4-letter words are worth 1 point each.
# Longer words earn 1 point per letter.
# Each puzzle includes at least one “pangram” which uses every letter. 
# These are worth 7 extra points!
def score(word, letters):
    if len(word) == 4:
        return 1
    elif len(word) >= 7:
        all_used = True
        for letter in letters:
            if letter not in word:
                all_used = False
                break
        
        if all_used:
            return len(word) + 7        
    
    return len(word)

def has_vowels(word):
    vowels = "aeiouy"
    has_vowels = False
    for letter in word:
        if letter in vowels:
            has_vowels = True
            break

    return has_vowels

# load individual dictionary files from disk into a single dictionary in memory
def load_dictionary(path, dictionary):
    with open(path, "r") as file:
        while True:
            line = file.readline().rstrip()
            
            if not line:
                break
            if line[0].isupper():
                continue
            if len(line) < 4:
                continue
            
            key = line.lower()
            if has_vowels(key):
                if key in dictionary:
                    dictionary[key] = dictionary[key] + 1
                else:
                    dictionary[key] = 1
        
    return dictionary

# Create words using letters from the hive.
# Words must contain at least 4 letters.
# Words must include the center letter.
# Our word list does not include words that are obscure, hyphenated, or proper nouns.
# No cussing either, sorry.
# Letters can be used more than once.
def beehive(dictionary, letters, center_letter, debug, path, level, is_stdout):
    answers = []
    return answers

parser = argparse.ArgumentParser(description='beehive')
parser.add_argument("--letters", type=str, help="non-center letters from beehive board", required=True)
parser.add_argument("--center", type=str, help="center letter from beehive board", required=True)
parser.add_argument("--debug", help="enable debug output", action='store_true', default=False, required=False)
parser.add_argument("--path", type=str, help="location to output answers", required=False)
parser.add_argument("--level", type=int, help="number of dictionary a matched word should appear in", required=False, default=0)
parser.add_argument("--stdout", help="", action='store_true', default=False, required=False)
args = parser.parse_args()
is_stdout = args.stdout
letters = args.letters.rstrip().lower()
center = args.center.rstrip().lower()
output_path = ""
if is_stdout == False:
    if args.path:
        output_path = args.path.rstrip().lower()
    else:
        is_stdout = True
all_letters = letters + center
level = args.level

if is_stdout == False:
    output_log(sys.stdout, "behive running...")

output_path = os.path.join(output_path, all_letters + "." + "txt")    

if is_stdout:
    output = sys.stdout
else:
    output = open(output_path, 'w')

dictionary = {}
dictionary = load_dictionary(os.path.join("word_files", "wordlist.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "wordlist.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "wordlist.10000.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "words_alpha.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "words.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "usa2.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "usa.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "ukenglish.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "english2.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "english3.txt"), dictionary)
dictionary = load_dictionary(os.path.join("word_files", "engmix.txt"), dictionary)

beehive(dictionary, letters, center, args.debug, output_path, level, is_stdout)

output_log(output, "{:<32s} {:>6s}".format("letters:", letters.upper()))
output_log(output, "{:<32s} {:>6s}".format("center letter:", center.upper()))

center_matched = {}
for word in dictionary:
    if center in word:
        center_matched[word] = dictionary[word]

output_log(output, "{:<32s} {:>6s}".format("words checked:", str(len(dictionary.keys()))))
output_log(output, "{:<32s} {:>6s}".format("words with center letter:", str(len(center_matched.keys()))))

matched = {}
for word in center_matched:
    found = True
    for letter in word:
        if found:
            if args.debug:
                debug_log(output, "checking letter: '" + letter + "' in all letters: '" + all_letters + "'")
            if letter not in all_letters:
                found = False
                break
    
    if found:
        if args.debug:
            debug_log(output, "" + word + " ADDED")
        matched[word] = center_matched[word]
        found = False
    else:
        if args.debug:
            debug_log(output, "" + word + " SKIPPED")

output_log(output, "{:<32s} {:>6s}".format("words matched with all letters:", str(len(matched))))

# remove words that are not in more than 'level' dictionaries
# if level is 0, inclue all anwers
likely_words = {}
for word in matched:
    if level == 0 or matched[word] >= level:
        likely_words[word] = matched[word]

output_log(output, "{:<32s} {:>6s}".format("likely good word:", str(len(likely_words))))

h = {}
for letter in all_letters:
    h[letter] = []

sorted_answers = []
# sort by length
for word in sorted(likely_words, key=lambda word: len(word), reverse=True):
    sorted_answers.append(word)

total_score = 0
for word in sorted_answers:
    h[word[0]].append(word)
    word_score = score(word, all_letters)
    total_score += word_score

output_log(output, "{:<32s} {:>6s}".format("total score:", str(total_score)))

for key in h.keys():
    output_log(output, "{:21s} \"{:<1s}\"        {:>4s} {:>4s}".format("words that begin with", key.upper(), "score", "level"))
    output_log(output, "{:<32s} {:>4s} {:>4s}".format("-------------------------", "-----", "-----"))
    for word in h[key]:
        word_score = score(word, all_letters)
        output_log(output, "{:3}{:<29s} {:>4d} {:>4d}".format("=> ", word, word_score, dictionary[word]))

output.close() 

if is_stdout == False:
    output_log(sys.stdout, "beehive finished")
