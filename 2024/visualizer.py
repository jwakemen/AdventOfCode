from blessed import Terminal
import time
from typing import List

class GraphVisualizer:
    def __init__(self):
        self.term = Terminal()
        self.frames = 0
        self.num_lines = 0
        self.char_maps = {
            '#': self.term.blue_bold(u'\u2588'),
            '[': self.term.green_bold('['),
            ']': self.term.green_bold(']'),
            'O': self.term.green_bold('O'),
            '@': self.term.red_bold('@'),
            '*': self.term.red_bold(u'\u25CF'),
            '.': ' '
        }
        print(self.term.clear)

    def show_frame(self, graph: dict[tuple[int,int], str], frametime=0):
        """
        Print out a frame to the terminal. It will print on top of the last frame.

        graph: A dict of 2d locations where each location contains one character
        frametime: How long each frame should remain on the screen in seconds

        [0][0] is the top-left corner
        """
        print(self.term.home)
        max_x = max(x for x, _ in graph.keys())
        max_y = max(y for _, y in graph.keys())
        m = [[self.char_maps['.'] for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for (x, y), c in graph.items():
            if c in self.char_maps:
                m[x][y] = self.char_maps[c]
            else:
                m[x][y] = c

        info = f'Move: {self.frames+1}\n'
        frame = info + '\n'.join([''.join(row) for row in m])
        if self.frames == 0:
            self.num_lines = len(m)
        else:
            assert self.num_lines == len(m)

        print(frame)

        self.frames += 1
        time.sleep(frametime)

