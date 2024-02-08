import os
import json
from ultralytics import YOLO
import datetime
import argparse


def auto_annotate(model, image_dir,batch_size=12,move=False,output_image_dir='auto_annotations',output_annotation_dir='annotations'):
    '''
    Automatically annotate images in a directory using a YOLOv8 model. Generates a COCO json annotation file.
    '''
    model = YOLO(model)
    ann_name = image_dir.split('/')[0]+ '_' + datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    images = os.listdir(image_dir)
    data = {'categories':[],'images':[],'annotations':[]}
    names = model.names
    current_batch = batch_size
    prev_batch = 0

    
    data['categories'] = [{"id":k,"name":v,"supercategory":"object"} for k,v  in enumerate(names)]

    image_list = [f'{image_dir}/{image}' for image in images]
    
    while current_batch < len(image_list):
        batch = image_list[prev_batch:current_batch]
        results = model(batch,verbose=False)
        if move:
            for image in batch:
                # move images to attached bucket
                 os.system(f"mv {image} {output_image_dir}")

        for i,item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xywhn
            h,w = item.orig_shape
            data['images'].append({"file_name":batch[i].split('/')[-1],"id":image_id,"width":w,"height":h})
            # if len(boxes) == 0:
            #     os.system(f"mv {batch[i]} background/{batch[i].split('/')[-1]} ")
            for box,cls in zip(boxes,classes):
                x,y,w,h = [float    (b) for b in box]
                data['annotations'].append({
                    "id" : len(data['annotations']),
                    "image_id":image_id,
                    "category_id":int(cls),
                    "bbox":[x,y,w,h],
                    "file_name":batch[i].split('/')[-1]
                     })
   
        prev_batch = current_batch
        current_batch += batch_size if current_batch + batch_size < len(image_list) else len(image_list)
        
    print(f"Annotations written to annotations/{ann_name}.json")
    print(f"Annotated {len(data['images'])} images")
    with open(f'{output_annotation_dir}/{ann_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

parser = argparse.ArgumentParser(description='Auto Annotate')
parser.add_argument('--model', type=str, help='path to model')
parser.add_argument('--dir', type=str, help='path to image directory')
parser.add_argument('--batch_size', type=int, help='batch size')
parser.add_argument('--move', type=bool, default=False,help='move images to attached bucket')
parser.add_argument('--output_image_dir', type=str, help='path to output image directory')
parser.add_argument('--output_annotation_dir', default='annotations', type=str, help='path to output annotation directory')

if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.dir, args.batch_size,args.move, args.output_image_dir, args.output_annotation_dir)