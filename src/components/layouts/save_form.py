from tkinter import Misc, messagebox
from tkinter.ttk import Frame, Button, Combobox

from variable_handler import VariableHandler


class SaveForm(Frame):
    def __init__(self, master: Misc, variable_handler: VariableHandler):
        super().__init__(master, padding=(10, 0, 0, 0))

        self.variable_handler = variable_handler

        self.saves_combobox = Combobox(self, values=variable_handler.get_saved_pokemons())
        self.saves_combobox.grid(row=0, column=0, padx=4)
        self.saves_combobox.bind('<<ComboboxSelected>>', self.load_pokemon)

        Button(self, text='Save', command=self.save_pokemon).grid(row=0, column=1)

    def save_pokemon(self):
        name = self.saves_combobox.get()

        if not name:
            messagebox.showerror('Error', 'You need to give the saved Pokémon a name!')
            return

        if not messagebox.askyesno('Save Pokémon', f'Save Pokémon {name}?'):
            return

        self.variable_handler.save_pokemon(name)

        # Updates the combobox options with the newly saved Pokémon
        if not self.saves_combobox['values']:
            self.saves_combobox['values'] = (name,)
        elif name not in self.saves_combobox['values']:
            self.saves_combobox['values'] += (name,)

    def load_pokemon(self, *_):
        name = self.saves_combobox.get()
        if messagebox.askyesno('Load Pokémon', f'Load Pokémon {name}?\n' 'This will override any unsaved evs.'):
            self.variable_handler.load_pokemon(name)
        else:
            self.saves_combobox.set('')
