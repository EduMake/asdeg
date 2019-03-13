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

from asdeg.ScaledCanvas import *
from asdeg.Path import *


class PathGraphic:
    def __init__(self, path: Path):
        self.path = path
        self.line = None
        self.label = None
        self.label2 = None
        self._color = None

    def mark(self, color):
        self._color = color

    def reset(self):
        self._color = None

    def draw(self, canvas: ScaledCanvas, filter_color=None):
        if (not filter_color and not self._color) or filter_color == self._color:
            color = (self._color if self._color else 'red')
            coordinates1 = canvas.transform(self.path.start.x, self.path.start.y)
            coordinates2 = canvas.transform(self.path.end.x, self.path.end.y)
            self.line = canvas.create_line(coordinates1[0], coordinates1[1], coordinates2[0], coordinates2[1], fill=color, width="5")
            canvas.lower(self.line)
            self.label = canvas.create_text((coordinates1[0]+coordinates2[0])/2, (coordinates1[1]+coordinates2[1])/2, text=str(self.path.distance), font=("Sans Serif", 11, ""))
            self.label2 = canvas.create_text((coordinates1[0]+coordinates2[0]-2)/2, (coordinates1[1]+coordinates2[1]-2)/2, text=str(self.path.distance), fill="white", font=("Sans Serif", 11, ""))

    def undraw(self, canvas: Canvas):
        canvas.delete(self.line)
        canvas.delete(self.label)
        canvas.delete(self.label2)
