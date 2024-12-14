import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from utils import read_rows_from_file

def check_all_records(records: List[List[int]]) -> int:
  valid_results = [check_record_safe(record) for record in records]
  
  return sum(valid_results)

def check_all_modified_records(records: List[List[int]]) -> int:
  modified_records = [create_modifications(record) for record in records]
  valid_results = [any([check_record_safe(record) for record in modified]) for modified in modified_records]
  
  return sum(valid_results)

def check_record_safe(record: List[int]) -> bool:
  record_diffs: List[int] = [j-i for i, j in zip(record[:-1], record[1:])]
  same_sign: bool = all(t>0 for t in record_diffs) or all(t<0 for t in record_diffs)
  small_enough_differences: bool = all(abs(t)<=3 for t in record_diffs)
  
  return same_sign and small_enough_differences

def create_modifications(numbers: List[int]) -> List[List[int]]:
  result = []
  for i in range(len(numbers)):
    modified = numbers[:i] + numbers[i+1:]
    result.append(modified)
  result.append(numbers)
  return result

if __name__ == "__main__":
  records = read_rows_from_file("Day2/input.txt")  # Changed to relative path
  print(check_all_records(records))
  print(check_all_modified_records(records))