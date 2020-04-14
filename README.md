# Beehive utility

This command-line utility helps generate the words for combination of letters or generate a list of pangram words

```bash
> ./beehive --help
usage: beehive [-h] [--letters LETTERS] [--center CENTER] [--debug]
               [--path PATH] [--level LEVEL] [--stdout] [--pangrams] --command
               COMMAND [--words WORDS]

beehive puzzle solver

optional arguments:
  -h, --help         show this help message and exit
  --letters LETTERS  non-center letters from beehive board
  --center CENTER    center letter from beehive board
  --debug            enable debug output
  --path PATH        location to output answers
  --level LEVEL      number of dictionary a matched word should appear in
  --stdout
  --pangrams         List all pangram words
  --command COMMAND  which command to run (e.g. play, pangrams)
  --words WORDS      directory of word files to use
```

## Word lists

This application does not come with the word list files you need. You can find several different sources for words in the language of your choice.

Note: files should contain one word per line

Some possible lists to use:

* https://www.keithv.com/software/wlist/
* https://github.com/dwyl/english-words
* https://github.com/first20hours/google-10000-english
* http://www.gwicks.net/dictionaries.htm
* https://www.mit.edu/~ecprice/wordlist.10000
* https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt