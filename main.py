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

from RandomGraph import *
from GraphCanvas import *
from SolutionGrid import *
from random import seed


class MainWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.winfo_toplevel().title("ASDEG")
        self.pack(fill=BOTH, expand=1)

        self.controls_frame = None
        self.seed_entry_frame = None
        self.seed_label = None
        self.seed_entry = None
        self.generate_button = None
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

        self.seed_var = IntVar()
        self.seed_var.set(6)
        seed(self.seed_var.get())
        self.create_widgets()
        self.graph = RandomGraph()
        self.dijkstra_graph_canvas.draw(self.graph)
        self.a_star_graph_canvas.draw(self.graph)
        self.bind('<Configure>', self.frame_changed)

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
        if self.solution_grid.graph is None:
            self.solution_grid.graph = self.graph
        do_dijkstra = self.solution_grid.dijkstra_enabled
        do_a_star = self.solution_grid.a_star_enabled
        dijkstra_in_progress = do_dijkstra and not self.solution_grid.dijkstra_solution.solved
        a_star_in_progress = do_a_star and not self.solution_grid.a_star_solution.solved
        if self.solution_grid.iteration == 0:
            self.dijkstra_graph_canvas.undraw()
            self.dijkstra_graph_canvas.draw(self.graph, self.solution_grid.dijkstra_solution)
            self.a_star_graph_canvas.undraw()
            self.a_star_graph_canvas.draw(self.graph, self.solution_grid.a_star_solution)
            self.solution_grid.output_step()
            return True
        else:
            if a_star_in_progress or dijkstra_in_progress:
                ret_val = False
                if dijkstra_in_progress:
                    if not self.solution_grid.dijkstra_solution.find_new_current():
                        self.solution_grid.dijkstra_solution.calc_next()
                        ret_val = True
                if a_star_in_progress:
                    if not self.solution_grid.a_star_solution.find_new_current():
                        self.solution_grid.a_star_solution.calc_next()
                        ret_val = True
                self.dijkstra_graph_canvas.undraw()
                self.dijkstra_graph_canvas.draw(self.graph, self.solution_grid.dijkstra_solution)
                self.a_star_graph_canvas.undraw()
                self.a_star_graph_canvas.draw(self.graph, self.solution_grid.a_star_solution)
                self.solution_grid.output_step()
                return ret_val
            else:
                return False

    def create_widgets(self):
        self.master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'
        self.controls_frame = Frame(self)
        self.controls_frame.pack(fill=X)

        self.seed_entry_frame = Frame(self.controls_frame)
        self.seed_entry_frame.pack(side=LEFT, anchor=W)
        self.seed_label = Label(self.seed_entry_frame, text="Seed:")
        self.seed_label.pack(side=LEFT)
        self.seed_entry = Entry(self.seed_entry_frame, textvariable=self.seed_var)
        self.seed_entry.pack(side=LEFT)
        self.seed_entry.update()
        self.generate_button = Button(self.seed_entry_frame, command=self.do_generate, text="Generate")
        self.generate_button.pack(side=LEFT)
        self.next_button = Button(self.seed_entry_frame, command=self.do_next, text="Next")
        self.next_button.pack(side=LEFT)

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
            self.dijkstra_graph_canvas.draw(self.graph, self.solution_grid.dijkstra_solution)
        if self.a_star_graph_canvas:
            self.a_star_graph_canvas.undraw()
            self.a_star_graph_canvas.draw(self.graph, self.solution_grid.a_star_solution)


root = Tk()
main_window = MainWindow(master=root)
main_window.mainloop()
# root.destroy()
