from typing import List

def read_columns_from_file(filename: str, datatype: type = int) -> List[List[int]]:
    """
    Reads a text file where each row has columns separated by whitespace
    and returns a list of columns. Values are converted to integers.
    
    Args:
        filename (str): Path to the text file
        
    Returns:
        List[List[int]]: List where each element is a list containing all integer values
        for that column position. Column lists may have different lengths.
    """
    rows: List[List[int]] = []
    max_columns: int = 0
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split the line and convert to integers
                values: List[int] = [datatype(val) for val in line.split() if val]
                max_columns = max(max_columns, len(values))
                rows.append(values)
        
        # Initialize columns
        columns: List[List[int]] = [[] for _ in range(max_columns)]
        
        # Fill columns only with existing values
        for row in rows:
            for col_idx, value in enumerate(row):
                columns[col_idx].append(value)
                    
        return columns
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except ValueError as e:
        print(f"Error: Invalid numeric value in file: {str(e)}")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []
    
def read_rows_from_file(filename: str, datatype: type = int) -> List[List[int]]:
    """
    Reads a text file where each row has integers separated by whitespace
    and returns a list of rows.
    
    Args:
        filename (str): Path to the text file
        
    Returns:
        List[List[int]]: List where each element is a list containing the integers from that row
    """
    try:
        with open(filename, 'r') as file:
            return [[datatype(val) for val in line.split() if val] for line in file]
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except ValueError as e:
        print(f"Error: Invalid numeric value in file: {str(e)}")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []
    
def read_file_to_string(filename: str) -> str:
    """
    Reads a text file and returns its entire content as a string.
    
    Args:
        filename (str): Path to the text file
        
    Returns:
        str: The entire content of the file as a string
    """
    try:
        with open(filename, 'r') as file:
            return file.read()
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return ""

if __name__ == "__main__":
    dat = read_rows_from_file("Day2/input.txt")
    print("Wait")