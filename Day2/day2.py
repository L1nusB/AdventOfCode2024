from typing import List

def create_list_diff(records: List[List[int]]) -> int:
  record_diffs: List[List[int]] = [[j-i for i, j in zip(record[:-1], record[1:])] for record in records]
  same_sign: List[bool] = [(all(t>0 for t in diffs) or all(t<0 for t in diffs)) for diffs in record_diffs]
  small_enough_differences: List[bool] = [any(abs(t)<=3 for t in diffs)) for diffs in record_diffs]

  valid : List[bool] = [sign and diff for sign, diff in zip(same_sign, small_enough_differences)]
  return sum(valid)

if name == "__main__":
  print("")
