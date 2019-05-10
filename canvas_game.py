from tkinter import Canvas, StringVar


class CanvasGame(Canvas):
    """Screen class"""

    def __init__(self, master=None, *ap, foreground="black", rows,
                 columns, cell, **an):
        """Init screen function"""
        self.foreground = StringVar()
        self.foreground.set(foreground)
        Canvas.__init__(self, master, *ap, **an)

        self.rows = rows
        self.columns = columns
        self.cell_width = cell
        self.cell_height = cell

        self.matrix = []
        for _ in range(self.columns):
            column_arr = ["gray" for _ in range(self.rows)]
            self.matrix.append(column_arr)
        self.rects = {}

    def hold_figure(self, figure):
        """Add figure to the matrix function"""
        for cell in figure.cells:
            x, y = cell
            self.matrix[x][y] = figure.color

    def remove_figure(self, figure):
        """Remove figure from  the matrix function"""
        for cell in figure.cells:
            x, y = cell
            if x > self.columns - 1 or x < 0:
                continue
            if y > self.rows - 1 or y < 0:
                continue

            self.matrix[x][y] = "gray"

    def draw(self):
        """Draw screen"""
        self.rects = {}
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                fill = self.matrix[column][row]
                self.rects[row, column] = self.create_rectangle(x1, y1,
                                                                x2, y2,
                                                                fill=fill,
                                                                tags="rect")

    def redraw(self):
        """Redraw figure function"""
        for column in range(self.columns):
            for row in range(self.rows):
                self.itemconfig(self.rects[row, column],
                                fill=self.matrix[column][row])

    def is_valid_coords(self, coords):
        """Checking whether the cells are busy"""
        for c in coords:
            if c[0] > self.columns - 1 or c[0] < 0:
                return False
            if c[1] > self.rows - 1 or c[1] < 0:
                return False
            if self.matrix[c[0]][c[1]] != "gray":
                return False
        return True

    def line_complete(self, i):
        """Checking whether line is full"""
        for j in range(self.columns):
            if self.matrix[j][i] == "gray":
                return False
        return True

    def delete_line(self, idx):
        """Delete line from screen function"""
        for x in range(self.columns):
            for y in range(idx, 0, -1):
                if y > -1:
                    self.matrix[x][y] = self.matrix[x][y - 1]

    def find_complete_lines(self, figure):
        """Find completed by figure lines"""
        count = 0
        to_delete = []
        for cell in figure.cells:
            if self.line_complete(cell[1]):
                to_delete.append(cell[1])
                count += 1
        to_delete = set(sorted(to_delete))
        for line in to_delete:
            self.delete_line(line)
        return count
