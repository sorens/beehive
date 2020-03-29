# Beehive utility

This command-line utility helps generate the words for combination of letters or generate a list of pangram words

```bash
> ./beehive --help
usage: beehive [-h] [--letters LETTERS] [--center CENTER] [--debug]
               [--path PATH] [--level LEVEL] [--stdout] [--pangrams] --command
               COMMAND

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
```