from nltk import download
from nltk.corpus import words
from collections import defaultdict
from wordle import WordlePuzzle, LetterColor


class WordleSolver:
    def __init__(self, englishDictionary, numLetters, numGuesses):
        self.numLetters = numLetters
        self.numGuesses = numGuesses
        self.dictionary = self.createWordleDictionary(englishDictionary)

        self.scores = defaultdict(defaultdict)

    def createWordleDictionary(self, englishDictionary):
        wordleDictionary = []
        for word in englishDictionary:
            if len(word) == self.numLetters:
                wordleDictionary.append(word.lower())
        return wordleDictionary

    def solve(self, wordlePuzzle):
        guesses = []
        # score 
        print(self.dictionary)


        return guesses





# solver = WordleSolver(words.words(), 5, 6)
# solver.solve("proxy")