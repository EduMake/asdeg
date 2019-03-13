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
from asdeg import SolutionGrid
from asdeg.Solution import *
from asdeg.StepGrid import StepGrid


class SolutionSubGrid:
    def __init__(self, parent_grid: SolutionGrid, start_column: int, use_heuristics: bool):
        self._parent_grid = parent_grid
        self._start_column = start_column
        self._use_heuristics = use_heuristics
        self._enabled = True
        self._solution = None
        self._grids = []
        self._graph = None
        self._solved_at = -1
        self._row = 0
        self._column = 0

    @property
    def solved_at(self) -> int:
        return self._solved_at

    def output_step(self):
        if self._enabled and self._solved_at == -1:
            t = StepGrid(self._parent_grid.frame, self.solution.iteration, 'black', 'white')
            self._grids.append(t)
            t.grid(column=self._start_column, row=self._row, sticky="new")
            t.solution = self._solution
        self._row += 2

        if self._enabled and self._solution.solved and self._solved_at == -1:
            self._solved_at = self._solution.iteration

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        self._graph = graph
        self._solved_at = -1
        if self._enabled:
            self._solution = Solution(graph, graph.origin_node, graph.destination_node, self._use_heuristics)
        self._grids = []
        self._row = 0
        self._column = 0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def solution(self) -> Solution:
        return self._solution

    @property
    def iteration(self) -> int:
        return self._solution.iteration
