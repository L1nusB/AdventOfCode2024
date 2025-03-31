from typing import Set, Tuple, List
import numpy as np


def parse_input(filename: str) -> np.ndarray:
    """
    Read a text file containing numbers and convert to a 2D array.
    Each line in the file becomes a row in the array.
    Each character in the line becomes an element in the row.

    Args:
        filename (str): Path to the input file

    Returns:
        list: 2D array (list of lists) containing the numbers
    """
    with open(filename, 'r') as file:
        return np.array([[int(char) if char.isnumeric() else -1 for char in line.strip()] for line in file], dtype=np.int32)


def get_trailhead_starts(top_map: np.ndarray) -> np.ndarray:
    return np.asarray(np.nonzero(top_map == 0)).T


def traverse(top_map: np.ndarray,
             cur_pos: Tuple[int, int],
             cur_height: int,
             visited: Set[Tuple[int, int]],
             target_height: int = 9,
             allow_revists: bool = False
             ) -> Tuple[int, Set[Tuple[int, int]]]:
    """Uses stateful or stateless DFS (depth-first search).
    In stateful mode keeps track of all visited fields to avoid loops and revisiting i.e. only checking if a path is a valid trailhead.
    In stateless count all distinct trails."""
    if not allow_revists:
        # Check if already visited current position
        if cur_pos in visited:
            return 0, visited
    visited.add(cur_pos)

    # If target height/peak has been reached register as valid trailhead
    if cur_height >= target_height:
        return 1, visited

    next_steps = [(cur_pos[0]+1, cur_pos[1]),  # Move down
                  (cur_pos[0]-1, cur_pos[1]),  # Move up
                  (cur_pos[0], cur_pos[1]+1),  # Move right
                  (cur_pos[0], cur_pos[1]-1)]  # Move left
    # Filter steps outside the boundaries
    next_steps = [(i, j) for i, j in next_steps if (
        (i >= 0 and i < top_map.shape[0]) and (j >= 0 and j < top_map.shape[1]))]
    valid_heads = 0
    for step in next_steps:
        if top_map[*step] == cur_height+1:
            valid_sub_heads, visited = traverse(
                top_map, step, cur_height+1, visited, target_height, allow_revists)
            valid_heads += valid_sub_heads
    return valid_heads, visited


if __name__ == "__main__":
    # top_map = parse_input("Day10/test.txt")
    # top_map = parse_input("Day10/test2.txt")
    # top_map = parse_input("Day10/test3.txt")
    # top_map = parse_input("Day10/test4.txt")
    # top_map = parse_input("Day10/test5.txt")
    # top_map = parse_input("Day10/input.txt")
    # trailheads = get_trailhead_starts(top_map)
    # trailhead_values = [traverse(top_map, tuple(start), 0, set(), 9)[
    #     0] for start in trailheads]
    # score = sum(trailhead_values)
    # print(score)
    ### Finish Part 1 ###
    # top_map = parse_input("Day10/test6.txt")
    # top_map = parse_input("Day10/test7.txt")
    top_map = parse_input("Day10/input.txt")
    trailheads = get_trailhead_starts(top_map)
    trailhead_values = [traverse(top_map, tuple(start), 0, set(), 9, True)[
        0] for start in trailheads]
    score = sum(trailhead_values)
    print(score)
    a = 0
