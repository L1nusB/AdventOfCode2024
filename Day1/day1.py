def retrieve_list(url):
    try:
        import requests
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return []
    

def parse_columns(file_path: str):
    first_column = []
    second_column = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines
            if line.strip():
                # Split the line by whitespace and convert to integers
                nums = line.strip().split()
                first_column.append(int(nums[0]))
                second_column.append(int(nums[1]))
    
    return first_column, second_column

def count_occurrences(numbers: list) -> dict:
    from collections import Counter
    return dict(Counter(numbers))



def calculate_abs_diff(col1: list, col2: list):
    return [abs(a - b) for a, b in zip(col1, col2)]

def weighted_sum(numbers: list, occurrences: dict) -> int:
    return sum(num * occurrences.get(num, 0) for num in numbers)

if __name__ == "__main__":
    # list = retrieve_list("https://adventofcode.com/2024/day/1/input")
    col1, col2 = parse_columns("Day1/input.txt")
    col1.sort()  # Sort first column in ascending order
    col2.sort()  # Sort second column in ascending order
    diff = calculate_abs_diff(col1, col2)
    total_diff = sum(diff)
    print(total_diff)
    occurrences = count_occurrences(col2)
    weighted_sum = weighted_sum(col1, occurrences)
    print(weighted_sum)

