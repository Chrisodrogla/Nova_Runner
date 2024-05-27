import json
import os
import sys

def split_json_file(input_file, chunk_size):
    with open(input_file, 'r') as f:
        data = json.load(f)

    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    output_files = []
    for i, chunk in enumerate(chunks):
        output_file = f"chunk_{i}.json"
        with open(output_file, 'w') as f:
            json.dump(chunk, f)
        output_files.append(output_file)
    
    return output_files

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_json.py <input_file> <chunk_size>")
        sys.exit(1)
    input_file = sys.argv[1]
    chunk_size = int(sys.argv[2])
    split_json_file(input_file, chunk_size)
