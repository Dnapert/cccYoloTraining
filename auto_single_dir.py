import os
import json
from ultralytics import YOLO
import datetime
import argparse

# Define custom categories
custom_categories = [
    {"id": 1, "name": "plastic_bag"},
    {"id": 2, "name": "plastic_bottle"},
    {"id": 3, "name": "plastic_cap"},
    {"id": 4, "name": "plastic_container"},
    {"id": 5, "name": "plastic_wrapper"},
    {"id": 6, "name": "plastic_other"},
    {"id": 7, "name": "foam_container"},
    {"id": 8, "name": "foam_other"},
    {"id": 9, "name": "aluminum_can"},
    {"id": 10, "name": "amazon_envelope"},
    {"id": 11, "name": "plastic_cup"},
    {"id": 12, "name": "small_plastic_bottle"},
    {"id": 13, "name": "glass_bottle"},
    {"id": 14, "name": "sports_ball"},
]

def auto_annotate(model, image_dir, batch_size=12, move=False, output_dir="/home/trashwheel/auto_annotations"):
    model = YOLO(model)
    
    if not os.path.exists(output_dir):
        print(f"ERROR: {output_dir} not found")
        return
    if not os.path.exists(image_dir):
        print(f"ERROR: {image_dir} not found")
        return
    images = os.listdir(image_dir)
    if len(images) == 0:
        print(f"ERROR: No images found in {image_dir}")
        return
    image_list = [f'{image_dir}/{image}' for image in images if image.split('.')[-1] in ['jpg','jpeg','png']]
    if len(image_list) == 0:
        print(f"ERROR: No valid images found in {image_dir}")
        return
    
    annotation_name = datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    if move:
        if not os.path.exists(f"{output_dir}/{annotation_name}"):
            os.makedirs(f"{output_dir}/{annotation_name}")
    
    print(f"Found: {len(image_list)} images")
    
    # Assign custom categories to data dictionary
    data = {'categories': custom_categories, 'images': [], 'annotations': []}

    # Mapping from model names to custom category IDs
    model_names_to_custom_ids = {name: i for i, cat in enumerate(custom_categories) for name in model.names if name == cat['name']}
    
    for i in range(0, len(image_list), batch_size):
        batch = image_list[i:i+batch_size]
        results = model(batch, verbose=False)
        
        for j, item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xyxy
            height, width = item.orig_shape
            file_name = os.path.basename(batch[j])
            data['images'].append({"file_name": file_name, "id": image_id, "width": width, "height": height})
            
            for box, cls in zip(boxes, classes):
                # Use mapping to get correct category ID
                category_id = model_names_to_custom_ids.get(cls, -1)  # Default to -1 if class name not found
                if category_id == -1:
                    print(f'Invalid category ID {cls}')
                    continue  # Skip annotation if class name not found in mapping
                x1, y1, x2, y2 = [float(b) for b in box]
                tl_x = x1
                tl_y = y1
                w = x2 - x1
                h = y2 - y1
                data['annotations'].append({
                    "id": len(data['annotations']),
                    "image_id": image_id,
                    "category_id": category_id,
                    "bbox": [tl_x, tl_y, w, h],
                    "area": w * h,
                    "segmentation": [],
                    "iscrowd": 0,
                })
                
    print(f"Annotations written to {os.path.join(output_annotation_dir, annotation_name + '.json')}")
    print(f"Annotated {len(data['images'])} images")
    with open(os.path.join(output_annotation_dir, annotation_name + '.json'), 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto Annotate')
    parser.add_argument('--model', type=str, help='path to model')
    parser.add_argument('--dir', type=str, help='path to image directory')
    parser.add_argument('--batch_size', type=int, default=12, help='batch size')
    parser.add_argument('--move', type=bool, default=False, help='move images to attached bucket')
    parser.add_argument('--output_dir', type=str, default='/home/trashwheel/auto_annotations', help='path to output image directory')

    args = parser.parse_args()
    auto_annotate(args.model, args.dir, args.batch_size, args.move, args.output_dir)
