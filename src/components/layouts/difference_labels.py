from tkinter import Misc

from components.blocks.difference_label import DifferenceLabel
from variable_handler import VariableHandler


class DifferenceLabels:
    """A column of 6 tkinter labels that display the difference of the ev inputs and goal inputs. The labels will also
    change color depending on if the value is above, below, or exactly zero.
    """
    def __init__(self, master: Misc, variable_handler: VariableHandler, first_row: int = 0, column: int = 0):
        self.variable_handler = variable_handler

        self._labels = []
        for i in range(6):
            self._labels.append(DifferenceLabel(master))
            self._labels[i].grid(row=first_row + i, column=column)
            variable_handler.add_tracker(f'evs:{i}', lambda stat=i: self.update(stat))
            variable_handler.add_tracker(f'goals:{i}', lambda stat=i: self.update(stat))

    def update(self, stat: int):
        """Recalculates the difference of a stat."""
        self._labels[stat].set_value(
            self.variable_handler.get_value(f'goals:{stat}') - self.variable_handler.get_value(f'evs:{stat}')
        )
