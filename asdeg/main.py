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

from asdeg.RandomGraph import *
from asdeg.SolutionGrid import *
from asdeg.ProblemDialog import *
from random import seed
from tkinter import filedialog
import pickle

class MainWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.winfo_toplevel().title("ASDEG")
        self.pack(fill=BOTH, expand=1)

        self.controls_frame = None
        self.seed_entry_frame = None
        self.num_nodes_label = None
        self.num_nodes_entry = None
        self.input_button = None
        self.edit_button = None
        self.seed_label = None
        self.seed_entry = None
        self.generate_button = None
        self.save_button = None
        self.load_button = None
        self.next_button = None
        self.solution_control_frame = None
        self.solution_label = None
        self.whole_button = None
        self.step_button = None
        self.all_output_frame = None
        self.graph_frame = None
        self.dijkstra_label = None
        self.dijkstra_graph_canvas = None
        self.x_separator = None
        self.a_star_label = None
        self.a_star_graph_canvas = None
        self.separator = None
        self.solution_grid = None

        self.num_nodes_var = IntVar()
        self.num_nodes_var.set(8)
        self.seed_var = IntVar()
        self.seed_var.set(6)
        seed(self.seed_var.get())
        self.create_widgets()
        self.graph = RandomGraph()
        self.chooseCurrentNext = True
        self.dijkstra_graph_canvas.draw(self.graph)
        self.a_star_graph_canvas.draw(self.graph)
        self.bind('<Configure>', self.frame_changed)
        self.solution_grid.graph = self.graph

    def do_undraw(self):
        self.dijkstra_graph_canvas.undraw()
        self.a_star_graph_canvas.undraw()

    def do_draw(self):
        self.dijkstra_graph_canvas.draw(self.graph)
        self.a_star_graph_canvas.draw(self.graph)

    def do(self):
        self.dijkstra_graph_canvas.undraw()
        self.a_star_graph_canvas.undraw()
        seed(self.seed_var.get())
        self.graph = RandomGraph()
        self.solution_grid.graph = self.graph
        self.dijkstra_graph_canvas.draw(self.graph)
        self.a_star_graph_canvas.draw(self.graph)

    def do_next(self):
        self.seed_var.set(self.seed_var.get() + 1)
        self.do()

    def do_load(self):
        fname = filedialog.askopenfilename(filetypes = (("ASDEG files", "*.asdeg"),))
        if not fname is None:
            filehandler = open(fname, 'rb')
            self.do_undraw()
            self.graph = pickle.load(filehandler)
            filehandler.close()
            self.solution_grid.graph = self.graph
            self.do_draw()

    def do_save(self):
        fname = filedialog.asksaveasfilename(defaultextension=".asdeg", filetypes = (("ASDEG files", "*.asdeg"),))
        if not fname is None:
            filehandler = open(fname, 'wb')
            pickle.dump(self.graph, filehandler)
            filehandler.close()

    def do_input(self):
        try:
            val = self.num_nodes_var.get()
        except:
            val = None
        if val != None:
            dlg = ProblemDialog(master=self, num_nodes = val, include_heuristics = True)
            if dlg.result:
                self.dijkstra_graph_canvas.undraw()
                self.a_star_graph_canvas.undraw()
                self.graph = dlg.result
                self.solution_grid.graph = self.graph
                self.dijkstra_graph_canvas.draw(self.graph)
                self.a_star_graph_canvas.draw(self.graph)

    def do_edit(self):
        dlg = ProblemDialog(master=self, existing_graph = self.graph, include_heuristics = True)
        if dlg.result:
            self.dijkstra_graph_canvas.undraw()
            self.a_star_graph_canvas.undraw()
            self.graph = dlg.result
            self.solution_grid.graph = self.graph
            self.dijkstra_graph_canvas.draw(self.graph)
            self.a_star_graph_canvas.draw(self.graph)

    def do_generate(self):
        self.seed_entry.update()
        self.do()

    @staticmethod
    def validate(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):

        del action, index, prior_value, validation_type, trigger_type, widget_name

        if text in '0123456789-+':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def solve_whole(self):
        while self.solve_step():
            pass
        return

    def solve_step(self):
        do_dijkstra = not self.solution_grid.dijkstra_grid is None
        do_a_star = not self.solution_grid.a_star_grid is None
        dijkstra_in_progress = do_dijkstra and not self.solution_grid.dijkstra_grid.solution.solved
        a_star_in_progress = do_a_star and not self.solution_grid.a_star_grid.solution.solved
        stepping = dijkstra_in_progress or a_star_in_progress
        if stepping:
            self.solution_grid.pre_step()
        if dijkstra_in_progress:
            dijkstra_in_progress = dijkstra_in_progress and not self.solution_grid.dijkstra_grid.solution.single_step()
            self.solution_grid.dijkstra_grid.output_step()
            self.dijkstra_graph_canvas.undraw()
            self.dijkstra_graph_canvas.draw(self.graph, self.solution_grid.dijkstra_grid.solution)
        if a_star_in_progress:
            a_star_in_progress = a_star_in_progress and not self.solution_grid.a_star_grid.solution.single_step()
            self.solution_grid.a_star_grid.output_step()
            self.a_star_graph_canvas.undraw()
            self.a_star_graph_canvas.draw(self.graph, self.solution_grid.a_star_grid.solution)
        if stepping:
            self.solution_grid.post_step()

        return dijkstra_in_progress or a_star_in_progress

    def create_widgets(self):
        self.master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'
        self.controls_frame = Frame(self)
        self.controls_frame.pack(fill=X)

        self.seed_entry_frame = Frame(self.controls_frame)
        self.seed_entry_frame.pack(side=LEFT, anchor=W)
        self.num_nodes_label = Label(self.seed_entry_frame, text="# of nodes:")
        self.num_nodes_label.pack(side=LEFT)
        self.num_nodes_entry = Entry(self.seed_entry_frame, textvariable=self.num_nodes_var, justify = RIGHT)
        self.num_nodes_entry.pack(side=LEFT)
        self.input_button = Button(self.seed_entry_frame, command=self.do_input, text="Input")
        self.input_button.pack(side=LEFT)
        self.edit_button = Button(self.seed_entry_frame, command=self.do_edit, text="Edit")
        self.edit_button.pack(side=LEFT)
        self.seed_label = Label(self.seed_entry_frame, text="Seed:")
        self.seed_label.pack(side=LEFT)
        self.seed_entry = Entry(self.seed_entry_frame, textvariable=self.seed_var, justify = RIGHT)
        self.seed_entry.pack(side=LEFT)
        self.seed_entry.update()
        self.generate_button = Button(self.seed_entry_frame, command=self.do_generate, text="Generate")
        self.generate_button.pack(side=LEFT)
        self.next_button = Button(self.seed_entry_frame, command=self.do_next, text="Next")
        self.next_button.pack(side=LEFT)
        self.load_button = Button(self.seed_entry_frame, command=self.do_load, text="Load")
        self.load_button.pack(side=LEFT)
        self.save_button = Button(self.seed_entry_frame, command=self.do_save, text="Save")
        self.save_button.pack(side=LEFT)

        self.solution_control_frame = Frame(self.controls_frame)
        self.solution_control_frame.pack(side=LEFT, anchor=E, pady=4)
        self.solution_label = Label(self.solution_control_frame, text="Solution:")
        self.solution_label.pack(side=LEFT)
        self.whole_button = Button(self.solution_control_frame, command=self.solve_whole, text="Whole")
        self.whole_button.pack(side=LEFT)
        self.step_button = Button(self.solution_control_frame, command=self.solve_step, text="Step")
        self.step_button.pack(side=LEFT)

        self.all_output_frame = Frame(self)
        self.all_output_frame.pack(side=LEFT, fill=BOTH, expand=1, pady=0, padx=0)

        self.graph_frame = Frame(self.all_output_frame)
        self.graph_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=6, pady=6)
        self.dijkstra_label = Label(self.graph_frame, text="Solution by Dijkstra's Algorithm",
                                    font=("Sans Serif", 11, "underline"))
        self.dijkstra_label.pack(side=TOP, anchor=N, fill=X, expand=0, padx=0)
        self.dijkstra_graph_canvas = GraphCanvas(self.graph_frame, show_heuristics=0)
        self.dijkstra_graph_canvas.pack(side=TOP, anchor=N, fill=BOTH, expand=1, padx=0, pady=0)

        self.x_separator = Frame(self.graph_frame, height=6)
        self.x_separator.pack(side=TOP, fill=X, expand=0)

        self.a_star_label = Label(self.graph_frame, text="Solution by A* Algorithm", font=("Sans Serif", 11, "underline"))
        self.a_star_label.pack(side=TOP, anchor=N, fill=X, expand=0, padx=0)
        self.a_star_graph_canvas = GraphCanvas(self.graph_frame, show_heuristics=1)
        self.a_star_graph_canvas.pack(side=TOP, anchor=N, fill=BOTH, expand=1, padx=0, pady=0)

        self.separator = Frame(self.all_output_frame, width=5, borderwidth=2, relief=RAISED)
        self.separator.pack(side=LEFT, fill=Y, expand=0)

        self.solution_grid = SolutionGrid(self.all_output_frame, True, True)
        self.solution_grid.pack(side=LEFT, anchor=N, fill=BOTH, expand=1, padx=6, pady=6)
        self.update()

    def frame_changed(self, event):

        del event

        self.update_idletasks()
        if self.dijkstra_graph_canvas:
            self.dijkstra_graph_canvas.undraw()
            self.dijkstra_graph_canvas.draw(self.graph, self.solution_grid.dijkstra_grid.solution)
        if self.a_star_graph_canvas:
            self.a_star_graph_canvas.undraw()
            self.a_star_graph_canvas.draw(self.graph, self.solution_grid.a_star_grid.solution)


root = Tk()
root.minsize(500,400)
main_window = MainWindow(master=root)
main_window.mainloop()
# root.destroy()
