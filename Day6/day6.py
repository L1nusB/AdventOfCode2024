import numpy as np
from typing import Dict, Set, List, Tuple
from numpy.typing import NDArray

def convert_strings_to_array(string_array: List[str], rules=None) -> NDArray[np.int_]:
    if not rules:
        rules = {'.':0,'#':-1,'^':2,'>':3,'v':4,'<':5}
    number_lists = [[rules.get(char, 0) for char in s] for s in string_array]
    return np.array(number_lists, dtype=int)

def go_up(maze: NDArray[np.int_], cur_pos: NDArray[np.int_]) -> None:
    col = maze[:,cur_pos[1]]
    closest_obstacle = np.argwhere(col==-1)
    # Default value if no obstacle can be found
    if closest_obstacle.size==0:
        #print("No obstacle above. Moving to the top of the maze")
        # Set to -1 because we subtract for distance calculation and thereby would not reach the border
        closest_obstacle = -1
    else:
        # Only consider elements that are above the current position
        closest_obstacle = np.array([co for co in closest_obstacle if co < cur_pos[0]])
        # Check if "closest" object is below the guard --> Then we move to the top of the maze
        if closest_obstacle.size == 0:
            #print("No obstacle above. Moving to the top of the maze")
            # Set to -1 because we subtract for distance calculation and thereby would not reach the border
            closest_obstacle = -1
        else:
            # Scan from the top as we are going up 
            closest_obstacle = closest_obstacle.max()
    # Subtract 1 because we do not want to overwrite the obstacle
    distance = cur_pos[0]-closest_obstacle-1 
    new_position = tuple([cur_pos[0]-distance,cur_pos[1]])
    # Add one as the guard has moved from the original position and thus we overwrite it
    maze[new_position[0]:cur_pos[0]+1, cur_pos[1]] = 1
    # Make a 90 degree turn --> Next orientation is to the right
    maze[new_position] = 3
    

def go_down(maze: NDArray[np.int_], cur_pos: NDArray[np.int_]) -> None:
    col = maze[:,cur_pos[1]]
    # Scan from the bottom (max) as we are going down
    closest_obstacle = np.argwhere(col==-1)
    # Default value if no obstacle can be found
    if closest_obstacle.size==0:
        #print("No obstacle below. Moving to the bottom of the maze")
        closest_obstacle = maze.shape[1]
    else:
        # Only consider elements that are below the current position
        closest_obstacle = np.array([co for co in closest_obstacle if co > cur_pos[0]])
        # Check if "closest" object is above the guard --> Then we move to the bottom of the maze
        if closest_obstacle.size == 0:
            #print("No obstacle below. Moving to the bottom of the maze")
            closest_obstacle = maze.shape[1]
        else:
            # Scan from the bottom as we are going up 
            closest_obstacle = closest_obstacle.min()
    # Don't subtract 1 because we we are going down and thus indexing is fine
    distance = closest_obstacle-cur_pos[0]
    new_position = tuple([cur_pos[0]+distance-1,cur_pos[1]])
    maze[cur_pos[0]:new_position[0], cur_pos[1]] = 1
    # Make a 90 degree turn --> Next orientation is to the left
    maze[new_position] = 5

def go_left(maze: NDArray[np.int_], cur_pos: NDArray[np.int_]) -> None:
    row = maze[cur_pos[0],:]
    closest_obstacle = np.argwhere(row==-1)
    
    # Default value if no obstacle can be found
    if closest_obstacle.size==0:
        #print("Only obstacle to the right. Moving to the left of the maze")
        # Set to -1 because we subtract for distance calculation and thereby would not reach the border
        closest_obstacle = -1
    else:
        # Only consider elements that are to the left the current position
        closest_obstacle = np.array([co for co in closest_obstacle if co < cur_pos[1]])
        # Check if "closest" object is right the guard --> Then we move to the left of the maze
        if closest_obstacle.size == 0:
            #print("Only obstacle to the right. Moving to the left of the maze")
            # Set to -1 because we subtract for distance calculation and thereby would not reach the border
            closest_obstacle = -1
        else:
            # Scan from the left as we are going left
            closest_obstacle = closest_obstacle.max()
    
    # Subtract 1 because we do not want to overwrite the obstacle
    distance = cur_pos[1]-closest_obstacle-1
    new_position = tuple([cur_pos[0],cur_pos[1]-distance])
    # Add one as the guard has moved from the original position and thus we overwrite it
    maze[cur_pos[0], new_position[1]:cur_pos[1]+1] = 1
    # Make a 90 degree turn --> Next orientation is to the up
    maze[new_position] = 2

