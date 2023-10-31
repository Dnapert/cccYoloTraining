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

image_dict = {}

def generate_nighvision_images(annotations_file, image_folder, output_folder):
    '''
    Creates night vision style images from provided images and annotations, doubling dataset size
    '''
    global image_dict
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
        
            file_name = annotation["file_name"]
            if file_name in image_dict:
                temp = copy.copy(annotation)
                temp["file_name"] = image_dict[file_name]
                updated_annotations.append(temp)
                continue
            else:
                image_path = os.path.join(image_folder, file_name)
                image = cv2.imread(image_path)

                if image is not None:
                    tmp_file_name = f'{annotation["file_name"]}_augmented'
                    
                        # Moved the new_annotation creation here
                    new_annotation = copy.copy(annotation)

                    new_id = int(''.join(random.choices(string.digits, k=16)))
                    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    version = res
                    new_file_name = augment_and_save_image(image, tmp_file_name, output_folder, version)
                    new_annotation['file_name'] = new_file_name
                    new_annotation['image_id'] = new_id
                    annotations_length += 1
                    new_annotation['id'] = new_id
                    updated_annotations.append(new_annotation)
                    print(f'Total new annotations: {len(updated_annotations)}')
                    new_image = copy.copy(image_template)
                    new_image['file_name'] = new_file_name
                    new_image['id'] = new_id
                    data["images"].append(new_image)
                    image_dict[file_name] = new_file_name
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
        A.ToGray(p=1),  # Convert image to grayscale
        A.RandomBrightnessContrast(brightness_limit=(.2,.2), contrast_limit=(.7,.7), p=1),  # Adjust brightness and contrast
        #A.GaussNoise(var_limit=(5.0, 5.0), p=0.5),  # Add Gaussian noise
        ])

        # Apply the transformations to the image
        augmented_image = transform(image=image)["image"]
        cv2.imwrite(output_path, augmented_image)
        #print(f"Augmented image saved as: {output_path}")
    return new_file_name



parser = argparse.ArgumentParser(description='Augent photos to mimic night vision')
parser.add_argument('--annotations_path', type=str, default='data/modified/formatted.json',help='Path to annotations file')
parser.add_argument('--image_folder',type=str,default='data/resized_images', help='Path to image input folder for augmentation')
parser.add_argument('--output_folder', type=str,default='data/resized_images',  help='Path to ouput folder for augmented images')

if __name__ == "__main__":
    args = parser.parse_args()
    # python3 augment_classes.py --annotations_path "data/modified/formatted_updated.json" --image_folder "data/resized_images" --output_folder "data/resized_images" 
    
    generate_nighvision_images(annotations_file=args.annotations_path, image_folder=args.image_folder, output_folder=args.output_folder)

    ''' python night_vision.py --annotations_path data/modified/formatted.json --image_fol
der data/resized_images --output_folder data/resized_images 
'''