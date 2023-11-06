import json
import argparse

def compare_class_dicts(annotaion_file1,annotation_file2):
    '''
    reads two json annotation files and compares the class_id's and class_names
    returns a dictionary of class_id's and class_names that are in both datasets
    '''
    print("starting")
    class_dict1 = {}
    class_dict2 = {}
    with open(annotaion_file1, 'r') as f:
        data1 = json.load(f)
    with open(annotation_file2, 'r') as f:
        data2 = json.load(f)
    for i in  data1['categories']:
        class_dict1[i['id']] = i['name']
    for i in  data2['categories']:
        class_dict2[i['id']] = i['name']
    #compare dicts
    common = {}
    for k,v in class_dict1.items():
        if k in class_dict2:
            common[k] = v
    print(common)
    return common

argparse = argparse.ArgumentParser()
argparse.add_argument('-a1','--annotation_file1', type=str, default='annotations/original_annotations.json')
argparse.add_argument('-a2','--annotation_file2', type=str, default='annotations/inatances_default.json')

args = argparse.parse_args()

if '__name__' == '__main__':
    compare_class_dicts(args.annotation_file1,args.annotation_file2)