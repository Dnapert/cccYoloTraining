import json
import os
import cv2
import albumentations as A
import copy
from datetime import datetime
import sys

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
            A.RandomBrightnessContrast(p=0.25),
            A.MedianBlur(p=0.25),
            A.RandomFog(p=0.1),
            A.RandomSnow(p=0.1),
            A.RandomShadow(p=0.1),
            A.RandomRain(p=0.1),
        ])
        # Apply the transformations to the image
        augmented_image = transform(image=image)["image"]
        cv2.imwrite(output_path, augmented_image)
        print(f"Augmented image saved as: {output_path}")
    return new_file_name

def generate_augmented_images(json_file, augment_ids, image_folder, output_folder):
    with open(json_file, "r") as f:
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
        if annotation["category_id"] in augment_ids:
            new_annotation = copy.copy(annotation);
            file_name = new_annotation["file_name"]
            image_path = os.path.join(image_folder, file_name)
            image = cv2.imread(image_path)

            if image is not None:
                file_name = f'{new_annotation["file_name"]}_augmented'
                for i in range(2):
                    new_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    new_file_name = augment_and_save_image(image, file_name, output_folder, i)
                    
                    new_annotation['file_name'] = new_file_name
                    new_annotation['image_id'] = new_id
                    annotations_length += 1
                    new_annotation['id'] = annotations_length
                    updated_annotations.append(new_annotation)
                    
                    new_image = copy.copy(image_template)
                    new_image['file_name'] = new_file_name
                    new_image['id'] = new_id
                    data["images"].append(new_image)
                    
                    print(f'Successfully inserted {new_annotation} ::: {new_image}')
            
    data["annotations"] += updated_annotations

    updated_json_file = os.path.splitext(json_file)[0] + "_updated.json"
    with open(updated_json_file, "w") as f:
        json.dump(data, f, indent=4)
                    
if __name__ == "__main__":
    json_file = sys.argv[1] # "./boi_dataset/annotation_coco_format_3.json"  (annotation path)
    category_ids_to_augment = [0, 3, 6, 8]
    image_folder = sys.argv[2] # "../images" (images to augment path)
    output_folder = sys.argv[3] # "../images/augmented/v2/" (augmented images path)
    
    # python3 augment_classes.py "./boi_dataset/annotation_coco_format_3.json" "../images" "../images/augmented/v2/"
    
    generate_augmented_images(json_file, category_ids_to_augment, image_folder, output_folder)
