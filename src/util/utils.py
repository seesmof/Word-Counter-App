from collections import defaultdict
from math import ceil
from rich.console import Console

from components.AlertPopup import AlertPopup

console = Console()


def closeApp(app, event):
    app.destroy()


def countLines(data):
    lines = data.split("\n")
    lines = [line for line in lines if line != ""]
    return lines, len(lines)


def countSymbols(lines):
    res = 0
    for line in lines:
        symbolsInLine = 0
        for char in line:
            symbolsInLine += 1
        res += symbolsInLine
    return res


def countWords(lines):
    res = 0
    for line in lines:
        wordsInLine = line.split(" ")
        res += len(wordsInLine)
    return res


def getPopularWords(lines):
    words = defaultdict(int)
    for line in lines:
        wordsInLine = line.split(" ")
        for word in wordsInLine:
            if word not in {"", " ", ".", "!", "?", "-"}:
                words[word] += 1
    return words


def showPopularWords(text):
    console.log(
        f"Started calculating most popular words from a text with {len(text)} symbols..."
    )

    # TODO read below and implement
    # have a new window open where we would have a scrollable frame
    # in the scrollable frame we would write all our popular words
    # we will write from a list of custom objects from a class, that would have a word and a count
    # each object would have a string representation
    # or we could actually even have a class that would wrap our words container and do all the operations on them, not sure yet

    lines, _ = countLines(text)
    mostPopularWords = getPopularWords(lines)
    mostPopularWords = sorted(
        mostPopularWords.items(), key=lambda x: x[1], reverse=True
    )

    resultsString = "Most popular words in a given text:\n"
    for word in mostPopularWords:
        resultsString += f"  - {word[0]}: {word[1]}\n"
    AlertPopup(resultsString)

    console.log(f"Calculated {len(mostPopularWords)} most popular words")


def getCurrentMetrics(text) -> tuple[int, int, int, int]:
    lines, linesCount = countLines(text)
    symbolsCount = countSymbols(lines)
    wordsCount = countWords(lines)
    timeToRead = ceil(wordsCount / 200)

    return lines, linesCount, symbolsCount, wordsCount, timeToRead
