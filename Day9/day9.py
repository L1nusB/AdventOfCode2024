import numpy as np
from typing import List, Tuple

def extract_data(path: str) -> str:
    with open(path, "r") as f:
        dat = f.read()
    return dat 

def create_discmap(input: str) -> Tuple[np.ndarray, np.ndarray]:
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
    return discmap, file_blocks

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

def reorder_disc(discmap: np.ndarray, file_length: int) -> np.ndarray:
    # Only the positions after the final desired size need to be considered for reorder
    reorder_blocks = discmap[file_length:]
    # Remove entries for free blocks
    reorder_blocks = reorder_blocks[reorder_blocks!=-1]
    # Since we put the blocks from back to front reverse the data and then go from the front
    reorder_blocks = np.flip(reorder_blocks)
    reordered_discmap = discmap.copy()[:file_length]
    reordered_discmap[reordered_discmap==-1] = reorder_blocks
    reordered_discmap[file_length:] = -1
    return reordered_discmap

def calc_checksum(discmap: np.ndarray, file_length: int) -> int:
    mult_map = discmap[:file_length] * np.arange(file_length, dtype=int)
    return mult_map.sum()
    
if __name__ == "__main__":
    input = extract_data("Day9/input.txt")
    # input = extract_data("Day9/test1.txt")
    # org_discmap = create_discmap(input)
    # input = extract_data("Day9/test2.txt")
    org_discmap, file_blocks = create_discmap(input)
    file_length = file_blocks.sum()
    reordered_discmap = reorder_disc(org_discmap, file_length)
    checksum = calc_checksum(reordered_discmap, file_length)
    print(checksum)