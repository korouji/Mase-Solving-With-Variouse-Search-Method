import json
import time

def load_maze(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def print_path(grid, path):
    grid_copy = [row[:] for row in grid]
    for (x, y) in path:
        if grid_copy[y][x] == 0:
            grid_copy[y][x] = '*'
    symbols = {0: '.', 1: '#', 2: 'S', 3: 'G', '*': '*'}
    for row in grid_copy:
        print(''.join(symbols.get(c, str(c)) for c in row))

def dfs_with_stats(maze_data):
    grid = maze_data["grid"]
    start = tuple(maze_data["start"])
    goal = tuple(maze_data["goal"])

    width, height = maze_data["width"], maze_data["height"]
    stack = [start]
    visited = set()
    parent = {start: None}
    nodes_expanded = 0
    backtracks = 0

    start_time = time.time()

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and grid[y][x] != 1

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            break

        x, y = current
        moves = [(0,1),(1,0),(0,-1),(-1,0)]
        valid_moves = 0
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent[(nx, ny)] = current
                valid_moves += 1
        if valid_moves == 0:
            backtracks += 1

    end_time = time.time()

    # بازسازی مسیر
    path = []
    node = goal
    while node in parent and node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    if path and path[0] == start:
        print("DFS Result on JSON Maze:")
        print(f"Path length: {len(path)}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Backtracks: {backtracks}")
        print(f"Time: {end_time - start_time:.6f}s\n")
        print_path(grid, path)
    else:
        print("DFS failed to find a path.")

    return path

if __name__ == "__main__":
    maze_data = load_maze("maze1.json")
    dfs_with_stats(maze_data)
