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

from copy import *
from Node import *


class SolutionNode:

    INFINITY = 99999999

    def __init__(self, node: Node):
        self._node = node
        self._total_path_distance = SolutionNode.INFINITY
        self._status = " "
        self._prev = None
        self._changed = False
        self._old = None

    def mark_as_start(self):
        self._total_path_distance = 0
        self._changed = False
        self._status = "▪"

    @property
    def node(self) -> Node:
        return self._node

    @property
    def prev(self) -> 'SolutionNode':
        return self._prev

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str):
        self._status = status

    def mark_path_to(self, prev: 'SolutionNode', total_distance):
        if self.total_path_distance < SolutionNode.INFINITY:
            self._old = copy(self)
        self._prev = prev
        self._total_path_distance = total_distance
        self._changed = True

    def reset(self):
        self._changed = False
        self._old = None

    @property
    def old(self) -> 'SolutionNode':
        return self._old

    @property
    def total_heuristic_distance(self):
        if self._total_path_distance == SolutionNode.INFINITY:
            return SolutionNode.INFINITY
        else:
            return self._total_path_distance + self._node.heuristic

    @property
    def total_path_distance(self):
        return self._total_path_distance

    @property
    def changed(self) -> bool:
        return self._changed
