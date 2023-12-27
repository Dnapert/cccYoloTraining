import os
import json
import argparse
import uuid
import cv2
from collections import defaultdict
def convert_yolo_bbox_to_coco_bbox(yolo_bbox, width, height):
    # YOLO format: x_center, y_center, w, h (all normalized)
    # COCO format: x1, y1, w, h (absolute values)

    x_center, y_center, w, h = yolo_bbox  

    # center coordinates and dimensions to absolute values
    x_center, y_center, w, h = x_center * width, y_center * height, w * width, h * height

    # Calculate top left corner of the bbox
    x1 = x_center - w / 2
    y1 = y_center - h / 2

    # Ensure that the coordinates are within the image boundaries
    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = min(x1 + w, width - 1)
    y2 = min(y1 + h, height - 1)

    # Update width and height to reflect potential adjustments
    w, h = x2 - x1, y2 - y1

    return [x1, y1, w, h]


    
def yolo_to_coco(dir,ann_name):
    '''
    given a directory with a yolo dataset (images and labels directories), convert to coco json format
    You will need to modify the categories dictionary to match your dataset!
    '''
    anns = os.listdir(f'{dir}/labels')
    images = os.listdir(f'{dir}/images')
    image_shapes = defaultdict(dict)
    for image in images:
        try:
            img = cv2.imread(f'{dir}/images/{image}')
            height,width,channels = img.shape
        except:
            print("error",image)
            continue
        image_shapes[image.split('.')[0]]["height"] = height
        image_shapes[image.split('.')[0]]["width"] = width
    image_ids = {i.split('.')[0]:uuid.uuid4().hex for i in images}
    categories = {
                22:'plastic_bottle',
                23:'large_plastic_bottle',
                14:'plastic_cap'
                }
    
    data = {}
  
    data['images'] = [{"file_name":i,"id":image_ids[i.split(".")[0]],"width":image_shapes[image.split('.')[0]]["width"],"height":image_shapes[image.split('.')[0]]["height"]} for i in images]
    data['annotations'] = []
    for file in anns:
        with open(f'{dir}/labels/{file}','r') as f:
            try:
                lines = f.readlines()
            except:
                print(file)
                continue
                
            for line in lines:
                line = line.split(' ')
                # The COCO box format is [top left x, top left y, width, height]
                bbox = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]
                width=image_shapes[file.split('.')[0]]["width"]
                height=image_shapes[file.split('.')[0]]["height"]
                new_bbox = convert_yolo_bbox_to_coco_bbox(bbox, width, height)
                data['annotations'].append({
                    "image_id": image_ids[file.split('.')[0]],
                    "category_id": int(line[0]),
                    "bbox": new_bbox,
                "file_name": file.split('.')[0] + '.jpg',
                })
                    
    data['categories'] = [{'id':id,'name':name,'supercategory':""} for id,name in categories.items()]
    with open(f"{dir}/{ann_name}",'w') as f:
        json.dump(data,f,indent=4)
        
argparser = argparse.ArgumentParser()
argparser.add_argument('-d','--dir',help='path to directory containing images and labels')
argparser.add_argument('-a','--ann',help='name of annotation file')

args = argparser.parse_args()
dir = args.dir
ann_name = args.ann

if __name__ == '__main__':
    yolo_to_coco(dir,ann_name)