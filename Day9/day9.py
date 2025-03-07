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
    print(discmap.tolist())
    return discmap
    
    
if __name__ == "__main__":
    # input = extract_data("Day9/input.txt")
    input = extract_data("Day9/test1.txt")
    org_discmap = create_discmap(input)
    input = extract_data("Day9/test2.txt")
    org_discmap = create_discmap(input)
    a = 0