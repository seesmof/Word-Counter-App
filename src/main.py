from rich import print
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.markdown import Markdown as md
from customtkinter import *
from collections import defaultdict

from components.AlertPopup import AlertPopup
from util.main import *

install()
console = Console()


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
    return lines, linesCount, symbolsCount, wordsCount


def updateMetrics(
    text: str, linesHeading: CTkLabel, symbolsHeading: CTkLabel, wordsHeading: CTkLabel
) -> None:
    _, linesCount, symbolsCount, wordsCount = getCurrentMetrics(text)

    linesHeading.configure(
        text=f"Lines: {linesCount}" if linesCount else "No lines found"
    )
    symbolsHeading.configure(
        text=f"Symbols: {symbolsCount}" if symbolsCount else "No symbols found"
    )
    wordsHeading.configure(
        text=f"Words: {wordsCount}" if wordsCount else "No words found"
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

    resultsHeading.place(x=0, y=190)
    resultsLines.place(x=0, y=215)
    resultsSymbols.place(x=0, y=235)
    resultsWords.place(x=0, y=255)

    return resultsHeading, resultsLines, resultsSymbols, resultsWords


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

    resultsHeading, resultsLines, resultsSymbols, resultsWords = renderResultsSection(
        root
    )

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
            getTextInput.get("0.0", "end"), resultsLines, resultsSymbols, resultsWords
        ),
    )


def configureApp() -> CTk:
    app = CTk()

    app.geometry("380x560")
    app.resizable(False, False)
    app.title("Word Counter App")

    app.bind("<Escape>", lambda event: closeApp(app, event=event))
    set_default_color_theme("dark-blue")
    app.grab_set()
    app.lift()

    return app


def configureTabsContainer(app: CTk) -> CTkTabview:
    tabsContainer = CTkTabview(app)
    tabsContainer.add("Analyze Text")
    tabsContainer.pack(expand=True, fill="both")

    return tabsContainer


def main() -> None:
    app = configureApp()

    tabsContainer = configureTabsContainer(app)
    mainTab = tabsContainer.tab("Analyze Text")

    renderMainTab(mainTab)
    app.mainloop()


if __name__ == "__main__":
    main()
