import json
import os
import cv2
import albumentations as A
import copy
from datetime import datetime
import sys
import string
import random
import argparse
from utility_scripts import labels_per_class

def generate_augmented_images(annotations_file, image_folder, output_folder, category_augmentations):
    '''
    augments images in a coco dataset based on the category id and the number of augmentations specified
    will produce a new json file with the augmented images
    displays a bar graph and prints a count of the number of each class in the new annotations file
    '''
    with open(annotations_file, "r") as f:
        data = json.load(f)

    annotations = data["annotations"]
    updated_annotations = []
    annotations_length = len(annotations)
    print(f'Annotations Length: {annotations_length}')
    
    image_template = {
        "file_name": "",
        "height": 4104,
        "width": 7296,
        "id": 2020120011100728
    }
    for annotation in annotations:
        if annotation["category_id"] in category_augmentations:
            #print(annotation["category_id"])
            file_name = annotation["file_name"]
            image_path = os.path.join(image_folder, file_name)
            image = cv2.imread(image_path)

            if image is not None:
                file_name = f'{annotation["file_name"]}_augmented'
                for i in range(category_augmentations[annotation["category_id"]]):
                    # Moved the new_annotation creation here
                    new_annotation = copy.copy(annotation)

                    new_id = int(''.join(random.choices(string.digits, k=16)))
                    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    version = res
                    new_file_name = augment_and_save_image(image, file_name, output_folder, version)

                    new_annotation['file_name'] = new_file_name
                    new_annotation['image_id'] = new_id
                    annotations_length += 1
                    new_annotation['id'] = new_id
                    updated_annotations.append(new_annotation)
                    #print(f'Total new annotations: {len(updated_annotations)}')
                    new_image = copy.copy(image_template)
                    new_image['file_name'] = new_file_name
                    new_image['id'] = new_id
                    data["images"].append(new_image)
        else:
            updated_annotations.append(annotation)
                
    data["annotations"] += updated_annotations
    
    print(len(data["annotations"]))

    updated_annotations_file = os.path.splitext(annotations_file)[0] + "_updated.json"
   
    with open(updated_annotations_file, "w") as f:
        json.dump(data, f, indent=4)
        
def augment_and_save_image(image, file_name, output_folder, version):
     # Save the augmented image in the same folder as the original image
    new_file_name = f"{os.path.splitext(file_name)[0]}_{version}.jpg"
    output_path = os.path.join(output_folder, new_file_name)
    os.makedirs(output_folder, exist_ok=True)
    if os.path.exists(output_path):
        print('File already exists')
    else: 
        # Define your augmentation pipeline using Albumentations
        transform = A.Compose([
            # Add your desired transformations here
            #A.RandomBrightnessContrast(p=0.25),
            A.MedianBlur(p=0.25),
            #A.RandomFog(p=0.1),
            A.RandomSnow(p=0.2),
            A.RandomShadow(p=0.2),
            A.RandomRain(p=0.2),
        ])
        # Apply the transformations to the image
        augmented_image = transform(image=image)["image"]
        cv2.imwrite(output_path, augmented_image)
        #print(f"Augmented image saved as: {output_path}")
    return new_file_name

def parse_input(input_string):
    # Parses an input '0,9 2,15 9,12' as {0:9, 2:15, 9:12}
    category_augmentations = {}
    for part in input_string.split():
        parts = part.split(',')
        category_augmentations[int(parts[0])] = int(parts[1])
    return category_augmentations

parser = argparse.ArgumentParser(description='Remove classes from annotations file')
parser.add_argument('-a','--annotations_path', type=str,default='data/formatted_updated.json' ,help='Path to annotations file')
parser.add_argument('-i','--image_folder',type=str,default='data/resized_images', help='Path to image input folder for augmentation')
parser.add_argument('-o','--output_folder', type=str, default='data/resized_images',help='Path to ouput folder for augmented images')
parser.add_argument('-c','--augment_categories', type=str, help='Category followed by comma followed by amount separated by spaces: 1,50 5,10 9,100')

if __name__ == "__main__":
    args = parser.parse_args()
    category_augmentations = parse_input(args.augment_categories)
    print(category_augmentations)
    # python3 augment_classes.py --annotations_path "../cccBaltimoreTrashWheelML/boi_dataset/annotation_coco_format_3.json" --image_folder "../images" --output_folder "../images/augmented/v2/" --augment_categories "0,5 3,5 6,5 8,5"
    
    generate_augmented_images(annotations_file=args.annotations_path, image_folder=args.image_folder, output_folder=args.output_folder, category_augmentations=category_augmentations)

    ''' python augment_classes.py --annotations_path data/modified/formatted_updated.json --image_folder data/resized_images --output_folder data/resized_images --augment_categories '0,2 2,3 3,5 6,5'
'''