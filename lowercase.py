import json 
import argparse

def tolower(annotation_file):
    with open(annotation_file, 'r') as f:
        file = json.load(f)
    for i in range(len(file['annotations'])):
        # change all .JPG images to .jpg
        file['annotations'][i]['file_name'] = file['annotations'][i]['file_name'].split('.')[0] + '.jpg'
    with open(annotation_file, 'w') as f:
        json.dump(file, f, indent=4)
        
argsparser = argparse.ArgumentParser()
argsparser.add_argument('-a',help='path to annotation file')
args = argsparser.parse_args()

if __name__ == '__main__':
    tolower(args.a)
        