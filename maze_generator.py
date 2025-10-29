# Maze Engine 

"""
MazeEngine.py

Clean, fully functional Maze Engine with:
- Custom maze creation
- Walls, free paths, start and goal
- ASCII display
- Save/load JSON
- Ready for search algorithm integration
"""

import json
import math
import heapq
from collections import deque

class MazeEngine:
    FREE = 0
    WALL = 1
    START = 2
    GOAL = 3

    def __init__(self, width=41, height=41, default=FREE):
        self.width = width
        self.height = height
        self.grid = [[MazeEngine.FREE for _ in range(width)] for _ in range(height)]
        self.start = None
        self.goal = None
        self.costs = None

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] != MazeEngine.WALL

    def set_cell(self, x, y, value):
        assert value in (MazeEngine.FREE, MazeEngine.WALL, MazeEngine.START, MazeEngine.GOAL)
        assert self.in_bounds(x, y)
        if value == MazeEngine.START:
            if self.start:
                sx, sy = self.start
                self.grid[sy][sx] = MazeEngine.FREE
            self.start = (x, y)
        elif value == MazeEngine.GOAL:
            if self.goal:
                gx, gy = self.goal
                self.grid[gy][gx] = MazeEngine.FREE
            self.goal = (x, y)
        self.grid[y][x] = value

    def toggle_wall(self, x, y):
        if self.in_bounds(x, y):
            if self.grid[y][x] == MazeEngine.WALL:
                self.grid[y][x] = MazeEngine.FREE
            else:
                if self.start == (x, y): self.start = None
                if self.goal == (x, y): self.goal = None
                self.grid[y][x] = MazeEngine.WALL

    def set_start(self, pos):
        x, y = pos
        assert self.is_free(x, y)
        self.set_cell(x, y, MazeEngine.START)

    def set_goal(self, pos):
        x, y = pos
        assert self.is_free(x, y)
        self.set_cell(x, y, MazeEngine.GOAL)

    def neighbors4(self, x, y):
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if self.is_free(nx, ny):
                yield nx, ny

    def get_cost(self, x, y):
        if not self.is_free(x, y):
            return math.inf
        return self.costs[y][x] if self.costs else 1

    def ascii(self, path=None):
        path_set = set(path) if path else set()
        lines = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                if (x,y) in path_set:
                    row += '*'
                elif self.start == (x,y):
                    row += 'S'
                elif self.goal == (x,y):
                    row += 'G'
                elif self.grid[y][x] == MazeEngine.WALL:
                    row += '#'
                else:
                    row += '.'
            lines.append(row)
        return '\n'.join(lines)

    def print_ascii(self, path=None):
        print(self.ascii(path))

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'width':self.width,'height':self.height,'grid':self.grid,'start':self.start,'goal':self.goal,'costs':self.costs}, f, indent=2)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        eng = cls(data['width'], data['height'])
        eng.grid = data['grid']
        eng.start = tuple(data['start']) if data['start'] else None
        eng.goal = tuple(data['goal']) if data['goal'] else None
        eng.costs = data.get('costs')
        return eng

# Simple console editor, no recursion
def simple_console_editor(engine):
    print('Simple Console Maze Editor')
    print('Commands: wall x y | free x y | start x y | goal x y | toggle x y | save filename | load filename | show | exit')
    while True:
        cmd = input('> ').strip()
        if not cmd: continue
        parts = cmd.split()
        if parts[0] == 'exit': break
        if parts[0] == 'show': engine.print_ascii(); continue
        if parts[0] == 'wall' and len(parts)==3: engine.set_cell(int(parts[1]), int(parts[2]), MazeEngine.WALL); continue
        if parts[0] == 'free' and len(parts)==3: engine.set_cell(int(parts[1]), int(parts[2]), MazeEngine.FREE); continue
        if parts[0] == 'toggle' and len(parts)==3: engine.toggle_wall(int(parts[1]), int(parts[2])); continue
        if parts[0] == 'start' and len(parts)==3: engine.set_start((int(parts[1]), int(parts[2]))); continue
        if parts[0] == 'goal' and len(parts)==3: engine.set_goal((int(parts[1]), int(parts[2]))); continue
        if parts[0] == 'save' and len(parts)==2: engine.save_to_file(parts[1]); continue
        if parts[0] == 'load' and len(parts)==2: engine.__dict__.update(MazeEngine.load_from_file(parts[1]).__dict__); continue
        print('Unknown or malformed command')

if __name__ == '__main__':
    eng = MazeEngine(41, 41)
    for x in range(eng.width):
        eng.set_cell(x, 0, MazeEngine.WALL)
        eng.set_cell(x, eng.height-1, MazeEngine.WALL)
    for y in range(eng.height):
        eng.set_cell(0, y, MazeEngine.WALL)
        eng.set_cell(eng.width-1, y, MazeEngine.WALL)
    for x in range(3, eng.width-3): eng.set_cell(x,3,MazeEngine.WALL)
    eng.set_start((1,1))
    eng.set_goal((eng.width-2, eng.height-2))
    print('Initial Maze:')
    eng.print_ascii()
    print('\nYou can run the simple console editor now:')
    simple_console_editor(eng)
