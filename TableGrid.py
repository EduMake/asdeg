# A* and Dijkstra Example Generator (ASDEG)
# Copyright (C) 2018 EduMake Limited and Stephen Parry
#
# This file is part of ASDEG (the A* and Dikstra Example Generator)
#
# ASDEG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASDEG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASDEG.  If not, see <https://www.gnu.org/licenses/>.

from tkinter import *


class TableGrid(Frame):

    def __init__(self, master: Frame, grid_color, back_color):
        super().__init__(master, bg=grid_color)
        self._grid_color = grid_color
        self._back_color = back_color
        self.columns = 0
        self.rows = 0

    def extend_to(self, new_rows, new_columns, ex_row=-1, ex_column=-1, ex_row_span=1, ex_column_span=1):
        if self.columns < new_columns:
            for c in range(self.columns, new_columns):
                for r in range(0, self.rows):
                    if not (ex_column <= c < ex_column + ex_column_span and ex_row <= r < ex_row + ex_row_span):
                        f = Frame(self, bg=self._back_color)
                        f.grid(column=c, row=r, padx=1, pady=1, sticky="nsew")
            self.columns = new_columns
        if self.rows < new_rows:
            for r in range(self.rows, new_rows):
                for c in range(0, self.columns):
                    if not (ex_column <= c < ex_column + ex_column_span and ex_row <= r < ex_row + ex_row_span):
                        f = Frame(self, bg=self._back_color)
                        f.grid(column=c, row=r, padx=1, pady=1, sticky="nsew")
            self.rows = new_rows

    def cell(self, row, column, row_span=1, column_span=1):
        for r in range(row, min(self.rows, row + row_span)):
            for c in range(column, min(self.columns, column + column_span)):
                for child in self.grid_slaves(row=r, column=c):
                    child.grid_remove()
                    child.destroy()
        self.extend_to(new_rows=row + row_span, new_columns=column + column_span, ex_row=row, ex_column=column, ex_row_span=row_span, ex_column_span=column_span)
        f = Frame(self, bg=self._back_color)
        f.grid(column=column, row=row, rowspan=row_span, columnspan=column_span, padx=1, pady=1, sticky="nsew")
        self.grid_columnconfigure(column, weight=1)
        return f

    def set_row_text(self, row, start_column, text, column_span=1, row_span=1, font=('Sans Serif', 11, ""), text_color=None, anchor='n'):
        if not text_color:
            text_color = self._grid_color
        c = start_column
        for s in text:
            ctl = Label(master=self.cell(row=row, column=c, row_span=row_span, column_span=column_span), text=str(s), anchor=anchor, font=font, bg=self._back_color, foreground=text_color)
            ctl.pack(fill=BOTH, expand=1)
            c += column_span
