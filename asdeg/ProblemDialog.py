from tkinter.simpledialog import *
from asdeg.ProblemFrame import *
from asdeg.Graph import *

class ProblemDialog(Dialog) :
    def __init__(self, master, num_nodes : int = None, existing_graph: Graph = None, include_heuristics : bool = True):
        self._problem_frame = None
        self._num_nodes = num_nodes
        self._include_heuristics = include_heuristics
        self._existing_graph = existing_graph
        super().__init__(master, "Problem")

    def apply(self):
        self.result = self._problem_frame.grid.inputted_graph.to_graph()
        return

    def redraw_preview(self):
        self._preview.undraw()
        self._preview.draw(self._problem_frame.grid.inputted_graph.to_graph())

    def onchange(self, a, b, c):
        self.redraw_preview()

    def frame_changed(self, event):
        del event
        self.update_idletasks()
        self.redraw_preview()


    def body(self, master):
        master.pack(padx=5, pady=5, fill=BOTH, expand=1)
        self._preview = GraphCanvas(master=master)
        self._preview.pack(side=TOP, anchor=N, fill=BOTH, expand=1, padx=0, pady=0)
        self._preview_button = Button(master=master,text="Preview", command=self.redraw_preview)
        self._preview_button.pack(side=TOP, anchor=N, fill=X)
        self._problem_frame = ProblemFrame(master, self._num_nodes, self._existing_graph, self._include_heuristics, self.onchange)
        self._problem_frame.pack(side=TOP, anchor=N, fill=BOTH, expand=1)
        self.bind('<Configure>', self.frame_changed)
        self._preview.draw(self._problem_frame.grid.inputted_graph.to_graph())
