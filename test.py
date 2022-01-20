from statistics import mean
from solver import WordleSolver
from wordle import WordlePuzzle
import time

def parseWordList(filename):
    return [l.strip() for l in open(filename).readlines()]

def testSolver(dictionaryFile, testFile):
    print(f"Dictionary: {dictionaryFile}")
    print(f"Test Words: {testFile}")
    
    dictionary = parseWordList(dictionaryFile)
    testWords = parseWordList(testFile)
    solver = WordleSolver(dictionary, 5, 6)

    start = time.time()
    guessCounts = []
    for i, word in enumerate(testWords):
        if i % 100 == 0:
            print(f"{i}/{len(testWords)}")
        guesses = solver.solve(WordlePuzzle(word))
        guessCounts.append(len(guesses))
    end = time.time()

    print(f"Completed in {round(end-start, 2)} seconds")
    print(f"Mean # guesses across {len(testWords)} words: {round(mean(guessCounts), 2)}")

testSolver("wordle-words.txt", "wordle-words.txt")
