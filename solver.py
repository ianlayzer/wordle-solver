from collections import defaultdict
from wordle import LetterColor, isSolved

class WordleSolver:
    def __init__(self, dictionary, numLetters, numGuesses):
        self.numLetters = numLetters
        self.numGuesses = numGuesses
        self.dictionary = self.createWordleDictionary(dictionary)
        self.candidates = self.dictionary

    def createWordleDictionary(self, englishDictionary):
        wordleDictionary = []
        for word in englishDictionary:
            if len(word) == self.numLetters:
                wordleDictionary.append(word)
        return wordleDictionary

    def solve(self, wordlePuzzle):
        guesses = []
        guessNum = 1
        while guessNum <= self.numGuesses:
            guess = self.getBestCandidate()
            guesses.append(guess)
            guessResult = wordlePuzzle.checkGuess(guess)
            if isSolved(guessResult):
                break
            self.pruneCandidates(guessResult)
            guessNum += 1
        self.candidates = self.dictionary # reset
        return guesses

    def getBestCandidate(self):
        # get counts of every letter throughout entire dictionary
        letterCounts = defaultdict(int)
        totalLetters = 0
        # get counts of every letter at each position
        indexToLetterToCount = defaultdict(lambda: defaultdict(int))
        for word in self.candidates:
            for i, letter in enumerate(word):
                letterCounts[letter] += 1
                indexToLetterToCount[i][letter] += 1
            totalLetters += len(word)

        # get word scores by summing scores of letters
        wordScores = {}
        for word in self.candidates:
            score = 0
            for i, letter in enumerate(word):
                # weight by frequency to favor more common letters to increase likelihood of yellow result
                letterFrequency = letterCounts[letter] / totalLetters
                letterScore = indexToLetterToCount[i][letter] * letterFrequency
                score += letterScore
            score *= len(set(list(word))) / len(word)
            wordScores[word] = score
        
        bestWord = max(wordScores, key=wordScores.get)
        return bestWord

    def pruneCandidates(self, guessResult):
        # handle green and yellow letters
        lettersInWord = set()
        for i, (letter, color) in enumerate(guessResult):
            if color == LetterColor.GREEN:
                lettersInWord.add(letter)
                newCandidates = []
                for word in self.candidates:
                    if word[i] == letter:
                        newCandidates.append(word)
                self.candidates = newCandidates
            elif color == LetterColor.YELLOW:
                lettersInWord.add(letter)
                newCandidates = []        
                for word in self.candidates:
                    if letter in word and word[i] != letter:
                        newCandidates.append(word)
                self.candidates = newCandidates
        # handle gray letters
        for i, (letter, color) in enumerate(guessResult):
            if color == LetterColor.GRAY and letter not in lettersInWord:
                newCandidates = []        
                for word in self.candidates:
                    if letter not in word:
                        newCandidates.append(word)
                self.candidates = newCandidates   
