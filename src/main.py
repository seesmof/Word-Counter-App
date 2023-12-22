from rich.traceback import install
from customtkinter import *

install()

from util.utils import *
from ui.ui import *


def configureApp() -> CTk:
    app = CTk()

    app.geometry("380x390")
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
