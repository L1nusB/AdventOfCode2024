import numpy as np
from typing import List, Tuple, Callable
from itertools import product
from operator import mul, add

def extract_data(filename: str) -> List[Tuple[int, List[int]]]:
    """
    Extract data from a text file where each line is formatted as 'key: value1 value2 ...'
    
    Args:
        filename: Path to the input text file
    
    Returns:
        A list of lists, where each inner list contains the key and a list of its associated values
    """
    # Initialize an empty list to store the parsed data
    parsed_data: List[List[int]] = []
    
    # Open and read the file
    with open(filename, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Strip any whitespace and split the line at the colon
            parts = line.strip().split(':')
            
            # The first part is the key number
            key: int = int(parts[0])
            
            # The second part contains the list of numbers
            # Split by whitespace and convert to integers
            numbers: List[int] = [int(num) for num in parts[1].strip().split()]
            
            # Append the parsed entry to the list
            parsed_data.append(tuple([key, numbers]))
    
    return parsed_data

def concat(num1: int, num2: int) -> int:
    return int(f"{num1}{num2}")

def check_equation(eq: Tuple[int, List[int]], operators: List[Callable] = [mul, add]) -> bool:
    def apply_operands_right_to_left(numbers: List[int], operands: List[Callable[[int,int],int]]) -> int:
        if len(numbers)==1:
            return numbers[0]
        return operands[0](numbers[0], apply_operands_right_to_left(numbers[1:], operands[1:]))
    def apply_operands_left_to_right(numbers: List[int], operands: List[Callable[[int,int],int]], target: int) -> int:
        current = numbers[0]
        for num, op in zip(numbers[1:], operands):
            # Fast terminate if target already exceeded
            if current > target:
                return current
            current = op(current, num)
        return current
        
    result, numbers = eq
    operations = list(product(operators, repeat=len(numbers)-1))
    for ops in operations:
        if apply_operands_left_to_right(numbers, ops, result)==result:
            return True
    return False

if __name__ == "__main__":
    equations = extract_data("Day7/input.txt")
    valids_sum_simple = sum([eq[0] for eq in equations if check_equation(eq, [mul,add])])
    print(valids_sum_simple)
    
    valids_sum_extended = sum([eq[0] for eq in equations if check_equation(eq, [mul,add, concat])])
    print(valids_sum_extended)