#!/usr/bin/env python3

import sys
import argparse
import os
import codecs
import glob

LEVEL = 0
SCORE = 1


def output_log(output, *args):
    message = ""
    for a in args:
        message += a
    print(message, file=output)

# debug print function


def debug_log(output, *args):
    new_args = []
    new_args.append("DEBUG => ")
    new_args.append(*args)
    output_log(output, *new_args)

# Score points to increase your rating.
# 4-letter words are worth 1 point each.
# Longer words earn 1 point per letter.
# Each puzzle includes at least one "pangram" which uses every letter.
# These are worth 7 extra points!


def score(word, letters):
    length = len(word)
    if length == 4:
        return 1
    elif length >= 7:
        if letters != "":
            all_used = True
            for letter in letters:
                if letter not in word:
                    all_used = False
                    break
            if all_used:
                return length + 7

    return length


def has_vowels(word):
    vowels = "aeiouy"
    has_vowels = False
    for letter in word:
        if letter in vowels:
            has_vowels = True
            break

    return has_vowels


def has_non_word_characters(word):
    for letter in word:
        value = ord(letter)
        if value < 65:
            return False
        elif value > 90 and value < 97:
            return False
        elif value > 122 and value < 127:
            return False

    return True


def is_valid_word(word):
    if has_vowels(word):
        if has_non_word_characters(word):
            return True

    return False

# load individual dictionary files from disk into a single dictionary in memory


def load_dictionary(path, dictionary, letters, ignore_capital):
    with codecs.open(path, encoding='utf-8') as file:
        for line in file:
            line = line.rstrip()
            length = len(line)
            if not line:
                break
            if ignore_capital and line[0].isupper():
                continue
            if length < 4 or length > 26:
                continue

            key = line.lower()
            if is_valid_word(key):
                if key in dictionary:
                    tup = dictionary[key]
                    level = tup[LEVEL]
                    level = level+1
                    if "missed.txt" in path:
                        level = 100+level
                    word_score = tup[SCORE]
                    tup = [level, word_score]
                    dictionary[key] = tup
                else:
                    level = 1
                    if "missed.txt" in path:
                        level = 100
                    tup = []
                    tup.append(level)
                    tup.append(score(key, letters))
                    dictionary[key] = tup

    output_log(sys.stdout, "{:<29s} loaded ({:>9})".format(
        path, str(len(dictionary))))
    return dictionary


def load_dictionaries(path, letters):
    dictionary = {}
    word_files_path = os.path.join(path, "*.txt")
    files = glob.glob(word_files_path)
    if len(files) == 0:
        output_log(sys.stderr, "no word files found")
        return

    for file in files:
        dictionary = load_dictionary(file, dictionary, letters, True)
    return dictionary


def count_unique_letters_in_word(word):
    letters = {}
    if word != "":
        for letter in word:
            letters[letter] = letter

    return len(letters)

# Create words using letters from the hive.
# Words must contain at least 4 letters.
# Words must include the center letter.
# Our word list does not include words that are obscure, hyphenated, or proper nouns.
# No cussing either, sorry.
# Letters can be used more than once.


