import argparse
import json
import os
import cv2
from albumentations import Compose, RandomBrightnessContrast, HueSaturationValue
import datetime

def load_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def save_image(image, save_path):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path, image)

def augment_and_update_annotations(args):
    # Check if the annotations_file path is a directory or does not exist
    if os.path.isdir(args.annotations_file):
        raise ValueError(f"The specified annotations_file is a directory, not a file: {args.annotations_file}")
    if not os.path.isfile(args.annotations_file):
        raise ValueError(f"The specified annotations_file does not exist: {args.annotations_file}")

    # Check if the updated_annotations_file path is valid
    if os.path.isdir(args.updated_annotations_file):
        raise ValueError(f"The specified updated_annotations_file is a directory, not a file: {args.updated_annotations_file}")
        
    # Optionally, check if the directory of the updated_annotations_file exists
    # This is helpful if you want to ensure the directory exists before attempting to write
    updated_annotations_dir = os.path.dirname(args.updated_annotations_file)
    if not os.path.exists(updated_annotations_dir):
        raise ValueError(f"The directory of the specified updated_annotations_file does not exist: {updated_annotations_dir}")
    
    with open(args.annotations_file, 'r') as f:
        data = json.load(f)

    categories_to_omit = set(args.classes_to_omit)
    category_ids_to_omit = {category['id'] for category in data['categories'] if category['name'] in categories_to_omit}
    omit_background = "background" in categories_to_omit

    augmentation = Compose([
        RandomBrightnessContrast(p=1),
        HueSaturationValue(hue_shift_limit=10, sat_shift_limit=15, val_shift_limit=10, p=1) 
    ])

    # Assuming we start new IDs from max existing + 1
    new_image_id = max(image['id'] for image in data['images']) + 1
    new_annotation_id = max(ann['id'] for ann in data['annotations']) + 1

    new_images_counter = 0
    for image_info in data['images']:
        if image_info['file_name'].startswith('aug_'):
            continue
        
        annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_info['id']]
        
        # Skip images if they are to be treated as background or do not meet the required conditions
        if omit_background and not annotations or any(ann['category_id'] in category_ids_to_omit for ann in annotations):
            continue

        if not any(ann['category_id'] in category_ids_to_omit for ann in annotations):
            image_path = os.path.join(args.image_dir, image_info['file_name'])
            if not os.path.exists(image_path):
                continue

            image = load_image(image_path)
            augmented = augmentation(image=image)
            augmented_image = augmented['image']

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            augmented_image_name = f"aug_{image_info['file_name'].replace('.jpg', '')}_{timestamp}.jpg"
            augmented_image_path = os.path.join(args.augmented_image_dir, augmented_image_name)
            save_image(augmented_image, augmented_image_path)

            # Add augmented image to data['images']
            augmented_image_info = dict(image_info)  # Create a copy to avoid modifying the original
            augmented_image_info['id'] = new_image_id
            augmented_image_info['file_name'] = augmented_image_name
            data['images'].append(augmented_image_info)

            # Copy annotations to refer to the new image ID
            for ann in annotations:
                new_ann = dict(ann)  # Create a copy to avoid modifying the original
                new_ann['id'] = new_annotation_id
                new_ann['image_id'] = new_image_id
                new_ann['file_name'] = augmented_image_name
                data['annotations'].append(new_ann)

                new_annotation_id += 1

            new_image_id += 1
            new_images_counter += 1

            print(f"Augmented image and annotations added for {augmented_image_name}")

    # Save updated annotations to a new file
    with open(args.updated_annotations_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Updated annotation file has been saved. Introduced {new_images_counter} images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment images, update annotations excluding specified classes, and append new data.")
    parser.add_argument("--annotations_file", type=str, required=True, help="Path to the COCO annotations JSON file.")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing the original images.")
    parser.add_argument("--augmented_image_dir", type=str, required=True, help="Directory to save augmented images.")
    parser.add_argument("--updated_annotations_file", type=str, required=True, help="File path to save the updated annotations JSON.")
    parser.add_argument("--classes_to_omit", nargs='+', required=True, help="List of class names to omit during augmentation.")

    args = parser.parse_args()
    augment_and_update_annotations(args)