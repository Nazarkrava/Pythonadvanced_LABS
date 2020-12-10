import tkinter as tk
from tkinter.ttk import *


class TableClass(tk.Frame):
    def __init__(self, parent=None, hidden_columns=tuple(), headings=tuple(), rows=list(), grid=dict()):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid = grid
        self.hidden_cols_len = len(hidden_columns)
        self.cols = (hidden_columns + headings)
        self._init_table(rows)

    def _init_table(self, rows):
        self.table = Treeview(self.parent, columns=self.cols, show='headings', selectmode='browse')
        for col in self.cols:
            self.table.heading(col, text=col)
        self.table["displaycolumns"] = self.cols[self.hidden_cols_len:]
        self.table.grid(row=self.grid['row'], column=self.grid['column'], columnspan=self.grid['columnspan'],
                        sticky='NESW')
        self.insert(rows)

        self.table.bind('<ButtonRelease-1>', self.get_selected_item)

    def get_selected_item(self, event=None):
        cur_item = self.table.focus()
        values = self.table.item(cur_item)['values']
        return values

    def insert(self, rows):
        for values in rows:
            self.table.insert("", "end", values=values)

    def clear(self):
        self.table.delete(*self.table.get_children())

    def update_table(self, rows):
        self.clear()
        self.insert(rows)
