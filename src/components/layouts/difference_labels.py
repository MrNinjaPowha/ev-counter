from tkinter import Misc

from components.blocks.difference_label import DifferenceLabel
from variable_handler import VariableHandler


class DifferenceLabels:
    def __init__(self, master: Misc, variable_handler: VariableHandler, first_row: int = 0, column: int = 0):
        self.variable_handler = variable_handler

        self._labels = []
        for i in range(6):
            self._labels.append(DifferenceLabel(master))
            self._labels[i].grid(row=first_row + i, column=column)
            variable_handler.add_tracker(f'evs:{i}', lambda stat=i: self.update(stat))
            variable_handler.add_tracker(f'goals:{i}', lambda stat=i: self.update(stat))

    def update(self, stat: int):
        self._labels[stat].set_value(
            self.variable_handler.get_value(f'goals:{stat}') - self.variable_handler.get_value(f'evs:{stat}')
        )
