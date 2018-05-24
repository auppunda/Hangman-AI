#!/usr/bin/python
import string
import random
import requests
import json

token = '0z9HX'
words = None
words_for_current_round = []
words_in_game = []
game_status = 1
frequency = {}

# removes all non _ or alpha characters from state
def filter(text):
	s = ""
	for c in text:
		if c.isalpha() or c ==' ' or c == '_':
			s += c
	return s

# checks if it follows format
def followsFormat(word, mark):
	if (len(word) - 1) != len(mark):
		return False
	for i in range(0, len(mark)):
		if mark[i].isalpha():
			if mark[i] != word[i]:
				return False
	return True

# resizes the words_for_current_round based off of guess
def resize(state):
	global words_for_current_round

	# formats the state string 
	str_words = state.split(" ")
	for i in range(0, len(str_words)):
		str_words[i] = filter(str_words[i])
	
	# resizes wordlist to narrow in based off of the guesses that have been made
	words_temp = []
	for word in words_for_current_round:
		word_good = False
		for c in str_words:
			word_good = followsFormat(word, c)
			if word_good:
				break
		if word_good:
			words_temp.append(word)

	words_for_current_round = words_temp

	# updates frequency
	for key in frequency:
		frequency[key] = 0

	for word in words_for_current_round:
		usedletters = []
		for c in word:
			if c != '\n' and c != ' ':
				if c in frequency and c not in usedletters:
					frequency[c] += 1
				usedletters.append(c)


# changes dict to be based of of state before any guesses made
def changeDict(words):

	# gets possible words list based off of state
	for word in words: 
		for a in words_in_game:
			if a == (len(word)-1):
				words_for_current_round.append(word)
				break
	
	# gets frequencies
	for word in words_for_current_round:
		usedletters = []
		for c in word:
			if c != '\n' and c != ' ' and c.isalpha():
				if c in frequency and c not in usedletters:
					frequency[c] += 1
				elif c not in usedletters:
					frequency[c] = 1
				usedletters.append(c)




#checks amount of _ left in a split state string
def amount_letters_left(hash):
	amount = 0
	for c in hash:
		if c == '_':
			amount += 1
	return amount

# gets guess when there is only one _ left
def getGuess(word):
	wis = ""
	global words_for_current_round
	for w in words_for_current_round:
		if followsFormat(w, word):
			wis = w
			break

	if wis == "":
		return 300

	words_temp = []
	for c in words_for_current_round:
		if c != wis:
			words_temp.append(c)

	words_for_current_round = words_temp

	c = wis[word.index('_')]
	for key in frequency:
		if key == c:
			frequency.pop(c, None)
			return c

	return 300

# gets overall guess for one iteration
def determine_guess(game, guesses):
	d = game.json()
	max = 0
	first = True
	max_key = ''
	str_words = d["state"].split(" ")
	for i in range(0, len(str_words)):
		str_words[i] = filter(str_words[i])
	# if guesses < 2:
	# 	for key in vowels:
	# 		if first:
	# 			max = vowels[key]
	# 			max_key = key
	# 			first = False
	# 		elif vowels[key] > max:
	# 			max = vowels[key]
	# 			max_key = key
	# 	vowels.pop(max_key, None)
	# 	return max_key

	for i in range(0, len(str_words)):
		if amount_letters_left(str_words[i]) == 1:
			a = getGuess(str_words[i])
			if(a == 300):
				continue

			frequency.pop(a, None)

			return a

	for key in frequency:
		if first:
			max = frequency[key]
			max_key = key
			first = False
		elif frequency[key] > max:
			max = frequency[key]
			max_key = key

	frequency.pop(max_key, None)
	return max_key

# makes post to upe 
def makeguess(c):
	print(c)
	g = "%c" % c
	guess = { "guess" : "%c" % g }
	game = requests.post("http://upe.42069.fun/%s" % token, data=guess)
	print (game.text)
	resize(game.json()['state'])
	return game

# starts game, puts in lengths for each word in state string in words_in_game
def start_game():
	games = requests.get("http://upe.42069.fun/%s" % token)
	d = games.json()
	s = d['state']
	w = s.split(' ')

	for i in range(0, len(w)):
		w[i] = filter(w[i])

	for item in w : 
		b = 0 
		if item != " ":
			for c in item:
				b = b + 1
			words_in_game.append(b)
	print (games.text)
	return games

#resets everything
def reset():
	s =  "http://upe.42069.fun/%s/reset" % token
	data = { "email" : "auppunda@g.ucla.edu"}
	game_e = requests.post(s, data=data)
	print(game_e.text)

# while loop to continuously run game
def main():
	#reset()
    #fo = open("words.txt", "r")
	fi = open("commonwords.txt", "r")
	global words
	global frequency
	global words_in_game
	words = list(fi)
	#common_words = list(fi)
	#words = list(fo)
	#reset()
	global words_for_current_round
	amount_guesses = 0
	i = 0
	while(1):
		game = start_game()
		#words_in_game = [1, 4]
		changeDict(words)
		
		while(game_status):	

			c = determine_guess(game, amount_guesses)
			amount_guesses += 1
			game = makeguess(c)
			d = game.json()
			if d["status"] == "DEAD" or d["status"] == "FREE":
				words_in_game = []
				words_for_current_round = []
				break
		




if __name__ == '__main__':
	main()
