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


class SolutionGrid(ScrollableFrame):
    def __init__(self, master: Frame, include_dijkstra: bool=None, include_a_star: bool =None):
        super().__init__(master)
        if include_dijkstra is None and include_a_star is None:
            self._dijkstra_enabled = True
            self._a_star_enabled = True
        else:
            self._dijkstra_enabled = include_dijkstra
            self._a_star_enabled = include_a_star
        self._dijkstra_solution = None
        self._a_star_solution = None
        self._dijkstra_grids = []
        self._a_star_grids = []
        self._iteration = -1
        self._graph = None
        self._dijkstra_solved_at = -1
        self._a_star_solved_at = -1
        self._row = 0
        self._column = 0

    @property
    def dijkstra_solved_at(self) -> int:
        return self._dijkstra_solved_at

    @property
    def a_star_solved_at(self) -> int:
        return self._a_star_solved_at

    def output_step(self):
        if self._dijkstra_enabled and self._dijkstra_solved_at == -1:
            t = StepGrid(self._frame, self._iteration, 'black', 'white')
            self._dijkstra_grids.append(t)
            t.grid(column=0, row=self._row, sticky="new")
            t.solution = self._dijkstra_solution
        if self._dijkstra_enabled and self._a_star_enabled:
            label = Label(self._frame, text="   ")
            label.grid(column=1, row=self._row, sticky="new")
        if self._a_star_enabled and self._a_star_solved_at == -1:
            t2 = StepGrid(self._frame, self._iteration, 'black', 'white')
            self._a_star_grids.append(t2)
            t2.grid(column=2 if self._dijkstra_enabled else 0, row=self._row, sticky="new")
            t2.solution = self._a_star_solution
        self._row += 1
        spacer = Label(self._frame, text=" ")
        spacer.grid(row=self._row, column=0, columnspan=3)
        self._row += 1

        if self._dijkstra_enabled and self._dijkstra_solution.solved and self._dijkstra_solved_at == -1:
            self._dijkstra_solved_at = self._iteration
        if self._a_star_enabled and self._a_star_solution.solved and self._a_star_solved_at == -1:
            self._a_star_solved_at = self._iteration

        self.update()
        self._iteration += 1

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        for c in self._frame.grid_slaves():
            c.grid_remove()
            c.destroy()
        self._graph = graph
        self._iteration = 0
        self._dijkstra_solved_at = -1
        self._a_star_solved_at = -1
        if self._dijkstra_enabled:
            self._dijkstra_solution = Solution(graph, graph.origin, graph.destination, False)
        if self._a_star_enabled:
            self._a_star_solution = Solution(graph, graph.origin, graph.destination, True)

    @property
    def dijkstra_enabled(self) -> bool:
        return self._dijkstra_enabled

    @property
    def a_star_enabled(self) -> bool:
        return self._a_star_enabled

    @property
    def dijkstra_solution(self) -> Solution:
        return self._dijkstra_solution

    @property
    def a_star_solution(self) -> Solution:
        return self._a_star_solution

    @property
    def iteration(self) -> int:
        return self._iteration
