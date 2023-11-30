import os
from utility_scripts.utils import *
import shutil
from random import shuffle
import argparse
import matplotlib.pyplot as plt
import numpy as np

def split_data(file_dir,output_dir,image_dir,image_type):
    """
    Splits the data into train, test, and validation sets and moves the images to the proper data sets.
    provide the directory of the label files and the directory to output the data sets.
    """
    files = os.listdir(file_dir)
    print(len(files))
    shuffle(files)
    i, j, k = split_indices(files, train=0.8, test=0.1, validate=0.1)
    datasets = {'train': i, 'test': j, 'val': k}
    print('train: ',len(datasets['train']),'test: ',len(datasets['test']), 'val: ', len(datasets['val']))
    for dataset in datasets:
        make_dirs(f'{output_dir}/{dataset}')
        directory = f'{output_dir}/{dataset}/labels'
        for index in datasets[dataset]:
            image_name = files[index].split('.')[0] + '.' + image_type
            shutil.move(f'{image_dir}/{image_name}', f'{output_dir}/{dataset}/images')
            shutil.copy(f'{file_dir}/{files[index]}', directory)
    print('done')
    for keys in datasets:
        counts = output_num_labels(f'{output_dir}/{keys}/labels')
        bar_graph(counts, output_dir, keys)
        print(keys, counts)
   
def output_num_labels(file_dir):
    """
    outputs the number of labels per class in data set.
    """
    files = os.listdir(file_dir)
    label_dict = {}
    for file in files:
        
        with open(f'{file_dir}/{file}', 'r') as f:
            lines = [line.rstrip('\n').split() for line in f]
            for line in lines:
                if(len(line) == 0) or len(line[0]) > 2:
                    continue
                if int(line[0]) not in label_dict:
                    label_dict[int(line[0])] = 1
                else:
                    label_dict[int(line[0])] += 1
    return label_dict


def bar_graph(label_dict, file_path, dataset_name):
    
    labels, values = zip(*sorted(label_dict.items()))
    indexes = np.arange(len(labels))
    width = .8
    plt.bar(indexes, values, width)
    plt.xticks(indexes , labels)
    plt.xlabel('labels')
    plt.ylabel('number of labels')
    plt.title('number of labels per class')
    os.makedirs(f'{file_path}/figures', exist_ok=True)
    plt.savefig(f'{file_path}/figures/{dataset_name}.png')
    plt.close()
            
parser = argparse.ArgumentParser()
parser.add_argument('--file_dir', type=str, default='data/modified/converted/labels', help='directory of the label files')
parser.add_argument('--output_dir', type=str, default='data/v8exp7_data', help='directory of the output files')
parser.add_argument('--images', type=str, default='data/resized_images', help='directory of the images')
parser.add_argument('--image_type', type=str, default='JPG', help='type of image')


if __name__ == '__main__':
    args = parser.parse_args()
    split_data(args.file_dir, args.output_dir, args.images, args.image_type)

