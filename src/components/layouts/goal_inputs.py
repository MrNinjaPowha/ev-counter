from tkinter import Misc

from components.blocks.ev_input import EVInput
from variable_handler import VariableHandler


class GoalInputs:
    """A column of 6 tkinter entries that only accepts numbers between 0 and 255."""
    def __init__(
            self, master: Misc, variable_handler: VariableHandler, first_row: int = 0, column: int = 0
    ):
        self._inputs = []
        for i in range(6):
            self._inputs.append(EVInput(master, variable_handler, 'goals', i))
            self._inputs[i].grid(row=first_row + i, column=column)
