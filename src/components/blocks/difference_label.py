from tkinter import Misc, StringVar
from tkinter.ttk import Label
from typing import Literal

from src.helpers.color import rgb


class DifferenceLabel(Label):
    """A tkk label with a text variable that can be set with set_value(). The label will also change the textcolor
    depending on the value.
    """
    def __init__(self, master: Misc):
        self.colors: dict[Literal['equal', 'below', 'above'], str] = {
            'equal': rgb(0, 140, 20),
            'below': rgb(0, 0, 0),
            'above': rgb(190, 0, 0)
        }

        self._value = StringVar(master, '0')
        super().__init__(master, textvariable=self._value, foreground=self.colors.get('equal'))

    def set_value(self, value: int):
        """Sets the text variable and changes the color depending on if the value is positive, negative, or zero."""
        self._value.set(str(value))

        if value == 0:
            self.configure(foreground=self.colors.get('equal'))
        elif value > 0:
            self.configure(foreground=self.colors.get('below'))
        elif value < 0:
            self.configure(foreground=self.colors.get('above'))
