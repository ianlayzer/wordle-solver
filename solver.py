from collections import defaultdict
from wordle import WordlePuzzle, LetterColor, isSolved
from statistics import mean

class WordleSolver:
    def __init__(self, englishDictionary, numLetters, numGuesses):
        self.numLetters = numLetters
        self.numGuesses = numGuesses
        self.dictionary = self.createWordleDictionary(englishDictionary)

        self.candidates = self.dictionary
        self.guessResults = []

    def createWordleDictionary(self, englishDictionary):
        wordleDictionary = []
        for word in englishDictionary:
            if len(word) == self.numLetters:
                wordleDictionary.append(word)
        return wordleDictionary

    def solve(self, wordlePuzzle):
        guesses = []
        # score all words
        guessNum = 1
        while guessNum <= self.numGuesses:
            guess = self.getBestCandidate()
            guesses.append(guess)
            guessResult = wordlePuzzle.checkGuess(guess)
            if isSolved(guessResult):
                break
            self.pruneCandidates(guessResult)
            guessNum += 1

        return guesses

    def getBestCandidate(self):
        # get letter scores
        letterCounts = defaultdict(int)
        totalLetters = 0
        indexToLetterToScore = defaultdict(lambda: defaultdict(int))
        for word in self.candidates:
            for i, letter in enumerate(word):
                letterCounts[letter] += 1
                indexToLetterToScore[i][letter] += 1
            totalLetters += len(word)

        # get word scores
        wordScores = {}
        for word in self.candidates:
            score = 0
            for i, letter in enumerate(word):
                score += indexToLetterToScore[i][letter] * letterCounts[letter] / totalLetters
            score *= len(set(list(word))) / len(word)
            wordScores[word] = score
        
        bestWord = max(wordScores, key=wordScores.get)
        return bestWord

    def pruneCandidates(self, guessResult):
        # handle green letters
        lettersInWord = set()
        for i, (letter, color) in enumerate(guessResult):
            if color == LetterColor.GREEN:
                lettersInWord.add(letter)
                newCandidates = []
                for word in self.candidates:
                    if word[i] == letter:
                        newCandidates.append(word)
                self.candidates = newCandidates
        # handle yellow letters
        for i, (letter, color) in enumerate(guessResult):
            if color == LetterColor.YELLOW:
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
            
wordleWords = [l.strip() for l in open("wordle-words.txt").readlines()]

guessCounts = []
for word in wordleWords:
    solver = WordleSolver(wordleWords, 5, 6)
    guesses = solver.solve(WordlePuzzle(word))
    guessCounts.append(len(guesses))

print(f"Average number of guesses: {mean(guessCounts)}")