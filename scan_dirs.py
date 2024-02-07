import os
from auto_annotate import auto_annotate


def scan_dirs():
    '''
    Scan buckets for new images and call the auto_annotate function on them
    '''
    directories = ['/home/bucket-mounts/1','/home/bucket-mounts/2','/home/bucket-mounts/3']
    total_images = 0
    for directory in directories:
       subdirs =  os.listdir(directory)
       for dir in subdirs:
           images = os.listdir(f'{directory}/{dir}/images')
           total_images += len(images)
    print(f"Found {total_images} images")
           
      

scan_dirs()