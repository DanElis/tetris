from random import choice, randint


class Figure():
    """Tetris figure class"""
    SHAPES = (
        ("yellow", (0, 0), (0, 1), (1, 0), (1, 1)),     # O
        ("lightblue", (0, 0), (0, 1), (0, 2), (0, 3)),  # I
        ("red", (0, 1), (1, 1), (1, 0), (2, 0)),        # Z
        ("green", (0, 0), (1, 0), (1, 1), (2, 1)),      # S
        ("orange", (0, 2), (0, 1), (0, 0), (1, 0)),     # L
        ("blue", (0, 0), (1, 0), (1, 1), (1, 2)),       # J
        ("purple", (0, 0), (1, 0), (2, 0), (1, 1)),     # T
    )

    def __init__(self, x=7, y=0):
        """Init figure"""
        figure = choice(self.SHAPES)
        self.color = figure[0]
        self.cells = []
        for cell in figure[1:]:
            self.cells.append((x + cell[0], y + cell[1]))
        coords = self.cells
        times = randint(0, 2)
        for _ in range(times):
            coords = self.rotate()
        self.cells = coords

    def shifted(self):
        """Shift the figure at second screen"""
        shifted = Figure()
        shifted.color = self.color
        shifted.cells = [(cell[0] - 4, cell[1] + 3) for cell in self.cells]
        return shifted

    def move_down(self):
        """Move the figure down"""
        new_cells = []
        for cell in self.cells:
            new_cells.append((cell[0], cell[1] + 1))
        return new_cells

    def move_left(self):
        """Move the figure left"""
        new_cells = []
        for cell in self.cells:
            new_cells.append((cell[0] - 1, cell[1]))
        return new_cells

    def move_right(self):
        """Move the figure right"""
        new_cells = []
        for cell in self.cells:
            new_cells.append((cell[0] + 1, cell[1]))
        return new_cells

    def rotate(self):
        """Rotate the figure"""
        shift_x = 1000
        shift_y = 1000
        old_cells_shifted = []
        for cell in self.cells:
            if cell[0] < shift_x:
                shift_x = cell[0]
            if cell[1] < shift_y:
                shift_y = cell[1]
                #нужно запомнить куда нам возвращаться
        for cell in self.cells:
            old_cells_shifted.append((cell[0]-shift_x, cell[1]-shift_y))
        new_cells = []
        min_x = 0
        min_y = 1000
        for cell in old_cells_shifted:
            tmp_cell = (-cell[1], cell[0])
            new_cells.append(tmp_cell)
            if tmp_cell[0] < min_x:
                min_x = tmp_cell[0]
            if tmp_cell[1] < min_y:
                min_y = tmp_cell[1] #min_x & min_y нужны для того чтобы мы не вышли за пределы поля
        new_cells_shifted = []
        for cell in new_cells:
            new_cells_shifted.append((cell[0]-min_x+shift_x,
                                      cell[1]-min_y+shift_y))
        return new_cells_shifted
