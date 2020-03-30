import sys
import argparse

# Create words using letters from the hive.

# Words must contain at least 4 letters.
# Words must include the center letter.
# Our word list does not include words that are obscure, hyphenated, or proper nouns.
# No cussing either, sorry.
# Letters can be used more than once.
# Score points to increase your rating.

# 4-letter words are worth 1 point each.
# Longer words earn 1 point per letter.
# Each puzzle includes at least one “pangram” which uses every letter. 
# These are worth 7 extra points!

def score(word):
    if len(word) == 4:
        return 1
    else:
        return len(word)

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

            dictionary[line.lower()] = line.lower()
        
    return dictionary

parser = argparse.ArgumentParser(description='beehive')
parser.add_argument("--letters", type=str, help="non-center letters from beehive board", required=True)
parser.add_argument("--center", type=str, help="center letter from beehive board", required=True)
parser.add_argument("--debug", help="enable debug output", action='store_true', default=False, required=False)
args = parser.parse_args()
letters = args.letters.rstrip().lower()
center = args.center.rstrip().lower()
all_letters = letters + center
print("beehive letters:      " + letters.upper())
print("behive center letter: " + center.upper())

dictionary = {}
dictionary = load_dictionary("word_files/wordlist.txt", dictionary)
dictionary = load_dictionary("word_files/wordlist.10000.txt", dictionary)
dictionary = load_dictionary("word_files/words_alpha.txt", dictionary)
dictionary = load_dictionary("word_files/words.txt", dictionary)
dictionary = load_dictionary("word_files/usa2.txt", dictionary)
dictionary = load_dictionary("word_files/usa.txt", dictionary)
dictionary = load_dictionary("word_files/ukenglish.txt", dictionary)
dictionary = load_dictionary("word_files/english2.txt", dictionary)
dictionary = load_dictionary("word_files/english3.txt", dictionary)
dictionary = load_dictionary("word_files/engmix.txt", dictionary)

center_matched = {}
for word in dictionary:
    if center in word:
        center_matched[word] = word

print("beehive words checked: " + str(len(dictionary.keys())))
print("beehive words with center letter '" + center.upper() + "': " + str(len(center_matched.keys())))

matched = {}
for word in center_matched:
    found = True
    for letter in word:
        if found:
            if args.debug:
                print("DEBUG => checking letter: '" + letter + "' in all letters: '" + all_letters + "'")
            if letter not in all_letters:
                found = False
                break
    
    if found:
        if args.debug:
            print("DEBUG => " + word + " ADDED")
        matched[word] = word
        found = False
    else:
        if args.debug:
            print("DEBUG => " + word + " SKIPPED")

print("beehive words matched with all letters: " + str(len(matched)))
sorted_answers = []
# sort by length
for word in sorted(matched, key=lambda word: len(matched[word]), reverse=True):
    sorted_answers.append(word)

total_score = 0
for word in sorted_answers:
    word_score = score(word)
    total_score += word_score
    print("answer: '" + word + "', value: " + str(word_score))

print("beehive total score: " + str(total_score))