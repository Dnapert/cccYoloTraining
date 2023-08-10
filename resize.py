import cv2

import os
from utils import *


def resize_images(image_dir, width, height,output_dir):
        fn = Path(output_dir) 
        fn.mkdir(parents=True, exist_ok=True)
        
        for filename in os.listdir(image_dir):
            
            image = cv2.imread(os.path.join(image_dir,filename))
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(output_dir,filename), image)
           


image_dir = 'images'
output_dir = 'resized_images'
width = 640
height = 480

resize_images(image_dir, width, height,output_dir)