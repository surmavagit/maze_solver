from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, window):
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
        if self.has_west_wall:
            wall = Line(Point(x_nw, y_nw), Point(x_nw, y_se))
            self._win.draw_line(wall, "black")
        if self.has_east_wall:
            wall = Line(Point(x_se, y_nw), Point(x_se, y_se))
            self._win.draw_line(wall, "black")
        if self.has_north_wall:
            wall = Line(Point(x_nw, y_nw), Point(x_se, y_nw))
            self._win.draw_line(wall, "black")
        if self.has_south_wall:
            wall = Line(Point(x_nw, y_se), Point(x_se, y_se))
            self._win.draw_line(wall, "black")

    def draw_move(self, to_cell, undo=False):
        center = Point((self._x1 + self._x2)//2, (self._y1 + self._y2)//2)
        new_center = Point((to_cell._x1 + to_cell._x2)//2, (to_cell._y1 + to_cell._y2)//2)
        self._win.draw_line(Line(center, new_center), "red")

def main():
    win = Window(800, 600)
    cell_a = Cell(win)
    cell_a.has_east_wall = False
    cell_a.draw(20, 20, 40, 40)
    cell_b = Cell(win)
    cell_b.has_west_wall = False
    cell_b.draw(40, 20, 60, 40)
    cell_c = Cell(win)
    cell_c.draw(60, 40, 80, 60)
    cell_a.draw_move(cell_b)

    win.wait_for_close()

main()
