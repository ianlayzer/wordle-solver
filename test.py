from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter
from solver import WordleSolver
from wordle import WordlePuzzle

def parseWordList(filename):
    return [l.strip() for l in open(filename).readlines()]

def testWord(word):
    solver = WordleSolver(parseWordList("wordle-words.txt"), 5)
    print(solver.solve(WordlePuzzle(word)))

def testSolver(dictionaryFile, testFile):
    print(f"Dictionary: {dictionaryFile}")
    print(f"Test Words: {testFile}")
    
    dictionary = parseWordList(dictionaryFile)
    testWords = parseWordList(testFile)
    solver = WordleSolver(dictionary, 5)

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
    
    guessCounter = Counter(guessCounts)
    x = [num for num in guessCounter]
    y = [guessCounter[num] for num in guessCounter]
    plt.bar(x, y)
    plt.xlabel("Number of guesses")
    plt.ylabel("Occurrences")
    plt.show() 

testSolver("wordle-words.txt", "wordle-words.txt")
