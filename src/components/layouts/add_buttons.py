from math import floor
from tkinter import Misc
from tkinter.ttk import Frame, Button
from typing import Callable, Any


class AddButtons(Frame):
    """A ttk frame with 18 buttons in a 3x6 grid that can increase stats by the amount of that buttons column (1-3).

    The add_func(stat, value, shift_down) callback will be called on any button being pressed.
    """
    def __init__(self, master: Misc, add_func: Callable[[int, int, bool], Any]):
        super().__init__(master)

        self.add_func = add_func

        for i in range(18):
            button = Button(self, text=i % 3 + 1, width=1)
            button.grid(row=3+floor(i/3), column=1 + i % 3)
            button.bind('<Button-1>', lambda event, index=i: self.handle_click(index))
            button.bind('<Shift-Button-1>', lambda event, index=i: self.handle_click(index, True))

    def handle_click(self, button_index: int, shift_down: bool = False):
        """Handles the click event of the buttons."""
        stat = floor(button_index / 3)
        value = 1 + button_index % 3
        self.add_func(stat, value, shift_down)
