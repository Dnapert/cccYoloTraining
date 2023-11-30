import json
import argparse
from utility_scripts.get_class_dict import get_class_dict

def auto_map(annotation_file,write:bool)->dict:
    '''
    given a coco json annotation file, remaps the class_id's to 0 indexed and fixes missing class_id's.
    returns a dictionary of class_id's and class_names
    outputs a data.yaml file for use with yolov5 and v8 with the class name list and number of classes
    '''
    with open(annotation_file, 'r') as f:
        data = json.load(f)
    
    class_dict = get_class_dict(annotation_file, False)

# Create a mapping from class_name to a new id
    class_to_new_id = {class_name: new_id for new_id, class_name in enumerate(class_dict.values())}
    #print(class_to_new_id)

# Update the 'id' in categories using the new mapping
    for category in data['categories']:
        category['id'] = class_to_new_id[category['name']]

# Update the 'category_id' in annotations using the new mapping
    for annotation in data['annotations']:
      
        original_class_name = class_dict[annotation['category_id']]
        annotation['category_id'] = class_to_new_id[original_class_name]    
    file_name = annotation_file.split('.', 1)[0] + '_remapped.json'
    if write:
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        class_dict=get_class_dict(file_name,True)
        
        
        with open(f"{file_name}.yaml","w") as f:
            f.write(f"nc: {len(class_dict)}\n")
            f.write("names: ")
            f.write(str(list(class_dict.values())))


    #print(class_to_new_id)
    return class_to_new_id   



argparse = argparse.ArgumentParser()
argparse.add_argument('-a','--annotation_file', type=str, default='annotations/modified/modified_annotations_updated.json')
argparse.add_argument('-w','--write', type=bool, default=True)
args = argparse.parse_args()
if __name__ == '__main__':
    auto_map(args.annotation_file,args.write)