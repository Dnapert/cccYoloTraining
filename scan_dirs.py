import os
from auto_annotate import auto_annotate


def scan_dirs():
    '''
    Scan buckets for new images and call the auto_annotate function on them
    '''
    directories = ['/home/bucket-mounts/1','/home/bucket-mounts/2','/home/bucket-mounts/3']

    for directory in directories:
       images =  os.listdir(f'{directory}/images')
       print(len(images))

scan_dirs()