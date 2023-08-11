from resize import *
from split_data import *
from coco2yolo import *
from remove_classes import *
from augment_classes import *
import argparse

def main(images, annotations, output_dir, remove, augment):
    # resize the images
    resize_images()

    # remove the classes that are not in the classes list
    remove_classes_from_annotations()

    # augment the classes
    generate_augmented_images()

    # convert the coco annotations to yolo format
    convert_coco_json()

    # split the data into train and test
    split_data()

   

    parser = argparse.ArgumentParser()
    parser.add_argument('--images',default='images', help='path to the image directory')
    parser.add_argument('--annotations', help='path to the annotation directory')
    parser.add_argument('--output_dir', help='path to the output directory')
    parser.add_argument('--remove', help='list of classes to remove', nargs='+')
    parser.add_argument('--augment', help='list of classes to augment', nargs='+')

    args = parser.parse_args()

    if __name__ == '__main__':
        main(args.images, args.annotations, args.output_dir, args.remove, args.augment)