from tkinter import Misc, BooleanVar
from tkinter.ttk import Frame, Checkbutton
from src.components import GenerationMenu, ItemMenu, EVCounter
from src.components.layouts.save_form import SaveForm
from src.variable_handler import VariableHandler


class Window(Frame):
    """The main ttk frame for the program"""
    def __init__(self, master: Misc, data_dir: str):
        super().__init__(master, padding=5, relief='raised')
        variable_handler = VariableHandler(data_dir)

        self.generation_menu = GenerationMenu(self, variable_handler)
        self.generation_menu.grid(sticky='EW')

        self.item_menu = ItemMenu(self, variable_handler)
        self.item_menu.grid(row=1, sticky='EW')
        self.item_menu.configure(width=14)

        SaveForm(self, variable_handler).grid(row=0, column=1, rowspan=2, sticky='NS')

        self.has_pokerus = BooleanVar(self, False)
        Checkbutton(
            self, text='Has PokéRus', variable=self.has_pokerus,
            command=lambda: variable_handler.set_value('has_pokerus', self.has_pokerus.get())
        ).grid(row=2, sticky='W')
        variable_handler.add_tracker(
            'has_pokerus', lambda: self.has_pokerus.set(variable_handler.get_value('has_pokerus'))
        )

        self.ev_counter = EVCounter(
            self, variable_handler
        )
        self.ev_counter.grid(row=3, column=0, columnspan=3)
    