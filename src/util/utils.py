from datetime import date
from os import path
from string import punctuation
from rich.console import Console
from customtkinter import *
from collections import Counter

console = Console()


def closeApp(app, event):
    app.destroy()


def countLines(data: str):
    lines = [line for line in data.splitlines() if line.strip()]
    return lines, len(lines)


def countSymbols(lines: [str]) -> int:
    totalSymbols = 0
    for line in lines:
        symbolsInLine = len(line)
        totalSymbols += symbolsInLine
    return totalSymbols


def countWords(lines: [str]) -> int:
    totalWords = 0
    for line in lines:
        wordsInLine = line.split()
        totalWords += len(wordsInLine)
    return totalWords


def getPopularWords(lines: [str]) -> dict:
    words = Counter(
        word.strip(punctuation).lower()
        for line in lines
        for word in line.split()
        if word
    )
    return {word.capitalize(): count for word, count in words.items()}


def getCurrentMetrics(text: str) -> tuple[int, int, int, int]:
    lines, linesCount = countLines(text)
    symbolsCount = countSymbols(lines)
    wordsCount = countWords(lines)
    readingTimeMinutes = wordsCount / 200
    timeToRead = f"{readingTimeMinutes:.2f} min"

    return lines, linesCount, symbolsCount, wordsCount, timeToRead


def getTextFromFile() -> str:
    filePath = CTkInputDialog(text="Enter file path", title="Load Text").get_input()
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            textFromFile = file.read()
    except:
        console.log("Failed to read text from file")

    return textFromFile


def generateFileName(text: str) -> str:
    words = text.split(" ")
    firstTwoWords = "_".join(words[:2])
    currentTime = date.today().strftime("%d_%m_%Y")
    fileName = f"{firstTwoWords}_{currentTime}"

    return fileName


def saveCurrentText(text: str) -> None:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    currentDir = path.dirname(path.abspath(__file__))
    dataFile = path.join(currentDir, "..", "..", "data", "latest.md")
    with open(dataFile, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
