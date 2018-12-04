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


class ScaledCanvas(Canvas):
    DEFAULT_HEIGHT = 368
    DEFAULT_WIDTH = 512

    def __init__(self, master: Frame=None, cnf=None, **kw):
        kw['height'] = ScaledCanvas.DEFAULT_HEIGHT
        kw['width'] = ScaledCanvas.DEFAULT_WIDTH
        self.min_x = 99999
        self.min_y = 99999
        self.max_x = -99999
        self.max_y = -99999
        super().__init__(master=master, cnf=cnf, **kw)

    def expand_range(self, x, y, margin=0):
        if x - margin < self.min_x:
            self.min_x = x - margin
        if x + margin > self.max_x:
            self.max_x = x + margin
        if y - margin < self.min_y:
            self.min_y = y - margin
        if y + margin > self.max_y:
            self.max_y = y + margin

    def transform(self, x, y):
        larger = max(self.max_x - self.min_x, self.max_y - self.min_y)
        scale = min(self.winfo_width(), self.winfo_height())
        offset_x = (self.winfo_width() - scale) / 2
        offset_y = (self.winfo_height() - scale) / 2
        return_x = (x - self.min_x) / larger * scale + offset_x
        return_y = (y - self.min_y) / larger * scale + offset_y
        return return_x, return_y
