from enum import Enum
from collections import Counter, defaultdict

class LetterColor(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    GRAY = "gray"

    def __repr__(self):
        return self.value

class WordlePuzzle:
    def __init__(self, targetWord):
        self.targetWord = targetWord
        self.targetCounter = Counter(self.targetWord)
    
    def checkGuess(self, guess):
        result = [None for _ in range(len(guess))]        
        greenCounts = defaultdict(int)
        for i, letter in enumerate(guess):
            if letter == self.targetWord[i]:
                result[i] = LetterColor.GREEN
                greenCounts[letter] += 1
            elif letter not in self.targetWord:
                result[i] = LetterColor.GRAY

        currCounts = defaultdict(int)
        for i, letter in enumerate(guess):
            targetLetterCount = self.targetCounter[letter]
            currCounts[letter] += 1
            if result[i] != None:
                continue
            if greenCounts[letter] == targetLetterCount or currCounts[letter] > targetLetterCount:
                result[i] = LetterColor.GRAY
            elif currCounts[letter] <= targetLetterCount:
                result[i] = LetterColor.YELLOW
        return list(zip(guess, result))

def isSolved(guessResult):
    for letter, color in guessResult:
        if color != LetterColor.GREEN:
            return False
    return True       
