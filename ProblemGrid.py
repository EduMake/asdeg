from TableGrid import *
from Graph import *
from InputtedGraph import *

class ProblemGrid(TableGrid) :
    def __init__(self, master: Frame, num_nodes: int = None, existing_graph: Graph = None, include_heuristics: bool = True, change_callback=None):
        super().__init__(master, 'black', 'white', 'grey')
        if existing_graph == None:
            self._num_nodes = num_nodes
        else:
            self._num_nodes = len(existing_graph.nodes)
        self._include_heuristics = include_heuristics
        self._weight_inputs = []
        self._angle_inputs = []
        self._name_inputs = []
        self._node_names =  []
        self._inputted_graph = InputtedGraph(num_nodes, existing_graph, include_heuristics, change_callback)
        self._change_callback = change_callback
        self.create_widgets()

    def update_headings(self):
        self._node_names = [ self._inputted_graph.name_vars[i].get() for i in range(0,self._num_nodes)]
        self.set_row_text(1, 4 if self._include_heuristics else 3, self._node_names, 1)


    def create_widgets(self):
        s = super()
        start_dest = 4 if self._include_heuristics else 3
        self.set_row_text(0, 0, ["Origin"], start_dest, 1)
        self.set_row_text(0, start_dest, ["Destination Weight"], self._num_nodes, 1)
        headings = ["Node Name", "Heuristic", "x", "y"] if self._include_heuristics else ["Node Name"]
        self.set_row_text(1,0,headings,1,1)
        self.update_headings()
        self._name_inputs = []
        self._x_inputs = []
        self._y_inputs = []
        self._weight_inputs = []
        for i in range(0, self._num_nodes):
            self._name_inputs.append(self.set_child(Entry(self, textvariable=self._inputted_graph.name_vars[i], fg='black', bg='white', width = 12, font=('Sans Serif', 11, "")), i + 2, 0))
            if self._include_heuristics :
                self._heuristic_inputs = [self.set_child(Entry(self, textvariable=self._inputted_graph.heuristic_vars[i], fg='black', bg='white', width = 5, font=('Sans Serif', 11, ""), justify = RIGHT), i + 2, 1) for i in range(0, self._num_nodes)]
            self._x_inputs.append(self.set_child(Entry(self, textvariable=self._inputted_graph.x_vars[i], fg='black', bg='white', width = 5, font=('Sans Serif', 11, ""), justify = RIGHT), i + 2, 2))
            self._y_inputs.append(self.set_child(Entry(self, textvariable=self._inputted_graph.y_vars[i], fg='black', bg='white', width = 5, font=('Sans Serif', 11, ""), justify = RIGHT), i + 2, 3))
            self._weight_inputs.append([self.set_child(Entry(self, textvariable=self._inputted_graph.weight_vars[i][j] if j < i else self._inputted_graph.weight_vars[j][i], fg='black', bg='white', width = 5, font=('Sans Serif', 11, ""), justify = RIGHT), i + 2, j + start_dest)  if j != i else None for j in range(0, self._num_nodes)])
        return

    @property
    def inputted_graph(self):
        return self._inputted_graph
