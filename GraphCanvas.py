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

from GraphGraphic import *
from Solution import *
from Graph import *
from tkinter import *


class GraphCanvas(ScaledCanvas):
    def __init__(self, master: Frame = None, cnf=None, **kw):
        self._graph_graphic = None
        if 'show_heuristics' in kw:
            self._show_heuristics = kw['show_heuristics']
            kw.pop('show_heuristics')
        else:
            self._show_heuristics = False
        kw['bg'] = 'blue'

        super().__init__(master=master, cnf=cnf, **kw)

    @property
    def show_heuristics(self):
        return self._show_heuristics

    def draw(self, graph: Graph, solution: Solution = None):
        self._graph_graphic = GraphGraphic(graph, self._show_heuristics)
        self._graph_graphic.draw(self, solution)

    def undraw(self):
        if self._graph_graphic:
            self._graph_graphic.undraw(self)
            self._graph_graphic = None
