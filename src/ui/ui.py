from customtkinter import *
from rich.console import Console

console = Console()


from util.utils import getCurrentMetrics, showPopularWords


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
        text=f"Time to read: {timeToRead} min" if timeToRead else "No words found"
    )


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

    return interactWithTextHeading, showMostPopularWordsButton, loadTextFromFileButton


def renderMainTab(root) -> None:
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
    ) = renderButtonsSection(root)

    showMostPopularWordsButton.configure(
        command=lambda: showPopularWords(getTextInput.get("0.0", "end"))
    )
    loadTextFromFileButton.configure(
        command=lambda: console.print("TODO: load text from file")
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
