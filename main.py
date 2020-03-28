import sys
import argparse
import os

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
            if key in dictionary:
                dictionary[key] = dictionary[key] + 1
            else:
                dictionary[key] = 1
        
    return dictionary

print("beehive running")

parser = argparse.ArgumentParser(description='beehive')
parser.add_argument("--letters", type=str, help="non-center letters from beehive board", required=True)
parser.add_argument("--center", type=str, help="center letter from beehive board", required=True)
parser.add_argument("--debug", help="enable debug output", action='store_true', default=False, required=False)
parser.add_argument("--output", type=str, help="location to output answers", required=True)
parser.add_argument("--level", type=int, help="number of dictionary a matched word should appear in", required=False, default=5)
args = parser.parse_args()
letters = args.letters.rstrip().lower()
center = args.center.rstrip().lower()
output_path = args.output.rstrip().lower()
all_letters = letters + center
level = args.level

if output_path == "":
    output_path = os.path.join(".", "output")

output_path = os.path.join(output_path, all_letters + "." + "txt")    

if output_path == "":
    output = sys.stdout
else:
    output = open(output_path, 'w') 

print("beehive letters:      " + letters.upper(), file=output)
print("behive center letter: " + center.upper(), file=output)

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

center_matched = {}
for word in dictionary:
    if center in word:
        center_matched[word] = dictionary[word]

print("beehive words checked: " + str(len(dictionary.keys())), file=output)
print("beehive words with center letter '" + center.upper() + "': " + str(len(center_matched.keys())), file=output)

matched = {}
for word in center_matched:
    found = True
    for letter in word:
        if found:
            if args.debug:
                print("DEBUG => checking letter: '" + letter + "' in all letters: '" + all_letters + "'", file=output)
            if letter not in all_letters:
                found = False
                break
    
    if found:
        if args.debug:
            print("DEBUG => " + word + " ADDED", file=output)
        matched[word] = center_matched[word]
        found = False
    else:
        if args.debug:
            print("DEBUG => " + word + " SKIPPED", file=output)

print("beehive words matched with all letters: " + str(len(matched)), file=output)

# remove words that are not in more than 3 dictionaries
likely_words = {}
for word in matched:
    if matched[word] > level:
        likely_words[word] = matched[word]

print("beehive likely good word: " + str(len(likely_words)), file=output)

h = {}
for letter in all_letters:
    h[letter] = []

sorted_answers = []
# sort by length
for word in sorted(likely_words, key=lambda word: len(word), reverse=True):
    sorted_answers.append(word)

for word in sorted_answers:
    h[word[0]].append(word)

total_score = 0
for key in h.keys():
    print(key.upper(), file=output)
    for word in h[key]:
        word_score = score(word, all_letters)
        total_score += word_score
        # print("answer: '" + word + "', value: " + str(word_score), file=output)
        msg = "=> ({0:2d}) {1:20s} ({2:2d})".format(word_score, word, dictionary[word])
        print(msg, file=output)

print("beehive total score: " + str(total_score), file=output)

output.close() 

print("beehive finished")