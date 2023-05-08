"""Run this script to start the program"""


from tkinter import Tk
from tkinter.ttk import Style

from src.window import Window


def main():
    """Initializes Tk root, ttk style and starts program"""
    root = Tk()
    root.title('Pokémon EV Counter')

    style = Style()
    style.theme_use('clam')
    style.configure('TEntry', padding=[6, 4])
    style.configure('TCombobox', padding=[6, 4])

    # Configure row and column to expand while keeping Window in the middle
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    Window(root, 'saved.pkl').grid()

    # Forces update to calculate window geometry before setting minsize
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()


if __name__ == '__main__':
    main()
