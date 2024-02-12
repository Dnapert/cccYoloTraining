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
    ann_name = image_dir.split('/')[0]+ '_' + datetime.datetime.now().strftime("%Y-%m-%d").replace("-0", "-")
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
    if not os.path.exists(image_dir):
        print(f"ERROR: {image_dir} not found")
        return
    directories = os.listdir(image_dir)
    if len(directories) == 0:
        print(f"ERROR: {image_dir} is empty")
        return
    
    dir_tree = {directory:os.listdir(f'{image_dir}/{directory}/images') for directory in directories}
    images = [f'{directory}/images/{image}' for directory in dir_tree for image in dir_tree[directory]]
    
    
    print(f"Found {len(images)} images")
    data = {'categories':[],'images':[],'annotations':[]}
    names = model.names
    current_batch = batch_size
    prev_batch = 0
    
    data['categories'] = [{"id":k,"name":v,"supercategory":"object"} for k,v  in names.items()]

    image_list = [f'{image_dir}/{image}' for image in images]
    print(len(image_list))
    counter = 0
    
    while current_batch < len(image_list):
        batch = image_list[prev_batch:current_batch]
        results = model(batch,verbose=False)

        for i,item in enumerate(results):
            image_id = len(data['images'])
            res = item.boxes.cpu().numpy()
            classes = res.cls
            boxes = res.xywhn
            h,w = item.orig_shape
            # Only add images with no detections
            
            if len(boxes) == 0:
                counter += 1
                sys.stdout.write(f'\r Found {counter} background images')
                if move:
                    os.system(f"mv {batch[i]} {output_image_dir}/{batch[i].split('/')[-1]} ")
                data['images'].append({"file_name":batch[i].split('/')[-1],"id":image_id,"width":w,"height":h})
                
    
        prev_batch = current_batch
        current_batch += batch_size if current_batch + batch_size < len(image_list) else len(image_list)
        
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