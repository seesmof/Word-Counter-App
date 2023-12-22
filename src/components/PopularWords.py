from os import path
from customtkinter import *

from util.utils import getPopularWords


class PopularWords(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Most Popular Words")
        self.geometry("400x400")
        self.resizable(False, False)

        self.wordsContainer = CTkScrollableFrame(
            self,
            label_text="Most Popular Words",
            label_font=("Arial", 14, "bold"),
            border_color="",
        )
        self.wordsContainer.pack(expand=True, fill="both")

        self.grab_set()
        self.lift()
        self.bind("<Escape>", self.closeWindow)

    def closeWindow(self, event):
        self.destroy()

    def updateWords(self):
        for widget in self.wordsContainer.winfo_children():
            widget.destroy()

        words = []
        currentDir = path.dirname(path.abspath(__file__))
        dataFile = path.join(currentDir, "..", "..", "data", "latest.md")

        with open(dataFile, "r", encoding="utf-8") as f:
            for line in f:
                words.extend(line.split())

        popularWords = getPopularWords(words)
        sortedPopularWords = sorted(
            popularWords.items(), key=lambda x: x[1], reverse=True
        )
        sortedPopularWords = sortedPopularWords[:12]

        for word, frequency in sortedPopularWords:
            CTkLabel(self.wordsContainer, text=f"{word}: {frequency}").pack(
                padx=5, anchor="w"
            )
