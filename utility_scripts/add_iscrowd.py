import json
import argparse

def add_iscrowd(ann_file):
    with open(ann_file) as f:
        data = json.load(f)
    for i in range(len(data['annotations'])):
        data['annotations'][i]['iscrowd'] = 0
        data['annotations'][i]['segmentation'] = []
        data['annotations'][i]['area'] = data['annotations'][i]['bbox'][2] * data['annotations'][i]['bbox'][3]
    with open(ann_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Added 'iscrowd' to {ann_file}")
    
    
parser = argparse.ArgumentParser(description='Add iscrowd to annotations')
parser.add_argument('--ann', type=str, help='path to annotation file')

if __name__ == '__main__':
    args = parser.parse_args()                                                  
    add_iscrowd(args.ann)
