
import json
import numpy as np
from collections import defaultdict
import argparse
from utils import *
import sys

def convert_coco_json(dir=str, annotation_file=str):
    counter = 0
    save_dir = os.path.join(dir,'converted')  # output directory
    

    # Import json
    with open(annotation_file) as f:
        fn = Path(save_dir) / 'labels'   # folder name
        fn.mkdir(exist_ok=True, parents=True)  # make folder
       
        data = json.load(f)
        print('Number of images:', len(data['images']))
        print('Number of annotations:', len(data['annotations']))
        print(f'Converting {annotation_file}...')

        # Create image dict
        #images = {x['id']: x for x in data['images']}
        images = {}
        for x in data['images']:
            
            if x['id'] not in images:
                images[x['id']] = x
            else:
                counter += 1
                #sys.stdout.write(f'\r {counter} duplicate images found')
                

        # Create image-annotations dict
        imgToAnns = defaultdict(list)
        ann_counter = 0
        for ann in data['annotations']:
            ann_counter += 1
            imgToAnns[ann['image_id']].append(ann)
       
        print(f'Number of duplicate images: {counter}')
        print(f'annotations length: {len(imgToAnns)}')
        # Write labels file
        for img_id, anns in imgToAnns.items():
            #print(f'Converting image {counter} of {len(imgToAnns)}...')
            #img = images['%g' % img_id] also causing error
            img = images[img_id]
            h, w, f = img['height'], img['width'], img['file_name']
            # if fixed_size:
            #     h = int(height)
            #     w = int(width)

            bboxes = []
            for ann in anns:
                
                # The COCO box format is [top left x, top left y, width, height]
                box = np.array(ann['bbox'], dtype=np.float64)
                box[:2] += box[2:] / 2  # xy top-left corner to center
                box[[0, 2]] /= w  # normalize x
                box[[1, 3]] /= h  # normalize y
                if box[2] <= 0 or box[3] <= 0:  # if w <= 0 and h <= 0
                    continue

                cls = ann['category_id']
                box = [cls] + box.tolist()
                if box not in bboxes:
                    bboxes.append(box)
              
            # Write
            with open((fn / f).with_suffix('.txt'), 'a') as file:
                #print(f, w, h, file=file)  # filename width height # no need to write this, messes up the training parser
                for i in range(len(bboxes)):
                    line = *(bboxes[i]),  # cls, box or segments
                    file.write(('%g ' * len(line)).rstrip() % line + '\n')
                    

parser = argparse.ArgumentParser(description='Convert COCO annotations to YOLOv5 format.')
parser.add_argument('--dir', type=str, default='data/modified', help='directory to save converted labels')
parser.add_argument('--annotation_file', type=str, default='data/modified/formatted_updated.json', help='annotation file name')

if __name__ == '__main__':
    args = parser.parse_args()

    convert_coco_json(dir=args.dir, annotation_file=args.annotation_file)

#json dir is the directory where the json file is located
#'training/yolov5_training/exp<n>' is the directory where the json files are located here