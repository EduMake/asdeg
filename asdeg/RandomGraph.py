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

from asdeg.Graph import *
from asdeg.intersection import *
from random import *
from asdeg.Node import *


class RandomGraph(Graph):
    def __init__(self):
        super().__init__()

        name_code = ord("A")
        coordinates = [(x, y, 0) for x in range(0, 200, 20) for y in range(0, 200, 20)]
        count = randrange(8, 10)
        samples = list(sample(coordinates, count))
        destination = samples.pop()
        destination_node = Node(chr(name_code + count - 1), count - 1, destination[0], destination[1], destination[2])
        self._nodes = [Node(chr(name_code + i), i, c[0], c[1], c[2], final_destination=destination_node)
                       for i, c in enumerate(samples)]
        origin_node = self._nodes[0]
        self._nodes.append(destination_node)
        all_paths = []
        for n in self._nodes:
            temp = self._nodes.copy()
            temp.remove(n)
            if n == origin_node:
                temp.remove(destination_node)
            if n == destination_node:
                temp.remove(origin_node)
            for n2 in temp.copy():
                if n in [p.end for p in n2.out_paths]:
                    temp.remove(n2)
                else:
                    for n3 in self._nodes:
                        if n3 != n2 and n3 != n and check_intersect(n.x, n.y, n2.x, n2.y, n3.x, n3.y, n3.x, n3.y):
                            temp.remove(n2)
                            break
            for n2 in temp.copy():
                for p in all_paths:
                    if check_intersect(n.x, n.y, n2.x, n2.y, p.start.x, p.start.y, p.end.x, p.end.y):
                        temp.remove(n2)
                        break
            pop = min(randrange(2, 4), len(temp))
            if pop > 0:
                for n2 in sample(temp, pop):
                    assert n2 != n and (n2.x != n.x or n2.y != n.y)
                    all_paths.append(n.link_from_to(n2)[0])
        print("paths:" + str(len(all_paths)))
        for p in all_paths:
            print(p.start.name + ":" + p.end.name + ":" + str(p.distance))
        self._origin_id = origin_node.id
        self._destination_id = destination_node.id

