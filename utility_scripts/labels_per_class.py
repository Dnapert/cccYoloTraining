import json 
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def labels_per_class(name,annotation_file): 
    '''
    Count the number of annotations per class in a COCO format annotation file
    '''
    with open(annotation_file, 'r') as json_file:
        data = json.load(json_file)
        label_dict = {}
        for i in range(0,len(data['annotations'])):
            label = data['annotations'][i]['category_id']
            if label not in label_dict:
                label_dict[label] = 1
            else:
                label_dict[label] += 1
        bar_graph(label_dict,name)
        label_dict = {k: v for k, v in sorted(label_dict.items(), key=lambda item: item[0])}

    print(f"labels per class: {label_dict}")
    return label_dict

def bar_graph(label_dict,name):
    
    labels, values = zip(*sorted(label_dict.items()))
    indexes = np.arange(len(labels))
    width = .8
    plt.bar(indexes, values, width)
    plt.xticks(indexes , labels)
    plt.xlabel('labels')
    plt.ylabel('occurances of labels')
    if not os.path.exists(name):
        os.makedirs(name,exist_ok=True)
    plt.savefig(f"{name}/labels.png")

parser = argparse.ArgumentParser()
parser.add_argument('--annotations', default='../data/modified/modified.json', help='path to the annotation directory')

if __name__ == '__main__':

    args = parser.parse_args()
    labels_per_class(args.annotations)
