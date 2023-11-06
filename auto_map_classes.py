import json
import argparse
from get_class_dict import get_class_dict

def auto_map(annotation_file):
    '''
    given a coco json annotation file, remaps the class_id's to 0 indexed and fixes missing class_id's.
    outputs a data.yaml file for use with yolov5 and v8 with the class name list and number of classes
    '''
    with open(annotation_file, 'r') as f:
        data = json.load(f)
    
    class_dict = get_class_dict(annotation_file,False)
    new_class_dict = {i: class_name for i, class_name in enumerate(class_dict.values())}
    #map keys in class_dict to new keys in new_class_dict
    for i in data['categories']:
        i['id'] = list(new_class_dict.keys())[list(new_class_dict.values()).index(i['name'])]
    for i in data['annotations']:
        i['category_id'] = list(new_class_dict.keys())[list(new_class_dict.values()).index(class_dict[i['category_id']])]
    with open(f"{annotation_file}_remapped", 'w') as f:
        json.dump(data, f, indent=4)
    get_class_dict(f"{annotation_file}_remapped",True)
    yaml_name = annotation_file.split('.',1)[0] + '.yaml'
    with open(yaml_name,"w") as f:
        f.write(f"nc: {len(new_class_dict)}\n")
        f.write("names: ")
        f.write(str(list(new_class_dict.values())))

    print(new_class_dict)
        



argparse = argparse.ArgumentParser()
argparse.add_argument('-a','--annotation_file', type=str, default='annotations/modified/modified_annotations_updated.json')
args = argparse.parse_args()
if __name__ == '__main__':
    auto_map(args.annotation_file)