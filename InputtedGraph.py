from Graph import *
from tkinter import *
from math import sqrt
class InputtedGraph:
    def __init__(self, num_nodes: int = None, existing_graph: Graph = None, include_heuristics :bool = True, change_callback = None):
        self._include_heuristics = include_heuristics
        self._change_callback = change_callback
        if existing_graph == None:
            self._num_nodes = num_nodes
            self._weight_vars = [[ IntVar() for j in range(0,i)] for i in range(0,self._num_nodes)]
            sq_size = int(sqrt(num_nodes))
            if sq_size * sq_size < num_nodes:
                sq_size += 1
            self._x_vars = [ IntVar(value = (i % sq_size) * 10) for i in range(0,self._num_nodes)]
            self._y_vars = [ IntVar(value = int(i / sq_size) * 10) for i in range(0,self._num_nodes)]
            self._name_vars = [ StringVar(value=chr(c)) for c in range(ord('A'),ord('A')+num_nodes) ]
            if self._include_heuristics :
                self._heuristic_vars = [ IntVar(value=0) for i in range(0,self._num_nodes) ]
        else:
            self._num_nodes = len(existing_graph.nodes)
            self._name_vars = [ StringVar(value = n.name) for n in existing_graph.nodes ]
            if self._include_heuristics :
                self._heuristic_vars = [ IntVar(value=n.heuristic) for n in existing_graph.nodes ]
            self._weight_vars = [[ IntVar() for j in range(0,i)] for i in range(0,self._num_nodes)]
            self._x_vars = [ IntVar(value = n.x) for n in existing_graph.nodes]
            self._y_vars = [ IntVar(value = n.y) for n in existing_graph.nodes]
            for i in range(0,self._num_nodes) :
                start = existing_graph.nodes[i]
                for out_path in start.out_paths :
                    end = out_path.end
                    j = end.id
                    if j < i:
                        self._weight_vars[i][j].set(out_path.distance)
                    else:
                        self._weight_vars[j][i].set(out_path.distance)
        if self._change_callback:
            self._traces = [ v.trace("w", self._change_callback) for v in self._name_vars]
            self._traces[-1:] = [ v.trace("w", self._change_callback) for v in self._heuristic_vars ]
            self._traces[-1:] = [ v.trace("w", self._change_callback) for v in self._x_vars ]
            self._traces[-1:] = [ v.trace("w", self._change_callback) for v in self._y_vars ]
            self._traces[-1:] = [ v.trace("w", self._change_callback) for l in self._weight_vars for v in l ]

    @property
    def name_vars(self):
        return self._name_vars

    @property
    def heuristic_vars(self):
        return self._heuristic_vars

    @property
    def weight_vars(self):
        return self._weight_vars

    @property
    def x_vars(self):
        return self._x_vars

    @property
    def y_vars(self):
        return self._y_vars

    @property
    def angle_vars(self):
        return self._angle_vars

    def to_graph(self):
        retval = Graph()
        for i in range(0,self._num_nodes) :
            nname = self._name_vars[i].get()
            x = self._x_vars[i].get()
            y = self._y_vars[i].get()
            h = self._heuristic_vars[i].get() if self._include_heuristics else None
            n = Node(nname, i, x, y, 0, h)
            retval.nodes.append(n)

        all_paths = []
        for i in range(0,self._num_nodes) :
            for j in range(0,i) :
                if self._weight_vars[i][j].get() > 0:
                    all_paths.append(retval.nodes[j].link_from_to(retval.nodes[i], self._weight_vars[i][j].get())[0])
        print("----------")
        print("paths:" + str(len(all_paths)))
        for p in all_paths:
            print(p.start.name + ":" + p.end.name + ":" + str(p.distance))
        retval.origin_id = 0
        retval.destination_id = len(retval.nodes) -1
        return retval
