import os
from auto_annotate import auto_annotate


def scan_dirs():
    '''
    Scan buckets for new images and call the auto_annotate function on them
    '''
    directories = ['/home/bucket-mounts/1','/home/bucket-mounts/2','/home/bucket-mounts/3']

    for directory in directories:
        #auto_annotate('best.pt',directory,move=True,output_image_dir='/home/bucket-mounts/auto_annotations',output_annotation_dir='/home/bucket-mounts/annotations')
        print(f"Scanning {directory}")
        print(os.listdir(directory))