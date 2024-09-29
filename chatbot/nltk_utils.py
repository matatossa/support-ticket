import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def tokenize(sentence):
   
    return nltk.word_tokenize(sentence)


def reduce(word):
  
    return lemmatizer.lemmatize(stemmer.stem(word.lower()))


def bag_of_words(tokenized_sentence, words):
    
    
    sentence_words = [reduce(word) for word in tokenized_sentence]
   
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag