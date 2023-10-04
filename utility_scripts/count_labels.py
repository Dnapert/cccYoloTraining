import os
import sys

def count_label_files():
    # Count number of label files in folder
    label_dir = 'data/modified/converted/labels'
    label_files = os.listdir(label_dir)
    print(f'Number of label files: {len(label_files)}')
    return len(label_files)

count_label_files()