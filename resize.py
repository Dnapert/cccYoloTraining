import cv2

import os
from pathlib import Path
import argparse
import sys


def resize_images(image_dir, target_width,output_dir):
        fn = Path(output_dir) 
        fn.mkdir(parents=True, exist_ok=True)
        images = os.listdir(image_dir)
        i = 0
        print('resizing images:')
        for filename in images:
            sys.stdout.write(f'\r {i}/{len(images)}')
            i += 1
            image = cv2.imread(os.path.join(image_dir,filename))
            height, width, _ = image.shape
            aspect_ratio = width / height
    
            # Calculate the new height based on the target width and aspect ratio
            target_height = int(target_width / aspect_ratio)
    
            image = cv2.resize(image, (int(target_width),int(target_height)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(output_dir,filename), image)
        print('\nDone!')
            




parser = argparse.ArgumentParser(description='Resize images')
parser.add_argument('--image_dir', type=str, default='images', help='path to the images')
parser.add_argument('--output_dir', type=str, default='resized_images_2', help='path to the resized images')
parser.add_argument('--target_width', type=int, default=640, help='width of the resized images')


if __name__ == '__main__':
    args = parser.parse_args()
   
    resize_images(args.image_dir, args.target_width,args.output_dir)