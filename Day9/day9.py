import numpy as np
from typing import List, Optional

def extract_data(path: str) -> str:
    with open(path, "r") as f:
        dat = f.read()
    return dat 

def create_discmap(input: str) -> np.ndarray:
    arr = np.array(list(input.strip()), dtype=int)
    discmap = np.zeros(shape=arr.sum(), dtype=int)
    file_blocks, free_blocks = arr[::2], arr[1::2]
    start = 0
    for id, (file_size, free_size) in enumerate(zip(file_blocks, free_blocks)):
        discmap[start:start+file_size] = id
        discmap[start+file_size:start+file_size+free_size] = -1
        start += file_size+free_size
    # Last fileblock needs to be set manually since it does not have a corresponding free block
    # and thus is not covered by the zipping
    discmap[-file_blocks[-1]:] = len(file_blocks)-1
    return discmap

def create_discmap_optimized(input: str) -> np.ndarray:
    """Optimized version of create_discmap using numpy's capabilities based on Claude Sonnet 3.7"""
    arr = np.array(list(input.strip()), dtype=int)
    
    # Get file and free block lengths
    file_blocks, free_blocks = arr[::2], arr[1::2]
    
    # Append 0 to free_blocks if needed (to handle the last file block)
    if len(file_blocks) > len(free_blocks):
        free_blocks = np.append(free_blocks, 0)
    
    # Create block pairs and their corresponding ids
    block_lengths = np.column_stack((file_blocks, free_blocks)).flatten()
    ids = np.repeat(np.arange(len(file_blocks)), 2)
    
    # Create mask for free blocks
    is_free_block = np.zeros_like(ids, dtype=bool)
    is_free_block[1::2] = True
    
    # Repeat each id/free indicator according to block length
    repeated_ids = np.repeat(ids, block_lengths)
    repeated_is_free = np.repeat(is_free_block, block_lengths)
    
    # Set final values (-1 for free blocks, otherwise use ids)
    discmap = np.where(repeated_is_free, -1, repeated_ids)
    
    return discmap
    
if __name__ == "__main__":
    # input = extract_data("Day9/input.txt")
    # input = extract_data("Day9/test1.txt")
    # org_discmap = create_discmap(input)
    input = extract_data("Day9/test2.txt")
    org_discmap = create_discmap(input)
    a = 0