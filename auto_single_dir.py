import os
import json
from ultralytics import YOLO
import datetime
import argparse


def auto_annotate(model, image_dir,batch_size=12,move=False,output_image_dir="/home/trashwheel/auto_annotations",output_annotation_dir='/home/trashwheel/auto_annotations/annotations'):
    '''
    Automatically annotate images in a directory using a YOLOv8 model. Generates a COCO json annotation file.
    pass path to trash wheel folder i.e. /home/trashwheel/1
    '''
    model = YOLO(model)
    ann_name = image_dir.split('/')[0]+ '_' + datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    if not os.path.exists(output_image_dir):
        print(f"ERROR: {output_image_dir} not found")
        return
    if not os.path.exists(image_dir):
        print(f"ERROR: {image_dir} not found")
        return
    images = os.listdir(image_dir)
    if len(images) == 0:
        print(f"ERROR: {image_dir} is empty")
        return
    image_list = [f'{image_dir}/{image}' for image in images if image.split('.')[-1] in ['jpg','jpeg','png']]
    
   
    
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
                # move images to output_image_dir
                 os.system(f"mv {image} {output_image_dir}")

        for i,item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xywhn
            h,w = item.orig_shape
            file_name = batch[i].split('/')[-1]
            data['images'].append({"file_name":file_name,"id":image_id,"width":w,"height":h})
       
            for box,cls in zip(boxes,classes):
                x,y,w,h = [float    (b) for b in box]
                data['annotations'].append({
                    "id" : len(data['annotations']),
                    "image_id":image_id,
                    "category_id":int(cls),
                    "bbox":[x,y,w,h],
                    "file_name":file_name,
                    "iscrowd":0,
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
parser.add_argument('--output_image_dir', type=str,default='/home/trashwheel/auto_annotations', help='path to output image directory')
parser.add_argument('--output_annotation_dir', default='/home/trashwheel/auto_annotations/annotations', type=str, help='path to output annotation directory')

if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.dir, args.batch_size,args.move, args.output_image_dir, args.output_annotation_dir)