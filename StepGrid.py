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
from TableGrid import *
from SolutionNode import *


class StepGrid(TableGrid):

    @staticmethod
    def format_inf(n):
        return '∞' if n >= SolutionNode.INFINITY else str(n)

    @staticmethod
    def format_solution_node_name(sn: SolutionNode):
        if not sn:
            return '-'
        else:
            return sn.node.name

    def __init__(self, master: Frame, iteration: int, grid_color, back_color):
        super().__init__(master, grid_color, back_color)
        self._solution = None
        self._iteration = iteration

    @property
    def solution(self) -> Solution:
        return self._solution

    @solution.setter
    def solution(self, solution: Solution):
        self._solution = solution
        if self._solution.use_heuristics:
            self.set_row_text(0, 0, ["A*"], 7)
            self.set_row_text(1, 0, ["Iter.", "Node", "PD", "HD", "PD+HD", "Prev", "Status"])
        else:
            self.set_row_text(0, 0, ["Dijkstra's"], 5)
            self.set_row_text(1, 0, ["Iter.", "Node", "PD", "Prev", "Status"])
        row = 2
        for sn in self._solution.all_nodes:
            column = 1
            if sn.old:
                self.set_row_text(row, column, sn.node.name, row_span=2, anchor='center')
                column += 1
                self.set_row_text(row, column, [self.format_inf(sn.old.total_path_distance)], font=('Sans Serif', 11, 'overstrike'), text_color='red')
                column += 1
                if self._solution.use_heuristics:
                    self.set_row_text(row, column, [self.format_inf(sn.node.heuristic), self.format_inf(sn.old.total_heuristic_distance)], font=('Sans Serif', 11, 'overstrike'), text_color='red')
                    column += 2
                self.set_row_text(row, column, [self.format_solution_node_name(sn.old.prev)], font=('Sans Serif', 11, 'overstrike'), text_color='red')
                row += 1
            else:
                self.set_row_text(row, column, sn.node.name)
            column = 2
            self.set_row_text(row, column, [self.format_inf(sn.total_path_distance)])
            column += 1
            if self._solution.use_heuristics:
                self.set_row_text(row, column, [self.format_inf(sn.node.heuristic), self.format_inf(sn.total_heuristic_distance)])
                column += 2
            self.set_row_text(row, column, [self.format_solution_node_name(sn.prev)])
            column += 1

            if sn.status == "*":
                t = "X"
                f = ('Sans Serif', 11, 'overstrike')
            else:
                t = sn.status
                f = ('Sans Serif', 11)
            if sn.old:
                self.set_row_text(row - 1, column, [t], font=f, row_span=2, anchor='center')
            else:
                self.set_row_text(row, column, [t], font=f)
            row += 1
        if self._solution.solved:
            sol = " -> ".join(n.node.name for n in reversed(self._solution.route_nodes_reversed))
            self.set_row_text(row=row, start_column=0, text=[sol], column_span= 7 if self._solution.use_heuristics else 5)
        self.set_row_text(row=2, start_column=0, text=[str(self._iteration)], row_span=row - 2, anchor='n')
