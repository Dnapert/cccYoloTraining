import cv2

import os
from pathlib import Path
import argparse
import sys


def resize_images(image_dir, width, height,output_dir):
        fn = Path(output_dir) 
        fn.mkdir(parents=True, exist_ok=True)
        images = os.listdir(image_dir)
        i = 0
        print('resizing images:')
        for filename in images:
            sys.stdout.write(f'\r {i}/{len(images)}')
            i += 1
            image = cv2.imread(os.path.join(image_dir,filename))
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(output_dir,filename), image)
        print('\nDone!')
            




parser = argparse.ArgumentParser(description='Resize images')
parser.add_argument('--image_dir', type=str, default='images', help='path to the images')
parser.add_argument('--output_dir', type=str, default='resized_images_2', help='path to the resized images')
parser.add_argument('--width', type=int, default=640, help='width of the resized images')
parser.add_argument('--height', type=int, default=480, help='height of the resized images')
args = parser.parse_args()

image_dir = args.image_dir
output_dir = args.output_dir
width = args.width
height = args.height

resize_images(image_dir, width, height,output_dir)