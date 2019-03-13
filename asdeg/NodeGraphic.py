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

from asdeg.Node import *
from asdeg.PathGraphic import *


class NodeGraphic:

    def __init__(self, node: Node, show_heuristic: bool):
        self._node = node
        self._show_heuristic = show_heuristic
        self._marker = None
        self._text_heuristic = None
        self._text_heuristic2 = None
        self._text_name = None
        self._path_graphics = []
        self._color = None
        for p in node.out_paths:
            self._path_graphics.append(PathGraphic(p))

    @property
    def path_graphics(self) -> List[PathGraphic]:
        return self._path_graphics

    @property
    def node(self):
        return self._node

    def mark(self, color):
        self._color = color

    def reset(self):
        self._color = None

    def draw(self, canvas: ScaledCanvas, filter_color=None):
        if (not filter_color and not self._color) or filter_color == self._color:
            coordinates = canvas.transform(self._node.x, self._node.y)
            color = (self._color if self._color else 'red')
            self._marker = canvas.create_oval(coordinates[0]-10, coordinates[1]-10, coordinates[0]+10, coordinates[1]+10, fill=color, width=0)
            self._text_name = canvas.create_text(coordinates[0], coordinates[1], text=self._node.name, fill="white")
            if self._node.heuristic is not None and self._show_heuristic:
                self._text_heuristic = canvas.create_text(coordinates[0] - 1, coordinates[1] - 11, text=str(self._node.heuristic), fill="black", font=("Sans Serif", 12, ""))
                self._text_heuristic2 = canvas.create_text(coordinates[0], coordinates[1] - 10, text=str(self._node.heuristic), fill="white", font=("Sans Serif", 12, ""))
        for pg in self._path_graphics:
            pg.draw(canvas, filter_color)

    def undraw(self, canvas: ScaledCanvas):
        canvas.delete(self._marker)
        canvas.delete(self._text_heuristic)
        canvas.delete(self._text_heuristic2)
        canvas.delete(self._text_name)
        for p in self._path_graphics:
            p.undraw(canvas)
