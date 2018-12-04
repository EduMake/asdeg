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

from math import sqrt, floor, ceil
from random import *
import Node


class Path:
    def __init__(self, start: Node, end: Node, distance):
        self._start = start
        self._end = end
        if distance is None:
            self._distance = crow_flies_longer(start, end)
        else:
            self._distance = distance

    @property
    def start(self) -> Node:
        return self._start

    @property
    def end(self) -> Node:
        return self._end

    @property
    def distance(self):
        return self._distance


def crow_flies(origin_node, destination_node):
    delta_x = origin_node.x - destination_node.x
    delta_y = origin_node.y - destination_node.y
    delta_z = origin_node.z - destination_node.z
    return sqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z)


def crow_flies_down(origin_node, destination_node):
    cf = crow_flies(origin_node, destination_node)
    return int(floor(cf / 5.0) * 5.0)


def crow_flies_longer(origin_node, destination_node):
    cf = crow_flies(origin_node, destination_node)
    return int(ceil((1.0+random() * 0.5) * cf / 5.0) * 5.0)
