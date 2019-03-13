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

from Solution import *
from ScrollableFrame import *
from StepGrid import StepGrid
from TableGrid import *
from SolutionSubGrid import *

class SolutionGrid(ScrollableFrame):
    def __init__(self, master: Frame, include_dijkstra: bool=None, include_a_star: bool =None):
        super().__init__(master)
        self._dijkstra_grid = None
        self._a_star_grid = None
        self._graph = None
        if include_dijkstra is None and include_a_star is None:
            include_a_star = True
            include_dijkstra = True
        if include_dijkstra:
            self._dijkstra_grid = SolutionSubGrid(self, 0, False)
        if include_a_star :
            self._a_star_grid  = SolutionSubGrid(self, 2 if include_dijkstra else 0, True)
        self._row = 0

    @property
    def frame(self):
        return self._frame

    @property
    def dijkstra_grid(self):
        return self._dijkstra_grid

    @property
    def a_star_grid(self):
        return self._a_star_grid

    def pre_step(self):
        if self._dijkstra_grid and self._a_star_grid:
            label = Label(self._frame, text="   ")
            label.grid(column=1, row=self._row, sticky="new")
        self._row += 1

    def post_step(self):
        spacer = Label(self._frame, text=" ")
        spacer.grid(row=self._row, column=0, columnspan= 3 if self._dijkstra_grid and self._a_star_grid else 1)
        self._row += 1
        self.update()

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        for c in self._frame.grid_slaves():
            c.grid_remove()
            c.destroy()
        self._graph = graph
        if self._dijkstra_grid:
            self._dijkstra_grid.graph = graph
        if self._a_star_grid:
            self._a_star_grid.graph = graph
        self._row = 0

#    @property
#    def iteration(self) -> int:
#        return self._iteration
