from resize import resize_images
from split_data import split_data
from coco2yolo import convert_coco_json
from remove_classes import remove_classes_from_annotations
from augment_classes import generate_augmented_images

import argparse

def export_training_dataset(images, width, height,annotations, remove, augment,image_type):
   
    
    # resize the images
    #resize_images(images,width, 'data/resized_images')
    
    
    # # remove the classes that are not in the classes list

    #remove_classes_from_annotations(annotations,remove,output_file='data/modified/modified_annotations.json')

    # # augment the classes
    generate_augmented_images('data/modified/modified_annotations.json',augment,'data/resized_images','data/augmented_images')
    
    # # count the number of images
    #count_images()
   
    # convert the coco annotations to yolo format
    convert_coco_json('data/modified',annotation_file='data/modified/modified_annotations_updated.json')

    # count the number of labels
    #count_label_files()

    # split the data into train and test
    #split_data('data/modified/converted/labels','data/split_data','data/resized_images',image_type=image_type)

   
    


parser = argparse.ArgumentParser()
parser.add_argument('--remove', help='list of classes to remove, integers seperated by spaces', nargs='+',type=int)
parser.add_argument('--augment', help='list of classes to augment, integers seperated by spaces', nargs='+',type=int)
parser.add_argument('--images',default='data/images', help='path to the image directory')
parser.add_argument('--width', default=640, help='width of the resized image')
parser.add_argument('--height', default=480, help='height of the resized image')
parser.add_argument('--annotations', default='data/annotation_coco_format.json',help='path to the annotation directory')
parser.add_argument('--image_type', default='jpg', help='image type, JPG or PNG')



if __name__ == '__main__':
    args = parser.parse_args()

    export_training_dataset(images=args.images, annotations=args.annotations, width=args.width, height=args.height,
         remove=args.remove, augment=args.augment, image_type=args.image_type)