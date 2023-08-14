from resize import *
from split_data import *
from coco2yolo import *
from remove_classes import *
from augment_classes import *
import argparse

def main(images, width,height,annotations, remove, augment,image_type):
    # resize the images
    resize_images(images,width,height, 'data/resized_images')

    # remove the classes that are not in the classes list
    remove_classes_from_annotations(annotations,remove,'data/modified.json')

    # augment the classes
    generate_augmented_images('data/modified.json',augment,'data/resized_images','data/augmented_images')

    # convert the coco annotations to yolo format
    convert_coco_json('data',fixed_size=True,height=height,width=width)

    # split the data into train and test
    split_data('data/converted','data/split_data','data/resized_images',image_type=image_type)

   
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--images',default='data/images', help='path to the image directory')
    parser.add_argument('--width', default=640, help='width of the resized image')
    parser.add_argument('--height', default=480, help='height of the resized image')
    parser.add_argument('--annotations', default='data',help='path to the annotation directory')
    parser.add_argument('--image_type', default='JPG', help='image type, JPG or PNG')
    parser.add_argument('--remove', help='list of classes to remove, integers seperated by spaces', nargs='+',type=int)
    parser.add_argument('--augment', help='list of classes to augment, integers seperated by spaces', nargs='+',type=int)

    args = parser.parse_args()




    main(images=args.images, annotations=args.annotations, width=args.width, height=args.height,
         remove=args.remove, augment=args.augment, image_type=args.image_type)