
import cv2
import json

def draw_bounding_box(img, annotation):
    '''
    takes image and coco annotation file, use this to test annoatation conversion
    '''
    with open(annotation, 'r') as f:
        data = json.load(f)
        boxes = []
        annotations = [i for i in data["annotations"] if i["file_name"] == img.split('/')[-1]]
        for i in range(len(annotations)):
            x = annotations[i]["bbox"][0]
            y = annotations[i]["bbox"][1]
            w = annotations[i]["bbox"][2]
            h = annotations[i]["bbox"][3]
            top_left_x = int(x)
            top_left_y = int(y)
            bottom_right_x = int(x + w)
            bottom_right_y = int(y + h)
            boxes.append([top_left_x, top_left_y, bottom_right_x, bottom_right_y])
    print(boxes)
    img = cv2.imread(img)
    for box in boxes:
        img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0))
   
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
draw_bounding_box('mareaverde_panama_sample/images/20231011_080844_1_2_043690.jpg', 'mareaverde_panama_sample/panama.json')