import os
import json
from ultralytics import YOLO
import datetime
import argparse
import sys


def auto_annotate(model, image_dir,batch_size=12,move=False,output_image_dir='auto_annotations',output_annotation_dir='annotations'):
    '''
    Generate coco datset of only background images (no detections) using yolov8 model
    pass path to trash wheel folder i.e. /home/trashwheel/1
    '''
    model = YOLO(model)
    ann_name = image_dir.split('/')[-1]+ '_' + datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    if not os.path.exists(output_image_dir):
        print(f"ERROR: {output_image_dir} not found")
        return
    if not os.path.exists(image_dir):
        print(f"ERROR: {image_dir} not found")
        return
    directories = os.listdir(image_dir)
    if len(directories) == 0:
        print(f"ERROR: {image_dir} is empty")
        return
    
    dir_tree = {directory:os.listdir(f'{image_dir}/{directory}/images') for directory in directories}
    image_list = [f'{image_dir}/{directory}/images/{image}' for directory in dir_tree for image in dir_tree[directory]]
    
    print(f"Found: {len(image_list)} images")
    data = {'categories':[],'images':[],'annotations':[]}
    names = model.names

    
    data['categories'] = [{"id":k,"name":v,"supercategory":"object"} for k,v  in names.items()]

    counter = 0
    
    for i in range(0, len(image_list), batch_size):
        batch = image_list[i:i+batch_size]
        results = model(batch,verbose=False)

        for i,item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            boxes = res.xyxy
            h,w = item.orig_shape
            # Only add images with no detections
            
            if len(boxes) == 0:
                counter += 1
                file_name = batch[i].split('/')[-1]
                if move:
                    os.system(f"mv {batch[i]} {output_image_dir}/{file_name} ")
                data['images'].append({"file_name":file_name,"id":image_id,"width":w,"height":h})
            
        
    print(f"Annotations written to annotations/background_{ann_name}.json")
    print(f"Annotated {len(data['images'])} images")
    with open(f'{output_annotation_dir}/background_{ann_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

parser = argparse.ArgumentParser(description='Auto Annotate')
parser.add_argument('--model', type=str, help='path to model')
parser.add_argument('--dir', type=str, help='path to image directory')
parser.add_argument('--batch_size', type=int,default=12, help='number of images to process at a time, default is 12,if you run out of memory reduce this number')
parser.add_argument('--move', type=bool, default=False,help='move images to specified directory')
parser.add_argument('--output_image_dir', type=str, help='path to output image directory')
parser.add_argument('--output_annotation_dir', default='annotations', type=str, help='path to output annotation directory')

if __name__ == "__main__":
    args = parser.parse_args()
    auto_annotate(args.model, args.dir, args.batch_size,args.move, args.output_image_dir, args.output_annotation_dir)