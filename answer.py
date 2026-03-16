import numpy as np
import nltk
nltk.download('words')
from nltk.corpus import words

def initialize_answer(word_length=np.random.randint(1,26)):
    """
    Generates a word from the NLTK list of random words fitting the desired (or default random) list of words

    word_length - determines how long we want a word to be, by defualt its random between 1 and 26 but it can be changed for testing sake

    random_word - Returns a list of chars of length equal to word_length
    """
    full_word_list = words.words('en') # gets every word from the nltk import into a list

    final_list = []
    # trims out words not matching the desired length
    for w in full_word_list:
        # check length of word
        if len(w) == word_length:
            final_list.append(w) #append if appropriate length

    # pick a random index between 0 and the new length of the word to get a random word of desired length
    random_word = final_list[np.random.randint(0,len(final_list)-1)].lower()

    return [char for char in random_word]


