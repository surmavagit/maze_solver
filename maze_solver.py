from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")

        self.canvas = Canvas(self.__root, height=height, width=width)
        self.canvas.pack()

        self.running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            fill=fill_color,
            width=2
            )
        canvas.pack()

class Cell:
    def __init__(self, window = None):
        self.has_west_wall = True
        self.has_east_wall = True
        self.has_north_wall = True
        self.has_south_wall = True
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = window

    def draw(self, x_nw, y_nw, x_se, y_se):
        self._x1 = x_nw
        self._y1 = y_nw
        self._x2 = x_se
        self._y2 = y_se
        west_wall = Line(Point(x_nw, y_nw), Point(x_nw, y_se))
        east_wall = Line(Point(x_se, y_nw), Point(x_se, y_se))
        north_wall = Line(Point(x_nw, y_nw), Point(x_se, y_nw))
        south_wall = Line(Point(x_nw, y_se), Point(x_se, y_se))
        west_wall_color = "white"
        east_wall_color = "white"
        north_wall_color = "white"
        south_wall_color = "white"
        if self.has_west_wall:
            west_wall_color = "black"
        if self.has_east_wall:
            east_wall_color = "black"
        if self.has_north_wall:
            north_wall_color = "black"
        if self.has_south_wall:
            south_wall_color = "black"
        self._win.draw_line(west_wall, west_wall_color)
        self._win.draw_line(east_wall, east_wall_color )
        self._win.draw_line(north_wall, north_wall_color )
        self._win.draw_line(south_wall, south_wall_color )

    def draw_move(self, to_cell, undo=False):
        center = Point((self._x1 + self._x2)//2, (self._y1 + self._y2)//2)
        new_center = Point((to_cell._x1 + to_cell._x2)//2, (to_cell._y1 + to_cell._y2)//2)
        color = "red"
        if undo:
            color = "grey"
        self._win.draw_line(Line(center, new_center), color)

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None
            ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for c in range(self.num_cols):
            row = []
            for r in range(self.num_rows):
                cell = Cell(self.win)
                row.append(cell)
            self._cells.append(row)

        if self.win is not None:
            for i in range(self.num_cols):
                for j in range(self.num_rows):
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell_y = self.y1 + i * self.cell_size_y
        cell_x = self.x1 + j * self.cell_size_x
        self._cells[i][j].draw(cell_x, cell_y, cell_x + self.cell_size_x, cell_y + self.cell_size_y)

        self._animate()

    def _animate(self):
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_north_wall = False
        if self.win is not None:
            self._draw_cell(0, 0)

        exit_col = self._cells[len(self._cells) - 1]
        exit_cell = exit_col[len(exit_col) - 1]
        exit_cell.has_south_wall = False
        if self.win is not None:
            self._draw_cell(len(self._cells) - 1, len(exit_col) - 1)

def main():
    #print("running main")
    win = Window(800, 600)
    maze = Maze(20, 20, 10, 10, 50, 50, win)
    maze._break_entrance_and_exit()

    win.wait_for_close()

main()
