import os
import json
from ultralytics import YOLO
import datetime
import argparse

def auto_annotate(model, image_dir, batch_size=12, move=False, output_dir="/home/trashwheel/auto_annotations"):
    '''
    Automatically annotate images in a directory using a YOLOv8 model. Generates a COCO json annotation file.
    pass path to trash wheel folder i.e. /home/trashwheel/1/12-1-23/images
    '''
    model = YOLO(model)
    
    if not os.path.exists(output_dir):
        print(f"ERROR: {output_dir} not found")
        return
    if not os.path.exists(image_dir):
        print(f"ERROR: {image_dir} not found")
        return
    images = os.listdir(image_dir)
    if len(images) == 0:
        print(f"ERROR: {image_dir} is empty")
        return
    image_list = [f'{image_dir}/{image}' for image in images if image.split('.')[-1] in ['jpg','jpeg','png']]
    if len(image_list) == 0:
        print(f"ERROR: {image_dir} is empty")
        return
    annotation_name = datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")  # timestamp for annotation file and directory
    
    if move:
        if not os.path.exists(f"{output_dir}/{annotation_name}"):
            os.makedirs(f"{output_dir}/{annotation_name}")
    
    print(f"Found: {len(image_list)} images")
    data = {'categories': [], 'images': [], 'annotations': []}
    names = model.names
    
    data['categories'] = [{"id": k, "name": v, "supercategory": "object"} for k, v in names.items()]
    
    for i in range(0, len(image_list), batch_size):
        batch = image_list[i:i+batch_size]
        results = model(batch, verbose=False)
        if move:
            for image in batch:
                # move images to output_dir
                os.system(f"mv {image} {output_dir}/{annotation_name}")
                
        for j, item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res[:, -1]
            boxes = res[:, :-1]
            height, width = item.orig_shape
            file_name = batch[j].split('/')[-1]
            data['images'].append({"file_name": file_name, "id": image_id, "width": width, "height": height})
            
            for box, cls in zip(boxes, classes):
                x1, y1, x2, y2 = [float(b) for b in box]
                tl_x = x1
                tl_y = y1
                w = x2 - x1
                h = y2 - y1
                data['annotations'].append({
                    "id": len(data['annotations']),
                    "image_id": image_id,
                    "category_id": int(cls),
                    "bbox": [tl_x, tl_y, w, h],
                    "file_name": file_name,
                    "area": w * h,
                    "segmentation": [],
                    "iscrowd": 0,
                })
                
    print(f"Annotations written to {annotation_name}.json")
    print(f"Annotated {len(data['images'])} images")
    with open(f'{output_dir}/{annotation_name}.json', 'w') as f:
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
