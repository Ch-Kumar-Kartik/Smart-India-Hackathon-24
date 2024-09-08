import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenize the input sentence using NLTK's word_tokenize.
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Stem a word using the Porter stemmer.
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """
    Create a bag-of-words representation of the tokenized sentence.
    
    tokenized_sentence: List of words from the input sentence.
    words: List of all words from the training data.
    
    Returns a NumPy array of shape (len(words),) with 1s and 0s indicating presence of words.
    """
    sentence_words = [stem(word) for word in tokenized_sentence]  # Stem each word
    bag = np.zeros(len(words), dtype=np.float32)  # Initialize bag with zeros
    
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1  # Set 1 if the word is present in the sentence
    
    return bag
