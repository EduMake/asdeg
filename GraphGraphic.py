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
from NodeGraphic import *


class GraphGraphic:
    def __init__(self, graph: Graph, show_heuristics: bool):
        self.graph = graph
        self._node_graphics = {}
        for n in graph.nodes:
            self._node_graphics[n.id] = NodeGraphic(n, show_heuristics)

    def draw(self, canvas: ScaledCanvas, solution: Solution=None):
        for ng in self._node_graphics.values():
            canvas.expand_range(ng.node.x, ng.node.y, 20)
        if solution:
            for sn in solution.all_nodes:
                ng = self._node_graphics[sn.node.id]
                if sn.status == '/':
                    ng.mark('magenta')
                elif sn.status == '*':
                    ng.mark('green')
                elif sn.status == '*':
                    ng.mark('green')
                elif sn.status == '▪':
                    ng.mark('darkcyan')
                elif sn.status == 'X':
                    ng.mark('darkblue')
                for pg in ng.path_graphics:
                    start_sn = solution.all_nodes[pg.path.start.id]
                    end_sn = solution.all_nodes[pg.path.end.id]
                    if start_sn.status == '*' and end_sn.status == '*' and \
                            (start_sn.prev and start_sn.prev.node.id == end_sn.node.id or
                                end_sn.prev and end_sn.prev.node.id == start_sn.node.id):
                        pg.mark('green')
                    elif start_sn.status == '/':
                        pg.mark('magenta')

            for ng in self._node_graphics.values():
                ng.draw(canvas, 'green')
            for ng in self._node_graphics.values():
                ng.draw(canvas, 'magenta')
            for ng in self._node_graphics.values():
                ng.draw(canvas, 'darkcyan')
            for ng in self._node_graphics.values():
                ng.draw(canvas, 'darkblue')
            for ng in self._node_graphics.values():
                ng.draw(canvas)
            for ng in self._node_graphics.values():
                ng.reset()
                for pg in ng.path_graphics:
                    pg.reset()
        else:
            for ng in self._node_graphics.values():
                ng.draw(canvas)

    def undraw(self, canvas: ScaledCanvas):
        for n in self._node_graphics.values():
            n.undraw(canvas)
