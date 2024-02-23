import os
import json
from ultralytics import YOLO
import datetime
import argparse


def auto_annotate(model,batch_size=12,move=False,output_dir="/home/trashwheel/auto_annotations"):
    '''
    Automatically annotate images in a directory using a YOLOv8 model. Generates a COCO json annotation file.
    pass path to trash wheel folder i.e. /home/trashwheel/1
    '''
    model = YOLO(model)
    buckets = [f'/home/trashwheel/{i}' for i in range(1,4)]
    image_list = []

    for bucket in buckets:
        subdirs = os.listdir(bucket)
        for subdir in subdirs:
            images = os.listdir(f"{bucket}/{subdir}/images")
            image_list += [f'{bucket}/{subdir}/images/{image}' for image in images if image.split('.')[-1] in ['jpg','jpeg','png']]
    print(f"Found: {len(image_list)} images")
    
    ann_name = datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-") # timestamp for annotation file and directory
    if not  os.path.exists(f"{output_dir}/{ann_name}"):
        os.makedirs(f"{output_dir}/{ann_name}")
    output_dir = f"{output_dir}/{ann_name}"
    output_annotation_dir = f"{output_dir}/{ann_name}.json"
    
    
    print(f"Found: {len(image_list)} images")
    data = {'categories':[],'images':[],'annotations':[]}
    names = model.names
    current_batch = batch_size
    prev_batch = 0
    
    data['categories'] = [{"id":k,"name":v,"supercategory":"object"} for k,v  in names.items()]
    
    while current_batch < len(image_list):
        batch = image_list[prev_batch:current_batch]
        results = model(batch,verbose=False)
        if move:
            for image in batch:
                # move images to output_dir
                 os.system(f"mv {image} {output_dir}")

        for i,item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xyxy
            height,width = item.orig_shape
            file_name = batch[i].split('/')[-1]
            data['images'].append({"file_name":file_name,"id":image_id,"width":width,"height":height})
       
            for box,cls in zip(boxes,classes):
                x1,y1,x2,y2 = [float    (b) for b in box]
                tl_x = x1
                tl_y = y1
                w = x2 - x1
                h = y2 - y1
                data['annotations'].append({
                    "id" : len(data['annotations']),
                    "image_id":image_id,
                    "category_id":int(cls),
                    "bbox":[tl_x,tl_y,w,h],
                    "file_name":file_name,
                    "area":w*h,
                    "segmentation":[],
                    "iscrowd":0,
                     })
   
        prev_batch = current_batch
        current_batch += batch_size if current_batch + batch_size < len(image_list) else len(image_list)
        
    print(f"Annotations written to annotations/{ann_name}.json")
    print(f"Annotated {len(data['images'])} images")
    with open(f'{output_annotation_dir}/{ann_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

parser = argparse.ArgumentParser(description='Auto Annotate')
parser.add_argument('--model', type=str,default='best.pt', help='path to model')
parser.add_argument('--batch_size', type=int, help='batch size')
parser.add_argument('--move', type=bool, default=False,help='move images to attached bucket')
parser.add_argument('--output_dir', type=str,default='/home/trashwheel/auto_annotations', help='path to output image directory')


if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.batch_size,args.move, args.output_dir)