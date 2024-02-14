import cv2
from ultralytics import YOLO
import numpy as np
model = YOLO('best.pt') 
img = cv2.imread('images/resized_images/2_1695470532000.jpg')
results = model(img,device=0)  # results list
for i,r in enumerate(results):
    res = r.boxes
    classes = res.cls
    height,width = r.orig_shape
    boxes = np.squeeze(res.xywh.cpu())
    for box,cls in zip(boxes,classes):
        x,y,w,h = [int(b) for b in box]
        top_left_x = x - (w//2)
        top_left_y = y - (h//2)
        bottom_right_x = x + (w//2)
        bottom_right_y = y + (h//2)
        clas = int(cls)
        cv2.rectangle(img, (top_left_x,top_left_y),(bottom_right_x,bottom_right_y), (0,255,0), 2)
        cv2.putText(img, model.names[clas], (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()