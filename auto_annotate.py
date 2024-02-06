import os
import json
from ultralytics import YOLO
import datetime
import uuid
import argparse


def auto_annotate(model, image_dir,batch_size=12):
    '''
    Automatically annotate images in a directory using a YOLOv8 model. Generates a COCO json annotation file.
    '''
    model = YOLO(model)
    ann_name = image_dir.split('/')[0]+ '_' + datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    images = os.listdir(image_dir)
    data = {'categories':[],'images':[],'annotations':[]}
    names = model.names
    image_list = []
    current_batch = batch_size
    prev_batch = 0

        
    for k,v in enumerate(names):
        data['categories'].append({"id":k,"name":v,"supercategory":"object"})
    
    for i in range(len(images)):  # change this to len(images) to annotate all images
        image_list.append((f'{image_dir}/{images[i]}'))
    mod = len(image_list) % batch_size
    
    if mod != 0:
        current_batch -= mod
   
    while current_batch < len(image_list):
        batch = image_list[prev_batch:current_batch if current_batch < len(image_list) else len(image_list)]
        results = model(batch,verbose=False)

        for i,item in enumerate(results):
            image_id    = i
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xywhn
            h,w = item.orig_shape
            data['images'].append({"file_name":images[i],"id":image_id,"width":w,"height":h})
            for box,cls in zip(boxes,classes):
                x,y,w,h = [float    (b) for b in box]
                data['annotations'].append({
                    "image_id":image_id,
                    "category_id":int(cls),
                    "bbox":[x,y,w,h],
                    "file_name":images[i].split('/')[-1]
                     })
                
            prev_batch = current_batch
            current_batch += batch_size
    
  
    print(f"Annotated {len(images)} images")
    with open(f'annotations/{ann_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

parser = argparse.ArgumentParser(description='Auto Annotate')
parser.add_argument('--model', type=str, help='path to model')
parser.add_argument('--dir', type=str, help='path to image directory')
parser.add_argument('--batch_size', type=int, help='batch size')

if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.dir, args.batch_size)