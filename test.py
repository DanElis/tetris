import unittest
import tetris
from canvas_game import CanvasGame
from figure import Figure
import tkinter


class TestTetris(unittest.TestCase):

    def test_line_deletion(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                             borderwidth=3, relief="solid", bg="white",
                             rows=24, columns=16, cell=25)
        # fill line
        for j in range(ttrs.columns):
            ttrs.matrix[j][ttrs.rows-1] = "blue"

        f = Figure()
        f.cells.append((1, ttrs.rows - 1))

        count = ttrs.find_complete_lines(f)

        self.assertEqual(count, 1)
        for j in range(ttrs.columns):
            self.assertEqual(ttrs.matrix[j][ttrs.rows-1], "gray")

    def test_hold_figure(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                             borderwidth=3, relief="solid", bg="white",
                             rows=24, columns=16, cell=25)

        f = Figure()
        ttrs.hold_figure(f)
        for cell in f.cells:
            self.assertEqual(ttrs.matrix[cell[0]][cell[1]], f.color)

    def test_remove_figure(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                             borderwidth=3, relief="solid", bg="white",
                             rows=24, columns=16, cell=25)

        f = Figure()
        ttrs.hold_figure(f)
        f.cells.append((-1,10))
        f.cells.append((1, -10))
        ttrs.remove_figure(f)
        for cell in f.cells:
            self.assertEqual(ttrs.matrix[cell[0]][cell[1]], "gray")

    def test_find_complete_lines(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                          borderwidth=3, relief="solid", bg="white",
                          rows=24, columns=16, cell=25)
        # fill line
        for j in range(ttrs.columns):
            ttrs.matrix[j][ttrs.rows - 1] = "blue"
            ttrs.matrix[j][ttrs.rows - 2] = "red"

        f = Figure()
        f.cells.append((1, ttrs.rows - 1))
        f.cells.append((1, ttrs.rows - 2))

        self.assertTrue(ttrs.line_complete(ttrs.rows - 1))

        count = ttrs.find_complete_lines(f)

        self.assertEqual(count, 2)

    def test_draw(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                          borderwidth=3, relief="solid", bg="white",
                          rows=24, columns=16, cell=25)
        old_value = ttrs.matrix[1][1]
        ttrs.matrix[1][1] = 'red'
        ttrs.draw()
        self.assertNotEqual(ttrs.rects[1,1], old_value)
        ttrs.redraw()
        self.assertNotEqual(ttrs.rects[1,1], old_value)

    def test_figure_move_down(self):
        f = Figure()

        cells = f.move_down()
        for idx, cell in enumerate(f.cells):
            self.assertEqual(cells[idx][0], cell[0])
            self.assertEqual(cells[idx][1], cell[1]+1)

    def test_figure_move_left(self):
        f = Figure()

        cells = f.move_left()
        for idx, cell in enumerate(f.cells):
            self.assertEqual(cells[idx][0]+1, cell[0])
            self.assertEqual(cells[idx][1], cell[1])

    def test_figure_move_right(self):
        f = Figure()

        cells = f.move_right()
        for idx, cell in enumerate(f.cells):
            self.assertEqual(cells[idx][0]-1, cell[0])
            self.assertEqual(cells[idx][1], cell[1])

    def test_game_over(self):
        app = tetris.Game(title="Tetris")
        app.second_screen()
        self.assertNotEqual(app._job, None)

        for i in range(app.control.canvas.rows):
            for j in range(app.control.canvas.columns):
                app.control.canvas.matrix[j][i] = "red"
        app.gravity()

        self.assertEqual(app._job, None)

    def test_create_figure(self):
        app = tetris.Game(title="Tetris")
        app.second_screen()
        app.create_figure()
        app.create_figure()
        f = app.current_figure
        next_f = app.next_figure
        app.create_figure()
        self.assertEqual(next_f, app.current_figure)
        self.assertNotEqual(f, app.current_figure)

    def test_gravity(self):
        app = tetris.Game(title="Tetris")
        app.second_screen()
        app.gravity()
        f = app.current_figure
        next_f = app.next_figure
        app.create_figure()
        self.assertEqual(next_f, app.current_figure)
        self.assertNotEqual(f, app.current_figure)

    def test_is_valid_coords(self):
        tmp = tkinter.Frame(borderwidth=3, relief="solid")
        ttrs = CanvasGame(tmp, width=400, height=600,
                          borderwidth=3, relief="solid", bg="white",
                          rows=24, columns=16, cell=25)

        valid_coords = [(1,1),(2,9),(3,3)]
        not_valid_coords = valid_coords.copy()
        not_valid_coords.append((-1,-1))
        self.assertTrue(ttrs.is_valid_coords(valid_coords))
        self.assertFalse(ttrs.is_valid_coords(not_valid_coords))
        not_valid_coords = valid_coords.copy()
        not_valid_coords.append((1,-1))
        self.assertFalse(ttrs.is_valid_coords(not_valid_coords))

    def test_pause_and_resume(self):
        app = tetris.Game(title="Tetris")
        app.second_screen()
        self.assertNotEqual(app._job, None)
        app.pause()
        self.assertEqual(app._job, None)
        app.resume()
        self.assertNotEqual(app._job, None)
    def test_terminate(self):
        app = tetris.Game(title="Tetris")
        app.second_screen()
        control = app.control
        app.terminate()
        self.assertNotEqual(control,app.control)

if __name__ == '__main__':
    unittest.main()
