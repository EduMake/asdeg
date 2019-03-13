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
import enum

from asdeg.SolutionNode import *
from asdeg.Graph import *

class SolutionState(enum.Enum) :
    EMPTY = 0
    START_POPULATED = 1
    CURRENT_CHOSEN = 2
    OPENS_CALCED = 3
    AT_DESTINATION = 4
    ROUTE_TRACED = 5
    ROUTE_FORWARD_SOLVED = 6


class Solution:
    def __init__(self, graph: Graph, start, end, use_heuristics: bool):
        self._iteration = 0
        self._state = SolutionState.EMPTY
        self._graph = graph
        self._use_heuristics = use_heuristics
        self._route_nodes_reversed = []
        self._route_nodes_forwards = []
        self._route_paths = []
        self._all_nodes = list(range(len(graph.nodes)))
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
            self._all_nodes[n.id] = sn

    @property
    def iteration(self):
        return self._iteration

    @property
    def state(self):
        return self._state

    @property
    def graph(self):
        return self._graph

    @property
    def use_heuristics(self):
        return self._use_heuristics

    @property
    def all_nodes(self) -> List[SolutionNode]:
        return self._all_nodes

    @property
    def open_nodes(self) -> List[SolutionNode]:
        return self._open_nodes

    @property
    def route_nodes_reversed(self) -> List[SolutionNode]:
        return self._route_nodes_reversed

    @property
    def route_nodes_forwards(self) -> List[SolutionNode]:
        return self._route_nodes_forwards

    @property
    def solved(self) -> bool:
        return self._state == SolutionState.ROUTE_FORWARD_SOLVED

    def _populate_start(self):
        self._start.mark_as_start()
        self._open_nodes = [self._start]
        self._current = None
        self._state = SolutionState.START_POPULATED

    def _choose_current(self):
        if self._current is not None:
            self._current.status = "X"
        distance = 99999999
        current_sn = None
        for sn in self._open_nodes:
            if self._use_heuristics:
                new_distance = sn.total_path_distance + sn.node.heuristic
            else:
                new_distance = sn.total_path_distance
            if new_distance < distance or (new_distance == distance and sn == self._end):
                distance = new_distance
                current_sn = sn
        current_sn.status = "/"
        self._open_nodes.remove(current_sn)
        self._current = current_sn
        self._iteration += 1
        if self._current == self._end:
            self._state = SolutionState.AT_DESTINATION
        else:
            self._state = SolutionState.CURRENT_CHOSEN

    def _trace_route(self):
        if self._state == SolutionState.AT_DESTINATION:
            n = self._end
            while n:
                n.status = "*"
                self._route_nodes_reversed.append(n)
                n2 = n.prev
                if n2:
                    for p in n.node.in_paths:
                        if p.start == n2.node and p.end == n.node:
                            self._route_paths.append(p)
                    for p in n.node.out_paths:
                        if p.start == n and p.end == n2.node:
                            self._route_paths.append(p)
                n = n2
            self._state = SolutionState.ROUTE_TRACED

    def _solve_route_forwards(self):
        self._route_nodes_forwards = reversed(self._route_nodes_reversed)
        self._state = SolutionState.ROUTE_FORWARD_SOLVED

    def _calc_opens(self):
        for sn in self._all_nodes:
            sn.reset()
        curr_node = self._current.node
        base = self._current.total_path_distance
        for p in curr_node.out_paths:
            next_sn = self._all_nodes[p.end.id]
            if next_sn.status != "X":
                d = base + p.distance
                if d < next_sn.total_path_distance or (d == next_sn.total_path_distance and next_sn == self._end) :
                    next_sn.mark_path_to(self._current, d)
                    if next_sn.status == " ":
                        next_sn.status = "▪"
                        self._open_nodes.append(next_sn)
        self._state = SolutionState.OPENS_CALCED

    def single_step(self):
        if self._state == SolutionState.EMPTY:
            self._populate_start()
        elif self._state == SolutionState.START_POPULATED or self._state == SolutionState.OPENS_CALCED:
            self._choose_current()
            return False
        elif self._state == SolutionState.CURRENT_CHOSEN:
            self._calc_opens()
            return False
        elif self._state == SolutionState.AT_DESTINATION:
            self._trace_route()
            return False
        elif self._state == SolutionState.ROUTE_TRACED:
            self._solve_route_forwards()
            return True

