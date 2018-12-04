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

from typing import *
from Path import Path, crow_flies_down


class Node:

    def __init__(self, name, _id, x, y, z, heuristic=None, final_destination: 'Node'=None):
        self._name = name
        self._id = _id
        self._x = x
        self._y = y
        self._z = z
        self._out_paths = []
        self._in_paths = []
        if heuristic is None:
            if final_destination is None:
                self._heuristic = 0
            else:
                self._heuristic = crow_flies_down(self, final_destination)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def heuristic(self):
        return self._heuristic

    @property
    def in_paths(self) -> List[Path]:
        return self._in_paths

    @property
    def out_paths(self) -> List[Path]:
        return self._out_paths

    def link_to(self, destination_node: 'Node', distance=None):
        path = Path(self, destination_node, distance)
        self.out_paths.append(path)
        destination_node.in_paths.append(path)
        return path

    def link_from(self, origin_node: 'Node', distance=None):
        path = Path(origin_node, self, distance)
        self._in_paths.append(path)
        origin_node.out_paths.append(path)
        return path

    def link_from_to(self, from_to_node: 'Node', distance=None):
        path = Path(self, from_to_node, distance)
        self._out_paths.append(path)
        from_to_node.in_paths.append(path)
        assert self.name not in [p2.end.name for p2 in from_to_node.out_paths]
        #        assert from_to_node.name not in [p2.end.name for p2 in self._in_paths]
        path2 = Path(from_to_node, self, path.distance)
        self._in_paths.append(path2)
        from_to_node.out_paths.append(path2)
        return path, path2
