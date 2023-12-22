from collections import defaultdict
from datetime import date
from math import ceil
from rich.console import Console
from customtkinter import *

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


def getCurrentMetrics(text) -> tuple[int, int, int, int]:
    lines, linesCount = countLines(text)
    symbolsCount = countSymbols(lines)
    wordsCount = countWords(lines)
    timeToRead = ceil(wordsCount / 200)

    return lines, linesCount, symbolsCount, wordsCount, timeToRead


def readTextFromFile(filePath):
    try:
        with open(filePath, "r") as f:
            text = f.read()
    except Exception as e:
        console.print(e)
        text = ""
    return text


def getTextFromFile():
    getFilePath = CTkInputDialog(text="Enter file path", title="Load Text")
    filePath = getFilePath.get_input()
    textFromFile = readTextFromFile(filePath)

    return textFromFile


def generateFileName(text):
    words = text.split(" ")
    firstTwoWords = "_".join(words[:2])
    currentTime = date.today().strftime("%d_%m_%Y")
    fileName = f"{firstTwoWords}_{currentTime}"

    return fileName


def saveTextOnExit(text):
    text = [
        line for line in text.split("\n") if line != "" or line != "\n" or line != " "
    ]
    text.pop()
    console.print(text)
    filePath = f"data/latest.md"
    with open(filePath, "w") as f:
        f.write("\n".join(text))
