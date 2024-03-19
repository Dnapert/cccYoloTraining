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

def augment_for_multiple_classes(args):
    if not os.path.isfile(args.annotations_file):
        raise ValueError(f"The annotations_file does not exist: {args.annotations_file}")
    if not os.path.exists(args.image_dir):
        raise ValueError(f"The image_dir does not exist: {args.image_dir}")
    if not os.path.exists(args.augmented_image_dir):
        os.makedirs(args.augmented_image_dir)
    updated_annotations_dir = os.path.dirname(args.updated_annotations_file)
    if not os.path.exists(updated_annotations_dir):
        os.makedirs(updated_annotations_dir)

    with open(args.annotations_file, 'r') as f:
        data = json.load(f)

    classes_to_augment = set(args.classes_to_augment)
    categories_ids_to_augment = {category['id'] for category in data['categories'] if category['name'] in classes_to_augment}
    if not categories_ids_to_augment:
        raise ValueError(f"No categories found for the specified classes to augment: {classes_to_augment}")
    print(f'Augmenting: {classes_to_augment}, Category IDs: {categories_ids_to_augment}')
    
    augmentation = Compose([
        RandomBrightnessContrast(p=1),
        HueSaturationValue(hue_shift_limit=10, sat_shift_limit=15, val_shift_limit=10, p=1)
    ])

    new_image_id = max(image['id'] for image in data['images']) + 1
    new_annotation_id = max(ann['id'] for ann in data['annotations']) + 1
    
    augmented_images_counter = 0
    for image_info in data['images']:
        if image_info['file_name'].startswith('aug_'):
            continue
        
        annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_info['id'] and ann['category_id'] in categories_ids_to_augment]
        if not annotations:
            continue
        print(f'Found an image: {image_info["file_name"]}')
        image_path = os.path.join(args.image_dir, image_info['file_name'])
        if not os.path.exists(image_path):
            print(f'Image path {image_path} does not exist')
            continue

        image = load_image(image_path)
        augmented = augmentation(image=image)
        augmented_image = augmented['image']

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        augmented_image_name = f"aug_{image_info['file_name'].replace('.jpg', '')}_{timestamp}.jpg"
        augmented_image_path = os.path.join(args.augmented_image_dir, augmented_image_name)
        save_image(augmented_image, augmented_image_path)

        augmented_image_info = dict(image_info)
        augmented_image_info['id'] = new_image_id
        augmented_image_info['file_name'] = augmented_image_name
        data['images'].append(augmented_image_info)

        for ann in annotations:
            new_ann = dict(ann)
            new_ann['id'] = new_annotation_id
            new_ann['image_id'] = new_image_id
            data['annotations'].append(new_ann)
            new_annotation_id += 1

        new_image_id += 1
        augmented_images_counter += 1
        print(f"Augmented image and annotations added for {augmented_image_name}")

    if augmented_images_counter > 0:
        with open(args.updated_annotations_file, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Updated annotation file has been saved. Introduced {augmented_images_counter} augmented images.")
    else:
        print('No images augmented, unable to find any classes')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment images and update annotations for specific classes.")
    parser.add_argument("--annotations_file", required=True, help="Path to the COCO annotations JSON file.")
    parser.add_argument("--image_dir", required=True, help="Directory containing the original images.")
    parser.add_argument("--augmented_image_dir", required=True, help="Directory to save augmented images.")
    parser.add_argument("--updated_annotations_file", required=True, help="File path to save the updated annotations JSON.")
    parser.add_argument("--classes_to_augment", nargs='+', required=True, help="List of class names to augment.")

    args = parser.parse_args()
    augment_for_multiple_classes(args)

#Use Case:
#python augment_classes_v2.py --annotations_file /home/trashwheel-annotations/all_annotations.json --image_dir /home/trashwheel/annotated_images --augmented_image_dir /home/trashwheel/annotated_images --updated_annotations_file /home/trashwheel-annotations/all_annotations.json --classes_to_augment sports_ball plastic_cup small_plastic_bottle plastic_container plastic_bag plastic_wrapper