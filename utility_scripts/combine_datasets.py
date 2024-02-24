
import json
import argparse


def combine_datasets(annotation_file1, annotation_file2,ann_name):
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
    
    # Remap the image ids to be unique across the two datasets
    maxn = len(data1['images'])
  
    data1_id_dict = {data1['images'][i]['id']: i +1 for i in range(maxn)}
    
    for i in range(len(data1['images'])):
        data1['images'][i]['id'] = data1_id_dict[data1['images'][i]['id']]
    
    for i in range(len(data1['annotations'])):
        data1['annotations'][i]['id'] = i
        data1['annotations'][i]['image_id'] = data1_id_dict[data1['annotations'][i]['image_id']]
             
    data2_id_dict = {data2['images'][i]['id']: 1 + i + maxn for i in range(len(data2['images']))}
    
    for i in range(len(data2['images'])):
        data2['images'][i]['id'] = data2_id_dict[data2['images'][i]['id']]
        
    for i in range(len(data2['annotations'])):
        data2['annotations'][i]['id'] = 1 + i + maxn
        data2['annotations'][i]['image_id'] = data2_id_dict[data2['annotations'][i]['image_id']] 
             

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

    if not ann_name:
        ann_name = annotation_file1.split('.', 1)[0] + '_combined'
    file_name = ann_name + '.json'
    with open(file_name, 'w') as f:
        json.dump(combined_data, f, indent=4)

    print(f"Combined annotations saved to {file_name}")

if __name__ == '__main__':
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument('--a1', type=str, default='annotations/original_annotations.json')
    argsParser.add_argument('--a2', type=str, default='11-13.json')
    argsParser.add_argument('--ann_name', type=str, default=None)
    args = argsParser.parse_args()
    combine_datasets(args.a1,args.a2,args.ann_name)