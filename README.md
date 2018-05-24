# Hangman-AI
Hangman AI

Build instructions:
python3 hangman.py

This runs the program


To exit control c, I couldn't get keyboard working,
added functionality will be added later.

Code makes a list out of a commonwords file sorted
by frequency, and then bases its guesses on commonwords,
this makes it hard to get some lyrics but always works on
the simple word based lyrics.

The code checks if one of the words in the state has one left,
if it does, it tries to match it with the first word it finds from the 
words list. If it doesn't find a word, it makes a guess based off
of letter frequency of all the possible words that the state can 
be. 

Every guess, it resizes the wordlist so that it eliminates the 
words that it can't be based on the letters filled in. Through 
this it narrows in on a good guess.
