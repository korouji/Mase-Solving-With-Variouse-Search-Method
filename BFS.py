import json
from collections import deque
import time

def load_maze_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['grid'], tuple(data['start']), tuple(data['goal'])

def neighbors(grid, x, y):
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x+dx, y+dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != 1:  # دیوار نیست
                yield nx, ny

def bfs_json(grid, start, goal):
    start_time = time.time()
    queue = deque([start])
    came_from = {start: None}
    nodes_expanded = 0
    backtracks = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        neighbors_list = list(neighbors(grid, *current))
        if not neighbors_list:
            backtracks += 1
        for nx, ny in neighbors_list:
            if (nx, ny) not in came_from:
                queue.append((nx, ny))
                came_from[(nx, ny)] = current
        if current == goal:
            break

    # بازسازی مسیر
    path = []
    current = goal
    while current and current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()

    elapsed_time = time.time() - start_time

    return {
        'path': path,
        'nodes_expanded': nodes_expanded,
        'backtracks': backtracks,
        'time': elapsed_time
    }

def print_ascii(grid, path, start, goal):
    path_set = set(path)
    for y, row in enumerate(grid):
        line = ''
        for x, cell in enumerate(row):
            if (x, y) in path_set:
                line += '*'
            elif (x, y) == start:
                line += 'S'
            elif (x, y) == goal:
                line += 'G'
            elif cell == 1:
                line += '#'
            else:
                line += '.'
        print(line)


grid, start, goal = load_maze_from_file('maze1.json')
result = bfs_json(grid, start, goal)

print("BFS Result on JSON Maze:")
print(f"Path length: {len(result['path'])}")
print(f"Nodes expanded: {result['nodes_expanded']}")
print(f"Backtracks: {result['backtracks']}")
print(f"Time: {result['time']:.6f}s\n")

print_ascii(grid, result['path'], start, goal)
