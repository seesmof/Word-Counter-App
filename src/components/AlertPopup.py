from customtkinter import *


class AlertPopup(CTkToplevel):
    def __init__(
        self, message: str = "Whoops... Something went wrong", title: str = "Alert"
    ):
        super().__init__()
        self.resizable(False, False)
        self.title(title)

        infoLabel = CTkLabel(self, text=message)
        infoLabel.pack(padx=8, pady=8, anchor="center")

        dismissButton = CTkButton(
            self,
            text="Okay",
            command=self.destroy,
            font=("Arial", 12, "bold"),
            width=60,
        )
        dismissButton.pack(padx=8, pady=8, anchor="e")

        self.grab_set()
        self.lift()
        self.bind("<Escape>", self.closePopup)

    def closePopup(self, event):
        self.destroy()
