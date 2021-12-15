"Utilities for processing, converting, and solving mazes of any type."

import heapq
from typing import Tuple, List, Dict, Iterator

from ktane.solverutils.grid import Dimensions, Coord

__all__ = ["Node", "Wall", "solve_maze"]

# A maze is a set of nodes plus a set of walls (prohibited connections)
# A node is simply a point in N-dimensional space (N-tuple)
# Pathfinding is done with A* using these nodes, plus a check for walls

# A regular maze has every possible node within its dimensions and a set of defined walls
# A Switches maze has every possible node minus a set of exceptions and no walls
# Hexamaze has a custom movement algorithm (instead of +1Y/+1X, +2Y/+1X+1Y)

# todo: have a function to convert an ascii maze to a group of Wall objects


class Node(Coord):
    "Node type for 2D square grid mazes. 0,0 is the top left."


class Wall(Coord):
    """Wall type for 2D square grid mazes.
    0,1 is the top left vertical wall, 1,0 is the top left horizontal wall.
    This grid has twice as many rows and columns as the maze.
    See maze_wall.png for a visual explanation."""


def _neighbors(current: Node, size: Dimensions,
               walls: Tuple[Wall, ...]) -> Iterator[Node]:
    "Given a node and context, generate neighbor nodes."
    if current.row > 0:  # up
        if Wall(2*current.row-1, 2*current.col) not in walls:
            yield Node(current.row-1, current.col)
    if current.row < size.rows-1:  # down
        if Wall(2*current.row+1, 2*current.col) not in walls:
            yield Node(current.row+1, current.col)
    if current.col > 0:  # left
        if Wall(2*current.row, 2*current.col-1) not in walls:
            yield Node(current.row, current.col-1)
    if current.col < size.cols-1:  # right
        if Wall(2*current.row, 2*current.col+1) not in walls:
            yield Node(current.row, current.col+1)


def _get_direction(previous: Node, current: Node) -> str:
    if previous.row > current.row and previous.col == current.col:  # up
        return "Up"
    if previous.row < current.row and previous.col == current.col:  # down
        return "Down"
    if previous.col > current.col and previous.row == current.row:  # left
        return "Left"
    if previous.col < current.col and previous.row == current.row:  # right
        return "Right"
    raise RuntimeError("Invalid maze solution direction produced.")


def _unwind_path(current: Node, came_from: Dict[Node, Node]) -> List[str]:
    directions: List[str] = []
    while current in came_from:
        previous = came_from[current]
        directions.append(_get_direction(previous, current))
        current = previous
    directions.reverse()  # we unpacked the directions in reverse order
    return directions


def solve_maze(size: Dimensions, start: Node, goal: Node,
               walls: Tuple[Wall, ...]) -> List[str]:
    """Given maze dimensions, starting and ending points, and a list of walls,
    return a list of directions to move from the start to the end."""
    unvisited: List[Tuple[int, Node]] = []
    distances: Dict[Node, int] = {}
    # For node n, came_from[n] is the node immediately preceding it on
    # the shortest path currently known.
    came_from: Dict[Node, Node] = {}
    distances[start] = 0
    heapq.heappush(unvisited, (0, start))
    while unvisited:  # Dijkstra's algorithm
        distance, current = heapq.heappop(unvisited)
        if current == goal:
            return _unwind_path(current, came_from)
        new_distance = distance + 1
        for neighbor in _neighbors(current, size, walls):
            if neighbor not in distances or distances[neighbor] > new_distance:
                distances[neighbor] = new_distance
                heapq.heappush(unvisited, (new_distance, neighbor))
                came_from[neighbor] = current
    return []  # no path found
