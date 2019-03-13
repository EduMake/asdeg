from asdeg.ScrollableFrame import *
from asdeg.ProblemGrid import *
from asdeg.GraphCanvas import *

class ProblemFrame(ScrollableFrame):
    def __init__(self, master: Frame, num_nodes: int = None, existing_graph: Graph = None, include_heuristics: bool = True, change_callback = None):
        super().__init__(master)
        self._num_nodes = num_nodes
        self._existing_graph = existing_graph
        self._include_heuristics = include_heuristics
        self._change_callback = change_callback
        self.create_widgets()


    def create_widgets(self):
        self._grid = ProblemGrid(master=self._frame, num_nodes=self._num_nodes, existing_graph = self._existing_graph, include_heuristics=self._include_heuristics, change_callback = self._change_callback)
        self._grid.pack(fill=BOTH)
        return

    @property
    def grid(self):
        return self._grid
