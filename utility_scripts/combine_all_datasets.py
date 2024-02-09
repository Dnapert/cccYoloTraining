from combine_datasets import combine_datasets
import argparse
import os

def combine_all_annotations(directory,original_annotations):
    '''
    will combine all annotations in a directory into a single annotation file
    '''
    annotation_file = original_annotations
    if not os.path.exists(directory):
        print(f"{directory} does not exist")
        return
    for i,file in enumerate(os.listdir(directory)):
        if file != original_annotations:
            combine_datasets(f'{directory}/{file}',annotation_file,f'{directory}/combined_data')
            annotation_file = f'{directory}/combined_data.json'
            print(f"combininig {file}")

argparser = argparse.ArgumentParser()
argparser.add_argument('--dir', type=str, default='annotations')
argparser.add_argument('--ann', type=str, default='annotations/original_annotations.json')

if __name__ == "__main__":
    args = argparser.parse_args()
    combine_all_annotations(args.dir,args.ann)