import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import read_file_to_string
import re
from typing import List, Callable
from operator import mul, sub, add


def extract_operations(input: str, pattern: re.Pattern) -> List[str]:
    return pattern.findall(input)

def extract_operations_conditional(input: str, pattern: re.Pattern, enable: re.Pattern, disable: re.Pattern) -> List[str]:
    full_pattern = re.compile(f"{enable.pattern}|{disable.pattern}|{pattern.pattern}")
    enable = enable.pattern.replace("\\", "")
    disable = disable.pattern.replace("\\", "")
    matches = extract_operations(input, full_pattern)
    operations = []
    allow_operation = True
    for match in matches:
        if match == enable:
            allow_operation = True
        elif match == disable:
            allow_operation = False
        else:
            if allow_operation:
                operations.append(match)
    return operations
    

def apply_operation(mul_operations: List[str], func: Callable[[int, int],int]) -> int:
    result = 0
    for operation in mul_operations:
        numbers = re.findall(r"\d+", operation)
        result += func(int(numbers[0]), int(numbers[1]))
    return result

if __name__ == "__main__":
    multiply_pattern = re.compile(r"mul\(\d+,\d+\)")
    
    input = read_file_to_string("Day3/input.txt")
    mul_operations = extract_operations(input, multiply_pattern)
    result = apply_operation(mul_operations, mul)
    print(result)
    filtered_mul_operations = extract_operations_conditional(input, multiply_pattern, re.compile(r"do\(\)"), re.compile(r"don't\(\)"))
    result = apply_operation(filtered_mul_operations, mul)
    print(result)