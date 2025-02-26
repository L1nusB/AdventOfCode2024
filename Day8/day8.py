import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Callable

def max_scaling_factors(grid_bounds, start_position, distance_vector):
    """
    Determines the maximum scaling factors to move within bounds of a 2D grid.

    Parameters:
        grid_bounds (tuple): A tuple (rows, cols) representing the grid dimensions.
        start_position (tuple): A tuple (x, y) for the starting position in the grid.
        distance_vector (tuple): A tuple (dx, dy) representing the direction vector.

    Returns:
        tuple: A tuple (max_forward, max_backward) of scaling factors.
    """
    rows, cols = grid_bounds
    x, y = start_position
    dx, dy = distance_vector

    def compute_scaling(dx, dy, x, y, rows, cols, round: bool = True):
        max_scale = float('inf')

        if dx > 0:
            max_scale = min(max_scale, (cols - 1 - x) / dx)
        elif dx < 0:
            max_scale = min(max_scale, -x / dx)

        if dy > 0:
            max_scale = min(max_scale, (rows - 1 - y) / dy)
        elif dy < 0:
            max_scale = min(max_scale, -y / dy)

        return int(max_scale) if round else max_scale

    max_forward = compute_scaling(dx, dy, x, y, rows, cols)
    max_backward = compute_scaling(-dx, -dy, x, y, rows, cols)

    return -max_backward, max_forward

def extract_data(filename: str) -> np.ndarray:
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    return np.array([list(d) for d in data])

def set_antinodes_frequency_location(antinodes: NDArray[np.int_], loc: Tuple[int,int], locations: NDArray[np.int_], resonant_harmonics: bool = False) -> None:
    # Calculate distances and vectors
    distances = locations - loc
    if resonant_harmonics:
        filtered_antinode_pos = np.concatenate([[loc + scale*d for scale in range(max_scaling_factors(antinodes.shape, loc, d)[0],max_scaling_factors(antinodes.shape, loc, d)[1]+1)] for d in distances])
    else:
        antinode_pos = np.array([[loc + 2*d, loc - d] for d in distances])
        antinode_pos = antinode_pos.reshape(-1, antinode_pos.shape[-1])
        
        # Remove antinodes that are outside the field (first to the left and top, second to the bottom and third to the right)
        filtered_antinode_pos = np.array([pos for pos in antinode_pos if all(pos>=0) and pos[0]<antinodes.shape[0] and pos[1]<antinodes.shape[1]])
    
    # Set antinode values
    # Only if there are any remaining otherwise everything will be set
    if filtered_antinode_pos.size > 0:
        antinodes[tuple(filtered_antinode_pos.T)] = 1


def set_antinodes_frequency(antennas: NDArray[np.str_], antinodes: NDArray[np.int_], freq: str, resonant_harmonics: bool = False) -> None:
    locations = np.argwhere(antennas==freq)
    filtered_locations = locations.copy()
    for loc in locations:
        # Remove element of location
        filtered_locations = np.delete(filtered_locations, np.argwhere((filtered_locations==loc).all(axis=1)), axis=0)
        # Terminate if no further locations remain
        if filtered_locations.size > 0:
            set_antinodes_frequency_location(antinodes,loc=loc, locations=filtered_locations, resonant_harmonics=resonant_harmonics)
        else:
            break
        # visual_antinodes = np.full_like(antinodes, '.', dtype=np.str_)
        # visual_antinodes[antinodes==1] = '#'
        # visual_antinodes = np.where(antennas!='.', antennas, visual_antinodes)
        # with open(f'Day8/Output/output{freq}-{loc[0]}_{loc[1]}.txt', 'w') as f:
        #     np.savetxt(f, visual_antinodes, fmt="%s")

def construct_antinodes(antennas: NDArray[np.str_], resonant_harmonics: bool = False) -> NDArray[np.int_]:
    antinodes = np.zeros_like(antennas, dtype=int)
    frequencies = np.unique(antennas[antennas!='.'])
    [set_antinodes_frequency(antennas, antinodes, freq, resonant_harmonics) for freq in frequencies]
    return antinodes

if __name__ == '__main__':
    antennas = extract_data("Day8/input.txt")
    print(antennas)
    antinodes = construct_antinodes(antennas)
    # print(antinodes)
    visual_antinodes = np.full_like(antinodes, '.', dtype=np.str_)
    visual_antinodes[antinodes==1] = '#'
    visual_antinodes = np.where(antennas!='.', antennas, visual_antinodes)
    print(visual_antinodes)
    print(antinodes.sum())
    
    print("--------- Part 2 ----------")
    
    antinodes = construct_antinodes(antennas, True)
    visual_antinodes = np.full_like(antinodes, '.', dtype=np.str_)
    visual_antinodes[antinodes==1] = '#'
    visual_antinodes = np.where(antennas!='.', antennas, visual_antinodes)
    print(visual_antinodes)
    print(antinodes.sum())