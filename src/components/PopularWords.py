from customtkinter import *

from util.utils import getPopularWords


class PopularWords(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Most Popular Words")
        self.geometry("400x400")
        self.resizable(False, False)
        self.iconbitmap("public/logo.ico")

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
        with open("data/latest.md", "r") as f:
            for line in f:
                words.extend(line.split())

        popularWords = getPopularWords(words)

        for word, frequency in popularWords.items():
            CTkLabel(self.wordsContainer, text=f"{word}: {frequency}").pack(
                padx=5, anchor="w"
            )
