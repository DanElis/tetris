#!/usr/bin/env python3

from tkinter import Canvas, Label, Button, Frame, \
    N, E, W, S, PhotoImage, StringVar, messagebox

from canvas_game import CanvasGame
from figure import Figure


class Game(Frame):
    """Game class"""

    def __init__(self, master=None, title="Application"):
        """init Game class"""
        Frame.__init__(self, master)
        self.bQuit = Button(self, text='Quit', command=self.quit)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(title)
        self.grid(sticky=N+E+S+W)
        self.best = 0
        self.score = 0
        self.lines = 0
        self.first_screen()

    def create_figure(self):
        """Create figure and next figure fu9nction"""
        if self.next_figure is not None:
            self.control.canvas_next.remove_figure(self.next_figure.shifted())
            self.current_figure = self.next_figure
        else:
            self.current_figure = Figure()

        # Draw next figure
        self.next_figure = Figure()
        self.control.canvas_next.hold_figure(self.next_figure.shifted())
        self.control.canvas_next.redraw()

    def gravity(self, event=None):
        """Move the figure one cell down and draw function"""
        self.control.canvas.remove_figure(self.current_figure)
        coords = self.current_figure.move_down()
        if self.control.canvas.is_valid_coords(coords):
            self.current_figure.cells = coords
        else:
            self.control.canvas.hold_figure(self.current_figure)
            lines = self.control.canvas.find_complete_lines(self.current_figure)
            self.lines += lines
            self.score += 4
            if self.score > self.best:
                self.best = self.score
            self.control.score_string.set(f"Score: {self.score}")
            self.control.best_string.set(f"Best: {self.best}")
            self.control.lines_string.set(f"Lines: {self.lines}")
            self.create_figure()
            if self.control.canvas.is_valid_coords(self.current_figure.cells):
                self.control.canvas.hold_figure(self.current_figure)
            else:
                self.game_over()
                return 0
        self.control.canvas.hold_figure(self.current_figure)
        return 1

    def move_left(self, event):
        """Move the figure one cell left and draw function"""
        self.control.canvas.remove_figure(self.current_figure)
        coords = self.current_figure.move_left()
        if self.control.canvas.is_valid_coords(coords):
            self.current_figure.cells = coords
        self.control.canvas.hold_figure(self.current_figure)
        self.control.canvas.redraw()

    def move_right(self, event):
        """Move the figure one cell right and draw function"""
        self.control.canvas.remove_figure(self.current_figure)
        coords = self.current_figure.move_right()
        if self.control.canvas.is_valid_coords(coords):
            self.current_figure.cells = coords
        self.control.canvas.hold_figure(self.current_figure)
        self.control.canvas.redraw()

    def rotate(self, event):
        """Rotate the figure clockwise and draw function"""
        self.control.canvas.remove_figure(self.current_figure)
        coords = self.current_figure.rotate()
        if self.control.canvas.is_valid_coords(coords):
            self.current_figure.cells = coords
        self.control.canvas.hold_figure(self.current_figure)
        self.control.canvas.redraw()

    def first_screen(self):
        """Start screen control"""
        self.control = Frame(borderwidth=3, relief="solid", bg="white")
        self.control.grid(row=0, column=0, sticky=N + E + S + W)

        header_im = PhotoImage(file="tetris.png")
        self.control.header = Label(self.control, image=header_im,
                                    borderwidth=3, relief="solid",
                                    width=400, bg="white")
        self.control.header.image = header_im
        self.control.header.grid(row=0, columnspan=3, sticky=N + E + S + W)

        self.control.canvas = CanvasGame(self.control, width=400,
                                         height=600, borderwidth=3,
                                         relief="solid", bg="white",
                                         rows=24, columns=16, cell=25)
        self.control.canvas.grid(row=1, column=0, rowspan=7)

        self.control.canvas_next = Canvas(self.control, width=150,
                                         height=200, borderwidth=3,
                                         relief="solid", bg="white")
        self.control.canvas_next.grid(row=1, column=1, columnspan=2,
                                     sticky=N + E + S + W)

        self.control = Frame(borderwidth=3, relief="solid", bg="white")
        self.control.grid(row=0, column=0, sticky=N + E + S + W)

        self.control.best_string = StringVar()
        self.control.best_string.set(f"Best: {self.best}")
        self.control.score_string = StringVar()
        self.control.score_string.set(f"Score: {self.score}")

        header_im = PhotoImage(file="tetris.png")
        self.control.header = Label(self.control, image=header_im,
                                    borderwidth=3, relief="solid",
                                    width=615, bg="white")
        self.control.header.image = header_im
        self.control.header.grid(row=0, columnspan=4, sticky=N + E + S + W)

        self.control.score = Label(self.control,
                                   textvariable=self.control.score_string,
                                   borderwidth=3, relief="solid",
                                   font=("Liberation Sans", 14), bg="white")
        self.control.score.grid(row=2, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.new_game = Button(self.control, text="New Game",
                                      command=self.second_screen, borderwidth=3,
                                      relief="solid",
                                      font=("Liberation Sans", 14), bg="white")
        self.control.new_game.grid(row=4, column=1, columnspan=2,
                                  sticky=N + E + S + W)

        self.control.best = Label(self.control,
                                  textvariable=self.control.best_string,
                                  borderwidth=3,
                                  relief="solid", font=("Liberation Sans", 14),
                                  bg="white")
        self.control.best.grid(row=6, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.quit = Button(self.control, text="Quit",
                                   command=self.quit, borderwidth=3,
                                   relief="solid",
                                   font=("Liberation Sans", 14), bg="white")
        self.control.quit.grid(row=8, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.grid_rowconfigure(1, minsize=100)
        self.control.grid_rowconfigure(3, minsize=50)
        self.control.grid_rowconfigure(5, minsize=50)
        self.control.grid_rowconfigure(7, minsize=50)
        self.control.grid_columnconfigure(0, minsize=35)

    def second_screen(self):
        """Game screen control"""
        self.score = 0
        self.lines = 0
        self.control = Frame(borderwidth=3, relief="solid")
        self.control.grid(row=0, column=0, sticky=N + E + S + W)

        self.control.best_string = StringVar()
        self.control.best_string.set(f"Best: {self.best}")
        self.control.score_string = StringVar()
        self.control.score_string.set(f"Score: {self.score}")
        self.control.lines_string = StringVar()
        self.control.lines_string.set(f"Lines: {self.lines}")

        header_im = PhotoImage(file="tetris.png")
        self.control.header = Label(self.control, image=header_im,
                                    borderwidth=3, relief="solid",
                                    width=400, bg="white")
        self.control.header.image = header_im
        self.control.header.grid(row=0, columnspan=3, sticky=N + E + S + W)

        self.control.canvas = CanvasGame(self.control, width=400, height=600,
                                         borderwidth=3, relief="solid", bg="white",
                                         rows=24, columns=16, cell=25)
        self.control.canvas.grid(row=1, column=0, rowspan=7)

        self.control.canvas_next = CanvasGame(self.control, width=200, height=200,
                                             borderwidth=3, relief="solid",
                                             bg="white",
                                             rows=8, columns=8, cell=25)
        self.control.canvas_next.grid(row=1, column=1, columnspan=2,
                                     sticky=N + E + S + W)

        self.control.lines = Label(self.control,
                                   textvariable=self.control.lines_string,
                                   borderwidth=3, relief="solid",
                                   font=("Liberation Sans", 14), bg="white")
        self.control.lines.grid(row=3, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.score = Label(self.control,
                                   textvariable=self.control.score_string,
                                   borderwidth=3, relief="solid",
                                   font=("Liberation Sans", 14), bg="white")
        self.control.score.grid(row=4, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.best = Label(self.control,
                                  textvariable=self.control.best_string,
                                  borderwidth=3, relief="solid",
                                  font=("Liberation Sans", 14), bg="white")
        self.control.best.grid(row=5, column=1, columnspan=2, sticky=N + E + S + W)

        self.control.pause = Button(self.control, text="Pause",
                                    command=self.pause, borderwidth=3,
                                    relief="solid",
                                    font=("Liberation Sans", 14), bg="white")
        self.control.pause.grid(row=6, column=1, sticky=N + E + S + W)

        self.control.quit = Button(self.control, text="Quit",
                                   command=self.terminate, borderwidth=3,
                                   relief="solid",
                                   font=("Liberation Sans", 14), bg="white")
        self.control.quit.grid(row=6, column=2, sticky=N + E + S + W)

        self.control.canvas.draw()
        self.control.canvas_next.draw()
        self.next_figure = None
        self.create_figure()
        self._job = None
        self.bind_all("<Left>", self.move_left)
        self.bind_all("<Right>", self.move_right)
        self.bind_all("<Up>", self.rotate)
        self.bind_all("<Down>", self.gravity)
        self.tick()

    def tick(self):
        """Game timer"""
        flag = self.gravity()
        if flag == 0:
            return
        self.control.canvas.redraw()
        self._job = self.after(250, self.tick)

    def resume(self):
        """Resume game function"""
        self.control.pause.config(command=self.pause, text="Pause")
        self._job = self.after(250, self.tick)
        self.bind_all("<Left>", self.move_left)
        self.bind_all("<Right>", self.move_right)
        self.bind_all("<Up>", self.rotate)
        self.bind_all("<Down>", self.gravity)

    def pause(self):
        """Pause game function"""
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

        self.unbind_all("<Left>")
        self.unbind_all("<Right>")
        self.unbind_all("<Up>")
        self.unbind_all("<Down>")

        self.control.pause.config(command=self.resume, text="Resume")

    def game_over(self):
        """Stop the game"""
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        self.unbind_all("<Left>")
        self.unbind_all("<Right>")
        self.unbind_all("<Up>")
        self.unbind_all("<Down>")

        self.control.pause.config(command=self.second_screen, text="Start")
        messagebox.showinfo("Info", "Game Over")

    def terminate(self):
        """Quit to start screen"""
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
        self.first_screen()


if __name__ == "__main__":
    """Start main function"""
    app = Game(title="Tetris")
    app.mainloop()
