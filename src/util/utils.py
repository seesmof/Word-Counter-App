from datetime import date
from math import ceil
from pathlib import Path
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
    words = Counter(word for line in lines for word in line.split() if word)
    return dict(words)


def getCurrentMetrics(text: str) -> tuple[int, int, int, int]:
    lines, linesCount = countLines(text)
    symbolsCount = countSymbols(lines)
    wordsCount = countWords(lines)
    timeToRead = ceil(wordsCount / 200)

    return lines, linesCount, symbolsCount, wordsCount, timeToRead


def readTextFromFile(filePath: str) -> str:
    try:
        text = Path(filePath).read_text()
    except FileNotFoundError:
        text = ""
        console.log(f"Failed to load text from {filePath}")

    return text


def getTextFromFile():
    filePath = CTkInputDialog(text="Enter file path", title="Load Text").get_input()
    textFromFile = readTextFromFile(filePath)

    return textFromFile


def generateFileName(text: str) -> str:
    words = text.split(" ")
    firstTwoWords = "_".join(words[:2])
    currentTime = date.today().strftime("%d_%m_%Y")
    fileName = f"{firstTwoWords}_{currentTime}"

    return fileName


def saveTextOnExit(text: str) -> None:
    text = [line.strip() for line in text.split("\n") if line.strip()]
    filePath = Path("data/latest.md")
    filePath.write_text("\n".join(text))
