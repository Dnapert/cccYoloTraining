import json
import sys
def format_json(file,output):
    '''Formats a json file to be more readable'''
    with open(file, "r") as f:
        data = json.load(f)
    with open(output, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    file = sys.argv[1]
    output = sys.argv[2]
    format_json(file,output)