def beehive(dictionary, letters, center_letter, debug, path, level, is_stdout, output):
    all_letters = letters + center_letter
    output_log(output, "{:<32s} {:>6s}".format("letters:", letters.upper()))
    output_log(output, "{:<32s} {:>6s}".format(
        "center letter:", center_letter.upper()))

    center_matched = {}
    for word in dictionary:
        if center_letter in word:
            center_matched[word] = dictionary[word]

    output_log(output, "{:<32s} {:>6s}".format(
        "words checked:", str(len(dictionary.keys()))))
    output_log(output, "{:<32s} {:>6s}".format(
        "words with center letter:", str(len(center_matched.keys()))))

    matched = {}
    for word in center_matched:
        found = True
        for letter in word:
            if found:
                if debug:
                    debug_log(output, "checking letter: '" +
                              letter + "' from word: '" + word + "'")
                if letter not in all_letters:
                    found = False
                    break

        if found:
            if debug:
                debug_log(output, "" + word + " ADDED")
            matched[word] = center_matched[word]
            found = False
        else:
            if debug:
                debug_log(output, "" + word + " SKIPPED")

    output_log(output, "{:<32s} {:>6s}".format(
        "words matched with all letters:", str(len(matched))))

    # remove words that are not in more than 'level' dictionaries
    # if level is 0, inclue all anwers
    likely_words = {}
    total_score = 0
    for word in matched:
        if level == 0 or matched[word][LEVEL] >= level:
            likely_words[word] = matched[word]
            total_score += matched[word][SCORE]

    output_log(output, "{:<32s} {:>6s}".format(
        "likely good word:", str(len(likely_words))))
    output_log(output, "{:<32s} {:>6s}".format(
        "total score:", str(total_score)))

    h = {}
    for letter in all_letters:
        h[letter] = []

    sorted_answers = []
    # sort by level
    for word in sorted(likely_words, key=lambda word: likely_words[word][LEVEL], reverse=True):
        sorted_answers.append(word)
        h[word[0]].append(word)

    for key in h.keys():
        output_log(output, "{:21s} \"{:<1s}\"        {:>4s} {:>4s}".format(
            "words that begin with", key.upper(), "score", "level"))
        output_log(output, "{:<32s} {:>4s} {:>4s}".format(
            "-------------------------", "-----", "-----"))
        for word in h[key]:
            output_log(output, "{:3}{:<29s} {:>4d} {:>4d}".format(
                "=> ", word, dictionary[word][SCORE], dictionary[word][LEVEL]))


def pangrams(dictionary, output):
    words = {}
    for word in dictionary:
        if count_unique_letters_in_word(word) == 7:
            words[word] = word

    output_log(output, "{:<32s} {:>15d}".format(
        "number of pangram words:", len(words)))
    for word in words:
        output_log(output, "{:<32s} {:>15s}".format("pangram word:", word))


def analyze(dictionary, output, answer_file):
    words = {}
    words = load_dictionary(answer_file, words, "", False)

    for word in words:
        output_log(output, "{:<32s} {:>15s}".format("word:", word))


def main():
    parser = argparse.ArgumentParser(description='beehive puzzle solver')
    parser.add_argument("--letters", type=str,
                        help="non-center letters from beehive board", required=False, default="")
    parser.add_argument(
        "--center", type=str, help="center letter from beehive board", required=False, default="")
    parser.add_argument("--debug", help="enable debug output",
                        action='store_true', default=False, required=False)
    parser.add_argument("--path", type=str,
                        help="location to output answers", required=False)
    parser.add_argument(
        "--level", type=int, help="number of dictionary a matched word should appear in", required=False, default=0)
    parser.add_argument("--stdout", help="",
                        action='store_true', default=False, required=False)
    parser.add_argument("--pangrams", help="List all pangram words",
                        action='store_true', default=False, required=False)
    parser.add_argument(
        "--command", help="which command to run (e.g. play, pangrams)", required=True)
    parser.add_argument("--words", help="directory of word files to use",
                        required=False, default="word_files")
    parser.add_argument(
        "--answer", help="location of an answer file", required=False, default="")
    args = parser.parse_args()
    is_stdout = args.stdout

    output_path = ""
    if is_stdout == False:
        if args.path:
            output_path = args.path.rstrip().lower()
        else:
            is_stdout = True

    if is_stdout == False:
        output_log(sys.stdout, "behive running...")

    all_letters = ""
    # check which command we're running
    if args.command == "play":
        letters = ""
        center = ""
        if args.letters != "":
            letters = args.letters.rstrip().lower()
        if args.center != "":
            center = args.center.rstrip().lower()
        all_letters = letters + center
        level = args.level
        output_path = os.path.join(output_path, all_letters + "." + "txt")
        if is_stdout:
            output = sys.stdout
        else:
            output = open(output_path, 'w')

        dictionary = load_dictionaries(args.words, all_letters)
        if dictionary != None:
            beehive(dictionary, letters, center, args.debug,
                    output_path, level, is_stdout, output)

    elif args.command == "pangrams":
        output = sys.stdout
        dictionary = load_dictionaries(args.words, all_letters)
        if dictionary != None:
            pangrams(dictionary, output)
    elif args.command == "analyze":
        output = sys.stdout
        dictionary = load_dictionaries(args.words, all_letters)
        if dictionary != None:
            analyze(dictionary, output, args.answer)
    else:
        output_log(sys.stderr, "unknown command")
        parser.print_help()

    output.close()

    if is_stdout == False:
        output_log(sys.stdout, "beehive finished")


main()
