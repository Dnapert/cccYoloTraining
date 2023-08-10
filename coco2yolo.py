
import json
import numpy as np
from collections import defaultdict
import argparse
from utils import *

def convert_coco_json(json_dir=str, use_segments=bool, cls91to80=bool, fixed_size=bool,height=int,width=int):
    
    save_dir = os.path.join(json_dir,'converted')  # output directory
    coco80 = coco91_to_coco80_class()

    # Import json
    for json_file in sorted(Path(json_dir).resolve().glob('*.json')):
        fn = Path(save_dir) / 'labels'   # folder name
        fn.mkdir(exist_ok=True, parents=True)  # make folder
        with open(json_file) as f:
            data = json.load(f)
            #print('Number of images:', len(data['images']))
            #print('Number of annotations:', len(data['annotations']))
            print(f'Converting {json_file}...')

        # Create image dict
        #images = {'%g' % x['id']: x for x in data['images']}  this line was causing error, we dont need to convert to string
        images = {x['id']: x for x in data['images']}
        print('images: ',len(images))
        # Create image-annotations dict
        imgToAnns = defaultdict(list)
        for ann in data['annotations']:
            imgToAnns[ann['image_id']].append(ann)
       

        # Write labels file
        for img_id, anns in tqdm(imgToAnns.items(), desc=f'Annotations {json_file}'):
            #img = images['%g' % img_id] also causing error with line 23
            img = images[img_id]
            h, w, f = img['height'], img['width'], img['file_name']
            if fixed_size:
                h = height
                w = width

            bboxes = []
            segments = []
            for ann in anns:
                if ann['iscrowd']:
                    continue
                # The COCO box format is [top left x, top left y, width, height]
                box = np.array(ann['bbox'], dtype=np.float64)
                box[:2] += box[2:] / 2  # xy top-left corner to center
                box[[0, 2]] /= w  # normalize x
                box[[1, 3]] /= h  # normalize y
                if box[2] <= 0 or box[3] <= 0:  # if w <= 0 and h <= 0
                    continue

                cls = coco80[ann['category_id'] - 1] if cls91to80 else ann['category_id'] - 1  # class
                box = [cls] + box.tolist()
                if box not in bboxes:
                    bboxes.append(box)
                # Segments
                if use_segments:
                    if len(ann['segmentation']) > 1:
                        s = merge_multi_segment(ann['segmentation'])
                        s = (np.concatenate(s, axis=0) / np.array([w, h])).reshape(-1).tolist()
                    else:
                        s = [j for i in ann['segmentation'] for j in i]  # all segments concatenated
                        s = (np.array(s).reshape(-1, 2) / np.array([w, h])).reshape(-1).tolist()
                    s = [cls] + s
                    if s not in segments:
                        segments.append(s)

            # Write
            with open((fn / f).with_suffix('.txt'), 'a') as file:
                print(f, w, h, file=file)  # filename width height
                for i in range(len(bboxes)):
                    line = *(segments[i] if use_segments else bboxes[i]),  # cls, box or segments
                    file.write(('%g ' * len(line)).rstrip() % line + '\n')
                    
def merge_multi_segment(segments):
    """Merge multi segments to one list.
    Find the coordinates with min distance between each segment,
    then connect these coordinates with one thin line to merge all 
    segments into one.

    Args:
        segments(List(List)): original segmentations in coco's json file.
            like [segmentation1, segmentation2,...], 
            each segmentation is a list of coordinates.
    """
    s = []
    segments = [np.array(i).reshape(-1, 2) for i in segments]
    idx_list = [[] for _ in range(len(segments))]

    # record the indexes with min distance between each segment
    for i in range(1, len(segments)):
        idx1, idx2 = min_index(segments[i - 1], segments[i])
        idx_list[i - 1].append(idx1)
        idx_list[i].append(idx2)

    # use two round to connect all the segments
    for k in range(2):
        # forward connection
        if k == 0:
            for i, idx in enumerate(idx_list):
                # middle segments have two indexes
                # reverse the index of middle segments
                if len(idx) == 2 and idx[0] > idx[1]:
                    idx = idx[::-1]
                    segments[i] = segments[i][::-1, :]

                segments[i] = np.roll(segments[i], -idx[0], axis=0)
                segments[i] = np.concatenate([segments[i], segments[i][:1]])
                # deal with the first segment and the last one
                if i in [0, len(idx_list) - 1]:
                    s.append(segments[i])
                else:
                    idx = [0, idx[1] - idx[0]]
                    s.append(segments[i][idx[0]:idx[1] + 1])

        else:
            for i in range(len(idx_list) - 1, -1, -1):
                if i not in [0, len(idx_list) - 1]:
                    idx = idx_list[i]
                    nidx = abs(idx[1] - idx[0])
                    s.append(segments[i][nidx:])
    return s


def min_index(arr1, arr2):
    """Find a pair of indexes with the shortest distance. 
    Args:
        arr1: (N, 2).
        arr2: (M, 2).
    Return:
        a pair of indexes(tuple).
    """
    dis = ((arr1[:, None, :] - arr2[None, :, :]) ** 2).sum(-1)
    return np.unravel_index(np.argmin(dis, axis=None), dis.shape)

parser = argparse.ArgumentParser(description='Convert COCO annotations to YOLOv5 format.')
parser.add_argument('--json_dir', type=str, default='training/yolov5_training/exp2', help='directory path to COCO JSON files')
parser.add_argument('--use_segments', action='store_true',default= False, help='use segmentations instead of bounding boxes')
parser.add_argument('--cls91to80', action='store_true',default=False, help='convert 91-class COCO to 80-class')
parser.add_argument('--fixed_size',type=bool,default=False, help='use fixed size for image width and height')
parser.add_argument('--width', type=int, default=640, help='fixed image width')
parser.add_argument('--height', type=int, default=480, help='fixed image height')
args = parser.parse_args()

convert_coco_json(json_dir=args.json_dir, use_segments=args.use_segments, cls91to80=args.cls91to80, fixed_size=args.fixed_size, width=args.width, height=args.height)

#json dir is the directory where the json file is located
#'training/yolov5_training/exp<n>' is the directory where the json file is located in here