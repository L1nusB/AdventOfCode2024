import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import read_file_to_string, read_columns_from_file, read_rows_from_file
import re
from typing import List, Callable
import numpy as np

def count_list_matches(pattern: re.Pattern, input_list: List[str]) -> int:
    nested_matches = [pattern.findall(input_data) for input_data in input_list]
    matches = [item for sublist in nested_matches for item in sublist]
    return len(matches)

def extract_diagonals_from_rows(input_list: List[str]) -> List[str]:
    if not input_list:
        return []

    num_rows = len(input_list)
    num_cols = len(input_list[0])
    diagonals = []

    # Extract diagonals from top-left to bottom-right
    for d in range(num_rows + num_cols - 1):
        diagonal = []
        for row in range(max(0, d - num_cols + 1), min(num_rows, d + 1)):
            col = d - row
            diagonal.append(input_list[row][col])
        diagonals.append(''.join(diagonal))

    # Extract diagonals from top-right to bottom-left
    for d in range(num_rows + num_cols - 1):
        diagonal = []
        for row in range(max(0, d - num_cols + 1), min(num_rows, d + 1)):
            col = num_cols - 1 - (d - row)
            diagonal.append(input_list[row][col])
        diagonals.append(''.join(diagonal))

    return diagonals

def transform_rows_to_columns(input_list: List[str]) -> List[str]:
    if not input_list:
        return []

    num_rows = len(input_list)
    num_cols = len(input_list[0])
    columns = ['' for _ in range(num_cols)]

    for row in input_list:
        for col_index in range(num_cols):
            columns[col_index] += row[col_index]

    return columns

def split_into_chunks(input_list: List[str], chunk_size: int = 3) -> List[List[str]]:
    if not input_list:
        return []

    num_rows = len(input_list)
    num_cols = len(input_list[0])
    chunks = []

    for row_start in range(0, num_rows):
        for col_start in range(0, num_cols):
            chunk = []
            for row in range(row_start, min(row_start + chunk_size, num_rows)):
                chunk.append(list(input_list[row][col_start:col_start + chunk_size]))
            chunks.append(chunk)

    return chunks

def get_main_diagonals_from_chunk(chunk: List[str]) -> List[str]:
    chunk: np.ndarray = np.array(chunk)
    diagonals = [chunk.diagonal(), np.fliplr(chunk).diagonal()]
    diagonals = [''.join(diagonal) for diagonal in diagonals]
    return diagonals

def check_diagonal_match(pattern: re.Pattern, diagonals: List[str]) -> bool:
    for diagonal in diagonals:
        if not pattern.match(diagonal):
            return False
    return True

if __name__ == "__main__":
    xmas_pattern = re.compile(r"(?=(XMAS|SAMX))")
    mas_pattern = re.compile(r"(?=(MAS|SAM))")
    row_input = [row[0] for row in read_rows_from_file("Day4/input.txt", str)] # Returns a list of lists for separated entries (but input is not separated)
    col_input = transform_rows_to_columns(row_input)
    diag_input = extract_diagonals_from_rows(row_input)
    row_result = count_list_matches(xmas_pattern, row_input)
    col_result = count_list_matches(xmas_pattern, col_input)
    diag_result = count_list_matches(xmas_pattern, diag_input)
    total_matches = row_result + col_result + diag_result
    print(total_matches)
    
    row_input = [row[0] for row in read_rows_from_file("Day4/input.txt", str)] # Returns a list of lists for separated entries (but input is not separated)
    chunks = split_into_chunks(row_input)
    chunk_diagonals = [get_main_diagonals_from_chunk(chunk) for chunk in chunks]
    chunk_results = [check_diagonal_match(mas_pattern, diagonals) for diagonals in chunk_diagonals]
    print(sum(chunk_results))