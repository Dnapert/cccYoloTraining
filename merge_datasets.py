import json
import argparse

def merge_datasets(base_dataset, new_dataset,output_dataset):
    '''
    take two sets of json annotations
    and merge them into one dataset.
    datasets need to have classes matching

    '''    
    image_id_dict={}
    # load datasets
    with open(base_dataset, 'r') as f:
        base = json.load(f)
    with open(new_dataset, 'r') as f:
        new = json.load(f)
    holder = base.copy()
    # merge datasets    
    annotations = new['annotations']
    images = new['images']
    for image in images:
        image_id_dict[image['id']] = image['file_name']
        holder['images'].append(image)
    for annotation in annotations:
        if not annotation['image_id']:
            annotation['image_id'] = image_id_dict[annotation['image_id']]
        holder['annotations'].append(annotation)
   
    with open(output_dataset, 'w') as f:
        json.dump(holder, f)

args = argparse.ArgumentParser()
args.add_argument('--base_dataset', type=str, default='data/modified/modified.json')
args.add_argument('--new_dataset', type=str, default='annotations/output_split.json')
args.add_argument('--output_dataset', type=str, default='annotations/merged_dataset.json')

input = args.parse_args()
if __name__ == '__main__':
    merge_datasets(input.base_dataset, input.new_dataset, input.output_dataset)