
import json
import argparse
from utility_scripts.get_class_dict import get_class_dict
import json
import json



def combine_datasets(annotation_file1, annotation_file2):
    '''
    Reads two JSON annotation files and merges them with consistent class IDs and names.

    '''
    print("starting")
 
    with open(annotation_file1, 'r') as f:
        data1 = json.load(f)
    with open(annotation_file2, 'r') as f:
        data2 = json.load(f)

    class_dict1 = {category['id']: category['name'] for category in data1['categories']}
    class_dict2 = {category['id']: category['name'] for category in data2['categories']}

    all_classes = set(class_dict1.values()).union(set(class_dict2.values()))
 
    class_to_new_id = {name: i for i, name in enumerate(all_classes)}

    def update_annotations(annotations, class_dict):
        for annotation in annotations:
            class_name = class_dict.get(annotation['category_id'])
            if class_name in class_to_new_id:
                annotation['category_id'] = class_to_new_id[class_name]
        return annotations

    data1['annotations'] = update_annotations(data1['annotations'], class_dict1)
    data2['annotations'] = update_annotations(data2['annotations'], class_dict2)

    new_categories = [{"id": id, "name": name} for name, id in class_to_new_id.items()]

    combined_annotations = data1['annotations'] + data2['annotations']
    combined_images = data1['images'] + data2['images']

    combined_data = {
        'images': combined_images,
        'annotations': combined_annotations,
        'categories': new_categories
    }

    image_dict = {}

    # add file_name key to annotations, the cvat export didn't have them
    for i in combined_data['images']:
        # another issue with the cvat export, the file_name is the full path so we need to split it
        i['file_name'] = i['file_name'].split('/')[-1]
        if i['id'] not in image_dict:
            image_dict[i['id']] = i['file_name']
    for a in combined_data['annotations']:
        if not 'file_name' in a:
            a['file_name'] = image_dict[a['image_id']]


    file_name = annotation_file1.split('.', 1)[0] + '_combined.json'
    with open(file_name, 'w') as f:
        json.dump(combined_data, f, indent=4)

    print(f"Combined annotations saved to {file_name}")
    print(get_class_dict(file_name, False))


   

argparse = argparse.ArgumentParser()
argparse.add_argument('--annotation_file1', type=str, default='annotations/original_annotations.json')
argparse.add_argument('--annotation_file2', type=str, default='11-13.json')

args = argparse.parse_args()

if __name__ == '__main__':
    combine_datasets(args.annotation_file1,args.annotation_file2)