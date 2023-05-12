from tkinter import Misc, StringVar
from tkinter.ttk import Label
from typing import Literal

from src.helpers.color import rgb
from src.variable_handler import VariableHandler


class DifferenceLabel(Label):
    """A tkk label with a text variable that can be set with set_value(). The label will also change the textcolor
    depending on the value.
    """

    def __init__(self, master: Misc, variable_handler: VariableHandler, compare_variables: tuple[str, str]):
        self.variable_handler = variable_handler
        self.compare_variables = compare_variables

        self.colors: dict[Literal['equal', 'below', 'above'], str] = {
            'equal': rgb(0, 140, 20),
            'below': rgb(0, 0, 0),
            'above': rgb(190, 0, 0)
        }

        self._value = StringVar(master, '0')
        super().__init__(master, textvariable=self._value, foreground=self.colors.get('equal'))

        variable_handler.add_tracker(compare_variables[0], self.recalculate)
        variable_handler.add_tracker(compare_variables[1], self.recalculate)

    def recalculate(self):
        """Sets the text variable and changes the color depending on if the value is positive, negative, or zero."""
        difference = self.variable_handler.get_value(self.compare_variables[1]) - \
            self.variable_handler.get_value(self.compare_variables[0])

        self._value.set(str(difference))

        if difference == 0:
            self.configure(foreground=self.colors.get('equal'))
        elif difference > 0:
            self.configure(foreground=self.colors.get('below'))
        elif difference < 0:
            self.configure(foreground=self.colors.get('above'))
