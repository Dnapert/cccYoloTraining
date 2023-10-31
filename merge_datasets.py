import json
import argparse

def merge_datasets(base_dataset, new_dataset,output_dataset):
    '''
    needs to take two sets of annotations
    and merge them into one dataset
    datasets need to have classes matching

    '''    
    # load datasets
    with open(base_dataset, 'r') as f:
        base = json.load(f)
    with open(new_dataset, 'r') as f:
        new = json.load(f)
    holder = base.copy()
    # merge datasets    
    for k,v in new_dataset.items():
        holder[k].extend(v)
    with open(output_dataset, 'w') as f:
        json.dump(holder, f)

args = argparse.ArgumentParser()
args.add_argument('-b','--base_dataset', type=str, default='base_dataset.json')
args.add_argument('-n','--new_dataset', type=str, default='new_dataset.json')
args.add_argument('-o','--output_dataset', type=str, default='annotations/merged/merged_dataset.json')

if __name__ == '__main__':
    merge_datasets(args.base_dataset, args.new_dataset, args.output_dataset)