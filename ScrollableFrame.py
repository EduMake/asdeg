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

# This module adapted from original code by Fredrik Lundh

from tkinter import *
from AutoScrollbar import *


class ScrollableFrame(Frame):
    def __init__(self, top, *args, **kwargs):
        Frame.__init__(self, top, *args, **kwargs)

        h_scrollbar = AutoScrollbar(self, orient=HORIZONTAL)
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        v_scrollbar = AutoScrollbar(self, orient=VERTICAL)
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        self._canvas = Canvas(self, xscrollcommand=h_scrollbar.set,
                              yscrollcommand=v_scrollbar.set)
        self._canvas.grid(row=0, column=0, sticky='nsew')

        h_scrollbar.config(command=self._canvas.xview)
        v_scrollbar.config(command=self._canvas.yview)

        # Make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the canvas contents
        self._frame = Frame(self._canvas)
        self._frame.rowconfigure(1, weight=1)
        self._frame.columnconfigure(1, weight=1)

        self._canvas.create_window(0, 0, window=self._frame, anchor='nw')
        self._frame.bind('<Configure>', self.frame_changed)

    def frame_changed(self, event):
        del event
        self._frame.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox('all'))
