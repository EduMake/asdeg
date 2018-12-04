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

from SolutionNode import *
from Graph import *


class Solution:
    def __init__(self, graph: Graph, start, end, use_heuristics: bool):
        self._graph = graph
        self._use_heuristics = use_heuristics
        self._solution_nodes = list(range(len(graph.nodes)))
        for n in graph.nodes:
            sn = SolutionNode(n)
            if isinstance(start, int):
                if n.id == start:
                    self._start = sn
            elif isinstance(start, str):
                if n.name == start:
                    self._start = sn
            elif isinstance(start, Node):
                if n == start:
                    self._start = sn
            if isinstance(end, int):
                if n.id == end:
                    self._end = sn
            elif isinstance(end, str):
                if n.name == end:
                    self._end = sn
            elif isinstance(end, Node):
                if n == end:
                    self._end = sn
            self._solution_nodes[n.id] = sn
        self._start.mark_as_start()
        self._open_nodes = [self._start]
        self._solved = False
        self._current = None
        self._route_nodes = []
        self._route_paths = []

    @property
    def graph(self):
        return self._graph

    @property
    def use_heuristics(self):
        return self._use_heuristics

    @property
    def solution_nodes(self) -> List[SolutionNode]:
        return self._solution_nodes

    @property
    def open_nodes(self) -> List[SolutionNode]:
        return self._open_nodes

    @property
    def solved(self) -> bool:
        return self._solved

    def find_new_current(self):
        if self._current is not None:
            self._current.status = "X"
        distance = 99999999
        current_sn = None
        for sn in self._open_nodes:
            if self._use_heuristics:
                new_distance = sn.total_path_distance + sn.node.heuristic
            else:
                new_distance = sn.total_path_distance
            if new_distance < distance:
                distance = new_distance
                current_sn = sn
        current_sn.status = "/"
        self._open_nodes.remove(current_sn)
        self._current = current_sn
        self._solved = (self._current == self._end)
        if self._solved:
            n = self._end
            while n:
                n.status = "*"
                self._route_nodes.append(n)
                n2 = n.prev
                if n2:
                    for p in n.node.in_paths:
                        if p.start == n2.node and p.end == n.node:
                            self._route_paths.append(p)
                    for p in n.node.out_paths:
                        if p.start == n and p.end == n2.node:
                            self._route_paths.append(p)
                n = n2
        return self._solved

    def calc_next(self):
        for sn in self._solution_nodes:
            sn.reset()
        curr_node = self._current.node
        base = self._current.total_path_distance
        for p in curr_node.out_paths:
            next_sn = self._solution_nodes[p.end.id]
            if next_sn.status != "X":
                d = base + p.distance
                if d < next_sn.total_path_distance:
                    next_sn.mark_path_to(self._current, d)
                    if next_sn.status == " ":
                        next_sn.status = "▪"
                        self._open_nodes.append(next_sn)