def go_right(maze: NDArray[np.int_], cur_pos: NDArray[np.int_]) -> None:
    row = maze[cur_pos[0],:]
    closest_obstacle = np.argwhere(row==-1)
    
    # Default value if no obstacle can be found
    if closest_obstacle.size==0:
        #print("Only obstacle to the left. Moving to the right of the maze")
        closest_obstacle = maze.shape[0]
    else:
        # Only consider elements that are to the right the current position
        closest_obstacle = np.array([co for co in closest_obstacle if co > cur_pos[1]])
        # Check if "closest" object is left the guard --> Then we move to the right of the maze
        if closest_obstacle.size == 0:
            #print("Only obstacle to the left. Moving to the right of the maze")
            closest_obstacle = maze.shape[0]
        else:
            # Scan from the right as we are going right
            closest_obstacle = closest_obstacle.min()
    
    # Subtract 1 because we do not want to overwrite the obstacle
    distance = closest_obstacle-cur_pos[1]-1 
    new_position = tuple([cur_pos[0],cur_pos[1]+distance])
    # Add one as the guard has moved from the original position and thus we overwrite it
    maze[cur_pos[0], cur_pos[1]:new_position[1]] = 1
    # Make a 90 degree turn --> Next orientation is to the down
    maze[new_position] = 4

def traverse_maze(maze: NDArray[np.int_], visited_positions: List[Tuple[Tuple[int, int], int]]) -> bool:
    curr_pos = np.argwhere(maze>=2)[0]
    # Check if border of maze has been reached (-1 as shape is not 0-indexed)
    if curr_pos[0]<= 0 or curr_pos[1] <= 0 or curr_pos[0] >= maze.shape[0]-1 or curr_pos[1] >= maze.shape[1]-1:
        #print("Guard has reached the end of the maze")
        # Set the final element as a "visited" field
        maze[tuple(curr_pos)] = 1
        #print(maze)
        return 0
    if tuple(curr_pos) in [vp for vp,_ in visited_positions]:
        #print(f"Already visited {curr_pos} checking for orientation")
        if any(e==maze[tuple(curr_pos)] for e in [d for vp,d in visited_positions if vp==tuple(curr_pos)]):
            print(f"Same orientation and position {tuple(curr_pos)}. Guard is walking in a circle")
            return 1
        #else:
            #print(f'New orientation: {maze[tuple(curr_pos)]}')
    visited_positions.append([tuple(curr_pos)] + [maze[tuple(curr_pos)]])
    match maze[tuple(curr_pos)]:
        case 2:
            #print("Going up")
            go_up(maze, curr_pos)
            #print(maze)
        case 3:
            #print("Going right")
            go_right(maze, curr_pos)
            #print(maze)
        case 4:
            #print("Going down")
            go_down(maze, curr_pos)
            #print(maze)
        case 5:
            #print("Going left")
            go_left(maze, curr_pos)
            #print(maze)
        case _:
            raise ValueError(f'Invalid value for direction: {maze[curr_pos]}')
    return traverse_maze(maze, visited_positions)

if __name__=='__main__':
    with open("Day6/input.txt", "r") as f:
        maze = np.array(f.read().splitlines())
    maze = convert_strings_to_array(maze)
    #print(maze)
    print("Checking of unobstructed total traversed fields")
    num_traversed_fields = np.sum(maze==1)
    print(num_traversed_fields)
    
    print("Checking for blocks")
    blocked = 0
    cur_pos = tuple(np.argwhere(maze>=2)[0])
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if (i,j) == cur_pos:
                continue
            print(f"Blocking position {i,j}")
            blocked_maze = maze.copy()
            blocked_maze[i,j] = -1
            blocked += traverse_maze(blocked_maze, [])
    # Divide by two 
    print(blocked)