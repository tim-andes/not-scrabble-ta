import math
import random
import fnmatch
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALPHA = VOWELS + CONSONANTS

HAND_SIZE = 7
n = HAND_SIZE
hand = {}

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """Loads a large list of words. The words are strings of lowercase letters.
    Depending on the size of the word list, this function may take a while to
    finish.
    
    Input: WORDLIST_FILENAME, which is the file words.txt
        Returns: List of words from which to play the game.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

word_list = load_words()


def get_frequency_dict(sequence):
    """Produces a histogram dictionary that will act as the player's hand and
    selection of letters from which they will submit their words.

    Input: sequence, string or list
        Returns: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
 	

def get_word_score(word, n):
    """
    Calculates the score for a word. Assumes the word is a valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.
    
    Inputs:
        word: string
        n: int >= 0
    
    Returns: int >= 0
    """
    
    word_score = 0
    
    for value in word.lower():
        if value in SCRABBLE_LETTER_VALUES:
            word_score += SCRABBLE_LETTER_VALUES[value]    
    hand_score = 7 * len(word) - 3 * (n - len(word))  
    if hand_score < 1:
        hand_score = 1
    score = word_score * hand_score
    print(f"Score for '{word}': {score}")
    return score
    

def display_hand(hand):
    """Displays the letters currently in the hand.

    For example:
        display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
        a x x l l l e
    The order of the letters is unimportant.

    Input: hand, dictionary (string -> int)
        Returns: Does not return, but prints hand for player to see.
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
              print("\t", letter, end = ' ')
    print()              


def deal_hand(n):
    """Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    Input: n, an int >= 0
        Returns: dictionary (string -> int)
    """
    
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand['*'] = 1
    if hand['*'] > 1:
        hand['*'] = 1
    
    return hand

hand = deal_hand(n)


def update_hand(hand, word):
    """Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    Inputs:        
        hand: dictionary (string -> int)    
        word: string
    
    Returns: dictionary (string -> int)
    """
    hand_cop = hand.copy()
    
    for w in word:
        if w in hand_cop:
            hand_cop[w] = hand_cop.get(w, 0) - 1
            if hand_cop[w] <= 0:
                del hand_cop[w]
    hand = hand_cop.copy()
    
    displ_hand = ''
    for k, v in hand.items():
        for i in range(v):
            displ_hand += k + ' '    
    return hand


def is_valid_word(word, hand, word_list):
    """Returns Valid = True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    Inputs:        
        hand: dictionary (string -> int)    
        word: string
        word_list: list of lowercase strings
    
    Returns: boolean
    """
    valid = False
    match = False
    
    def wildcard_check(word_list, word):
        word_copy = word.replace('*', '[aeiou]')
        filtered = fnmatch.filter(word_list, word_copy)
        if filtered:
            word = filtered
            return word
        else:
            print("\t...No word match found.")
    # If guessed word in hand, Match.    
    for w in word:
        if w in hand.keys():
            match = True
        else: 
            print("Guessed word does not match letters in-hand, try again.")
            return
    # If Match in word_list, valid answer.
    if match:
        # Wildcard check
        if '*' in word:
           print("Wildcard detected, finding any matching words...")           
           word = wildcard_check(word_list, word)
           if word:
               print(f"...Submitting word, '{word[0]}'")
               return word           
           if word == False or word == None:
               print(">>> Invalid word, try again.")
               print("-- Tip: If out of words, enter '!!'")
               return
            
        if word.lower() in word_list:
            valid = True
            print(">>> Valid word.")
        else:
            print(">>> Invalid word, try again.")
            print("-- Tip: If out of words, enter '!!'")
    return valid


def calculate_handlen(hand):
    """Returns the length (number of letters) in the current hand.
    
    Input: hand, a dictionary histogram (string : int)
        Returns: n, an integer
    """
    n = sum(hand.values())
    wc_check = hand.get('*', 0)
    if wc_check:
        n -= 1
    if n < 0:
        n = 0
    return n


def substitute_hand(hand, ALPHA):
    """Takes request to substitute a letter an executes request, then provides
    an updated hand.
    
    Inputs: hand, the current selection of letters.
        Returns: Updated hand with replaced letter.
    """
    rand_ALPHA = random.choice(ALPHA)
    
    while True:
        old_letter = input("Choose a letter to substitute: ")
        # see if selected letter is in hand, if not, ask again:
        try:
            if hand[old_letter]:
                break
        except:
            print("That letter is not in your hand.")
    
    while True:
        new_letter = rand_ALPHA
        # make sure new letter is not already in the hand:
        try:
            if new_letter not in hand:
                break
        except:
            new_letter = rand_ALPHA
    # replace old letter with new letter, keep initial value
    hand[new_letter] = hand.pop(old_letter)
    
    print(f">>> Removed '{old_letter}' and added '{new_letter}'.")
    return hand

         
def try_again_func(deal_hand):
    """Provides users with option to restart game.
   
    Input: deal_hand, passes through a new randomized hand, then initialized by
    "hand" to pass in to the play_hand function.
    
    Returns: nothing, simply invokes play_hand function to play again.
    """
    try_again = input("\nWould you like to play again? Type 'yes' or 'no' ... : ").lower()
    if try_again in ['yes', 'ye', 'y']:
        print("-- Good luck!\n")
        print("\n--------------------------------------\n")
        hand = deal_hand(n)
        play_hand(hand, word_list)
    elif try_again in ['no', 'n']:
        print("-- Until next time!")
        sys.exit()
    else:
        print("-- Until next time!")
        sys.exit()
        

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      Inputs:
          hand: dictionary (string -> int)
          word_list: list of lowercase strings
      
      Prints: Current Score or Final Score.      
    """

    print("\n\nWelcome to Not-Scrabble!")
    print("\n* * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("\n-- Submit a word you see in your hand.")
    print("-- You can only use letter substition once per turn.")
    print("-- The wildcard (*) can only be used in place of vowels.")
    print("\n-------------------------------------------------------")
    
    score = 0
    
    print("\nYour current hand:")    
    display_hand(hand)   
      
    # begin play loop
    while True:
        sub_letter_count = 0
        while True:
            if sub_letter_count < 1:
                sub_letter_inq = input("\nWould you like to replace a letter? 'yes' or 'no': ")            
                if sub_letter_inq in ['yes', 'ye', 'y']:
                    sub_letter_count += 1
                    substitute_hand(hand, ALPHA)
                    print("\n-------------------------------------------------------")
                    print("\nYour current hand:")
                    display_hand(hand)
                    break
                if sub_letter_inq in ['no', 'n']:
                    break
                print(">>> Invalid entry.")    
        word = input("Submit a word: ").lower()                 
        
        if word == "!!":
            print("\n\nEnding game...")
            print(f"\n>> Final Score: {score} <<")
            try_again_func(deal_hand)
        else: 
            if is_valid_word(word, hand, word_list):
                score += get_word_score(word, n)                
                print(f"\n> Current Score: {score} <")    
                hand = update_hand(hand, word)    
            print("\n-------------------------------------------------------")
            print("\nYour current hand:")
            display_hand(hand)
            
        if not hand or len(hand) <= 1:
            print("...Too few letters remain!")
            print(f"\n>> Final Score: {score} <<")
            try_again_func(deal_hand)
    
play_hand(hand, word_list)
