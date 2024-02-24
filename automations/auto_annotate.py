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

def auto_annotate(model,batch_size=12,move=False,output_dir="/home/trashwheel/auto_annotations"):
    '''
    Automatically annotate images in all trashwheel bucket folders, saves coco json annotation file with date stamp and moves images to auto annotations folder in bucket.

    '''
    date = datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    model = YOLO(model)
    buckets = [f'/home/trashwheel/{i}' for i in range(1,4)]
    
    for i, bucket in enumerate(buckets):
        subdirs = os.listdir(bucket)
        images = []
        for date_captured in subdirs:
            images_folder = os.listdir(f"{bucket}/{date_captured}/images")
            for image in images_folder:
                if image.split('.')[-1] in ['jpg','jpeg','png']:
                    images.append(f'{bucket}/{date_captured}/images/{image}')
        print(f"Found: {len(images)} images for wheel id: {i + 1}")
        
        output_annotation_file = f"{output_dir}/{i + 1}/{date}.json"
        output_images_dir = f"{output_dir}/{i + 1}/{date}"

        os.makedirs(output_images_dir, exist_ok=True) # Create output directory if it doesn't exist
        
        data = {'categories':[],'images':[],'annotations':[]}
        names = model.names
        
        data['categories'] = [{"id":k,"name":v,"supercategory":"object"} for k,v  in names.items()]
        
        # Assign custom categories to data dictionary
        data = {'categories': custom_categories, 'images': [], 'annotations': []}
        
        name_to_id = {category['name']: category['id'] for category in custom_categories}
        model_id_to_custom_category_id = {i: name_to_id.get(name, -1) for i, name in model.names.items()}

        for j in range(0, len(images), batch_size):
            batch = images[j:j+batch_size]
            results = model(batch, verbose=False)
            
            for k, item in enumerate(results):
                image_id = len(data['images'])
                res = item.boxes.cpu().numpy()
                classes = res.cls
                boxes = res.xyxy
                height, width = item.orig_shape
                file_name = os.path.basename(batch[k])
                data['images'].append({"file_name": file_name, "id": image_id, "width": width, "height": height})
                
                for box, cls in zip(boxes, classes):
                    # Use mapping to get correct category ID based on model prediction name
                    category_id = model_id_to_custom_category_id.get(int(cls), -1)
                    if category_id == -1:
                        print('Unable to fetch category')
                        continue  # Skip annotation if class name not found in mapping
                    
                    x1, y1, x2, y2 = [float(b) for b in box]
                    w = x2 - x1
                    h = y2 - y1
                    data['annotations'].append({
                        "id": len(data['annotations']),
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": [x1, y1, w, h],
                        "area": w * h,
                        "segmentation": [],
                        "iscrowd": 0,
                    })
            if move:
                for image in batch:
                    try:
                        os.system(f"mv {image} {output_images_dir}")
                    except Exception as e:
                        print(f"Failed to move {image} to {output_images_dir}")
                        print(e)    
                        continue
                                
        print(f"Annotated {len(data['images'])} images")
            
        try:
            with open(f'{output_annotation_file}', 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Annotations written to {output_annotation_file}")
        except Exception as e:
            print(f"Failed to write annotations to {output_annotation_file} with error {e}")
            continue

parser = argparse.ArgumentParser(description='Auto Annotate')
parser.add_argument('--model', type=str, default='best.pt', help='path to model')
parser.add_argument('--batch_size', type=int, default=12, help='batch size')
parser.add_argument('--move', type=bool, default=False, help='move images to attached bucket')
parser.add_argument('--output_dir', type=str, default='/home/trashwheel/auto_annotations', help='path to output image directory')


if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.batch_size,args.move, args.output_dir)