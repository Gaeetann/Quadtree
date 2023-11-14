from __future__ import annotations
import ast
from decimal import Decimal as D
from tkinter import Tk, Canvas as Cv

class QuadTree:
    NB_NODES : int = 4
    def __init__(self, hg: bool | QuadTree, hd: bool | QuadTree, bd: bool | QuadTree,bg: bool | QuadTree):
        self.bg = bg
        self.bd = bd
        self.hd = hd
        self.hg = hg

    @property
    def depth(self) -> int:
        """ Recursion depth of the quadtree"""
        child_depths = [child.depth if isinstance(child, QuadTree) else 0 for child in
                        [self.hg, self.hd, self.bd, self.bg]]
        return max(child_depths) + 1


    @staticmethod
    def fromFile(filename: str) -> QuadTree:
        """ Open a given file, containing a textual representation of a list"""
        with open(filename) as file:
            files = ast.literal_eval(file.read())
            file.close()
        return QuadTree.fromList(files)


    @staticmethod
    def fromList(data: list) -> QuadTree:
        """ Generates a Quadtree from a list representation"""
        if QuadTree.NB_NODES == len(data):
            return QuadTree(
                QuadTree.fromList(data[0]) if isinstance(data[0], list) else data[0],
                QuadTree.fromList(data[1]) if isinstance(data[1], list) else data[1],
                QuadTree.fromList(data[2]) if isinstance(data[2], list) else data[2],
                QuadTree.fromList(data[3]) if isinstance(data[3], list) else data[3]
            )



class TkQuadTree(QuadTree):
    def __init__(self, data: list, size: int, x_val: int, y_val: int):
        self.data = data
        self.size = size
        self.x_val = x_val
        self.y_val = y_val

    def initialize(self):
        root = Tk()
        root.title("Tree")
        canvas = Cv(root, width=self.size, height=self.size)
        canvas.pack()
        max_sz = D(self.size) / D(2)
        self.paint(self.data, max_sz, canvas, self.x_val, self.y_val)
        root.mainloop()

    def paint(self, data: list, mx_sz: D, canvas: Cv, x: int, y: int):
        for index, child in enumerate(data, start=1):
            if index == 3:
                y += mx_sz
                x -= mx_sz
            elif index % 2 == 0:
                x += mx_sz

            if isinstance(child, list):
                self.paint(child, D(mx_sz) / D(2), canvas, x, y)
            else:
                fill_color = "brown" if child else "green"
                canvas.create_rectangle(x, y, x + mx_sz, y + mx_sz, fill=fill_color)


if __name__ == "__main__":
    TkQuadTree(
        [
            [0, 0, 0, [1, 0, 0, 0]],
            [0, 0, [0, 1, 0, 0], 0],
            [0, 0, 0, [[1, 0, 0, 1], [0, 0, 1, 1], 0, 0]],
            [0, 0, [[0, 0, 1, 1], [0, 1, 1, 0], 0, 0], 0]
        ],
        700, 0, 0
    ).initialize()

