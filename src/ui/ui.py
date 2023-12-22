from os import path
from customtkinter import *
from rich.console import Console

console = Console()


from util.utils import (
    generateFileName,
    getCurrentMetrics,
    getTextFromFile,
    saveCurrentText,
)
from components.AlertPopup import AlertPopup
from components.PopularWords import PopularWords


#! UI Sections
def renderInputSection(root) -> tuple[CTkLabel, CTkTextbox]:
    getTextHeading = CTkLabel(
        root, text="Enter text you want to count words in", font=("Arial", 14, "bold")
    )
    getTextInput = CTkTextbox(root, width=360, height=150)

    getTextHeading.place(x=0, y=0)
    getTextInput.place(x=0, y=30)

    return getTextHeading, getTextInput


def renderResultsSection(root) -> tuple[CTkLabel, CTkLabel, CTkLabel, CTkLabel]:
    resultsHeading = CTkLabel(root, text="Text Results", font=("Arial", 14, "bold"))
    resultsLines = CTkLabel(root, text="No lines found", font=("Arial", 13))
    resultsSymbols = CTkLabel(root, text="No symbols found", font=("Arial", 13))
    resultsWords = CTkLabel(root, text="No words found", font=("Arial", 13))
    resultsReadingTime = CTkLabel(root, text="No words found", font=("Arial", 13))

    resultsHeading.place(x=0, y=190)
    resultsLines.place(x=0, y=215)
    resultsSymbols.place(x=0, y=235)
    resultsWords.place(x=0, y=255)
    resultsReadingTime.place(x=0, y=275)

    return (
        resultsHeading,
        resultsLines,
        resultsSymbols,
        resultsWords,
        resultsReadingTime,
    )


def renderButtonsSection(root) -> tuple[CTkLabel, CTkButton, CTkButton, CTkButton]:
    interactWithTextHeading = CTkLabel(
        root,
        text="Text Interactions",
        font=("Arial", 14, "bold"),
    )
    showMostPopularWordsButton = CTkButton(
        root,
        text="Show Popular Words",
        font=("Arial", 12, "bold"),
    )
    loadTextFromFileButton = CTkButton(
        root,
        text="Load Text From File",
        font=("Arial", 12, "bold"),
    )
    saveTextToFileButton = CTkButton(
        root,
        text="Save Text To File",
        font=("Arial", 12, "bold"),
    )

    interactWithTextHeading.place(x=210, y=190)
    showMostPopularWordsButton.place(x=210, y=220)
    loadTextFromFileButton.place(x=210, y=260)
    saveTextToFileButton.place(x=210, y=300)

    return (
        interactWithTextHeading,
        showMostPopularWordsButton,
        loadTextFromFileButton,
        saveTextToFileButton,
    )


#! UI Functions
def updateMetrics(
    text: str,
    linesHeading: CTkLabel,
    symbolsHeading: CTkLabel,
    wordsHeading: CTkLabel,
    timeHeading: CTkLabel,
) -> None:
    (
        _,
        linesCount,
        symbolsCount,
        wordsCount,
        timeToRead,
    ) = getCurrentMetrics(text)

    linesHeading.configure(
        text=f"Lines: {linesCount}" if linesCount else "No lines found"
    )
    symbolsHeading.configure(
        text=f"Symbols: {symbolsCount}" if symbolsCount else "No symbols found"
    )
    wordsHeading.configure(
        text=f"Words: {wordsCount}" if wordsCount else "No words found"
    )
    timeHeading.configure(
        text=f"Reading Time: {timeToRead}" if timeToRead else "No words found"
    )

    saveCurrentText(text)


def loadTextFromFile(
    textField: CTkTextbox,
    resultsLines: CTkLabel,
    resultsSymbols: CTkLabel,
    resultsWords: CTkLabel,
    resultsReadingTime: CTkLabel,
) -> None:
    textFromFile = getTextFromFile()
    textField.insert("0.0", textFromFile)
    updateMetrics(
        textFromFile, resultsLines, resultsSymbols, resultsWords, resultsReadingTime
    )


def showPopularWords(text):
    popularWordsWindow = PopularWords()
    popularWordsWindow.updateWords()


def saveTextToFile(text):
    try:
        fileName = generateFileName(text)
        currentDir = path.dirname(path.abspath(__file__))
        filePath = path.join(currentDir, "..", "..", "data", fileName + ".md")
    except Exception as e:
        console.log(
            "Failed to save text to file, most likely due to input field being empty"
        )
        AlertPopup(
            "Could not save text to file. Make sure the input field is not empty."
        )
        return

    _, linesCount, symbolsCount, wordsCount, _ = getCurrentMetrics(text)
    metaData = f"""---
words: {wordsCount}
lines: {linesCount}
symbols: {symbolsCount}
---
"""
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(metaData)
        f.write("\n")
        f.write(text)


#! UI Tabs
def renderMainTab(root) -> CTkTextbox:
    getTextHeading, getTextInput = renderInputSection(root)

    (
        resultsHeading,
        resultsLines,
        resultsSymbols,
        resultsWords,
        resultsReadingTime,
    ) = renderResultsSection(root)

    (
        interactWithTextHeading,
        showMostPopularWordsButton,
        loadTextFromFileButton,
        saveTextToFileButton,
    ) = renderButtonsSection(root)

    showMostPopularWordsButton.configure(
        command=lambda: showPopularWords(getTextInput.get("0.0", "end"))
    )
    loadTextFromFileButton.configure(
        command=lambda: loadTextFromFile(
            getTextInput, resultsLines, resultsSymbols, resultsWords, resultsReadingTime
        )
    )
    saveTextToFileButton.configure(
        command=lambda: saveTextToFile(getTextInput.get("0.0", "end"))
    )

    getTextInput.bind(
        "<KeyRelease>",
        lambda event: updateMetrics(
            getTextInput.get("0.0", "end"),
            resultsLines,
            resultsSymbols,
            resultsWords,
            resultsReadingTime,
        ),
    )

    currentDir = path.dirname(path.abspath(__file__))
    dataFile = path.join(currentDir, "..", "..", "data", "latest.md")

    with open(dataFile, "r", encoding="utf-8") as f:
        loadedText = f.read()
        getTextInput.insert("0.0", loadedText)
        updateMetrics(
            loadedText,
            resultsLines,
            resultsSymbols,
            resultsWords,
            resultsReadingTime,
        )
