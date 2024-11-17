class FileNotFoundError(Exception):
    def __init__(self, message="Input file not found. Please provide a valid file path."):
        self.message = message
        super().__init__(self.message)

class InvalidInputDataError(Exception):
    def __init__(self, message="Invalid input data encountered during text processing."):
        self.message = message
        super().__init__(self.message)

class DiskSpaceFullError(Exception):
    def __init__(self, message="Insufficient disk space. Unable to write output file."):
        self.message = message
        super().__init__(self.message)


import os

def read_input_file(file_path):
    """Read the content of the input file."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        
        with open(file_path, 'r') as file:
            data = file.read()
        
        return data
    
    except FileNotFoundError as e:
        print(e)
        raise

def process_text_data(data):
    """Process the text data by performing various operations."""
    try:
        if not isinstance(data, str) or not data.strip():
            raise InvalidInputDataError("Input data must be a non-empty string.")
        
        word_count = len(data.split())
        char_freq = {char: data.count(char) for char in set(data)}
        
        # For simplicity, we'll assume generating a word cloud is a placeholder operation
        word_cloud = " ".join(data.split())  # Simplified word cloud
        
        return word_count, char_freq, word_cloud
    
    except InvalidInputDataError as e:
        print(e)
        raise

def write_output_file(output_path, results):
    """Write the processed results to the output file."""
    try:
        # Prepare the content to be written
        content = "Word Count: {}\n".format(results[0])
        content += "Character Frequencies: {}\n".format(results[1])
        content += "Word Cloud:\n{}\n".format(results[2])
        
        # Check if the content size exceeds 1MB
        if len(content.encode('utf-8')) > 1 * 1024 * 1024:  # Size in bytes
            raise DiskSpaceFullError("Output file size limit exceeded (1 MB).")
        
        # Write to the file
        with open(output_path, 'w') as file:
            file.write(content)
        
        print(f"Processed data successfully written to '{output_path}'")
    
    except DiskSpaceFullError as e:
        print(e)
        raise

def main():
    input_path = input("Enter the input file path: ")
    output_path = input("Enter the output file path: ")
    
    try:
        # Step 1: Read input data from a file
        data = read_input_file(input_path)
        
        # Step 2: Process the text data
        results = process_text_data(data)
        
        # Step 3: Store the processed results in an output file
        write_output_file(output_path, results)
    
    except (FileNotFoundError, InvalidInputDataError, DiskSpaceFullError) as e:
        print(f"Error: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
