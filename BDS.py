import json
import time
from collections import deque

def load_maze(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def print_path(grid, path, start, goal):
    grid_copy = [row[:] for row in grid]
    for (x, y) in path:
        if grid_copy[y][x] == 0:
            grid_copy[y][x] = '*'
    grid_copy[start[1]][start[0]] = 'S'
    grid_copy[goal[1]][goal[0]] = 'G'

    symbols = {0: '.', 1: '#', 2: 'S', 3: 'G', '*': '*'}
    for row in grid_copy:
        print(''.join(symbols.get(c, str(c)) for c in row))

def bidirectional_search(maze_data):
    grid = maze_data["grid"]
    start = tuple(maze_data["start"])
    goal = tuple(maze_data["goal"])
    width, height = maze_data["width"], maze_data["height"]

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and grid[y][x] != 1

    front_start = deque([start])
    front_goal = deque([goal])
    visited_start = {start}
    visited_goal = {goal}
    parent_start = {start: None}
    parent_goal = {goal: None}

    nodes_expanded = 0
    meeting_node = None
    directions = [(-1,0),(1,0),(0,-1),(0,1)]  # L,R,U,D
    start_time = time.time()

    while front_start and front_goal:
        if front_start:
            current_start = front_start.popleft()
            nodes_expanded += 1
            for dx, dy in directions:
                nx, ny = current_start[0]+dx, current_start[1]+dy
                neighbor = (nx, ny)
                if is_valid(nx, ny) and neighbor not in visited_start:
                    parent_start[neighbor] = current_start
                    visited_start.add(neighbor)
                    front_start.append(neighbor)
                    if neighbor in visited_goal:
                        meeting_node = neighbor
                        break
            if meeting_node:
                break

        if front_goal:
            current_goal = front_goal.popleft()
            nodes_expanded += 1
            for dx, dy in directions:
                nx, ny = current_goal[0]+dx, current_goal[1]+dy
                neighbor = (nx, ny)
                if is_valid(nx, ny) and neighbor not in visited_goal:
                    parent_goal[neighbor] = current_goal
                    visited_goal.add(neighbor)
                    front_goal.append(neighbor)
                    if neighbor in visited_start:
                        meeting_node = neighbor
                        break
            if meeting_node:
                break

    end_time = time.time()

    if not meeting_node:
        print("couldnot find a path.")
        return []

    path_start = []
    node = meeting_node
    while node:
        path_start.append(node)
        node = parent_start[node]
    path_start.reverse()

    path_goal = []
    node = parent_goal[meeting_node]
    while node:
        path_goal.append(node)
        node = parent_goal[node]

    path = path_start + path_goal
    print_path(grid, path, start, goal)
    print("Bidirectional Search Result:")
    print(f"Path length: {len(path)}")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Time: {end_time - start_time:.6f}s\n")
    

    return path

if __name__ == "__main__":
    maze_data = load_maze("maze1.json")
    bidirectional_search(maze_data)
