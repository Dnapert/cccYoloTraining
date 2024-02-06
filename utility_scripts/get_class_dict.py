import json
import argparse
def get_class_dict(annotation_file,write:bool)->dict:
    '''
    reads a json annotation file and returns a dictionary of class_id's and class_names
    optionally writes the dictionary to a json file with the name <annotation_file>.json
    '''
    class_dict = {}
    with open(annotation_file, 'r') as f:
        data = json.load(f)
    for i in  data['categories']:
        class_dict[i['id']] = i['name']
    #print(class_dict)
    #split file name and extension
    if write:
        annotation_file = annotation_file.split('/',1)[-1]
        annotation_file = annotation_file.split('.',1)[0]
        annotation_file +='_dict.json'
        with open(annotation_file, 'w') as f:
            json.dump(class_dict, f, indent=4)
        print(f'Class dict written to {annotation_file}')
    return class_dict

parser = argparse.ArgumentParser()

parser.add_argument('-a','--annotation_file', type=str, default='annotations/.json')
parser.add_argument('-w','--write', type=bool, default=True)
args = parser.parse_args()

if __name__ == '__main__':
    get_class_dict(args.annotation_file,args.write)