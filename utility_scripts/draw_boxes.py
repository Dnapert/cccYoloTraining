import cv2
import argparse

def draw_bounding_box(img, annotation):
    '''
    this takes an image and an annotation in the form of a txt file (yolo format)
    '''
    img = cv2.imread(img)
    image_width = 640
    image_height = 480
    boxes = []
    with open(annotation, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            split_data = lines[i].split()
            print(split_data)
            x = (float(split_data[1])) * image_width
            y = (float(split_data[2])) * image_height
            w = float(split_data[3]) * image_width
            h = float(split_data[4]) * image_height
            top_left_x = int(x - (w/2))
            top_left_y = int(y - (h/2))
            bottom_right_x = int(x + (w/2))
            bottom_right_y = int(y + (h/2))
            boxes.append([top_left_x, top_left_y, bottom_right_x, bottom_right_y])
            
    for i in range(len(boxes)):
        top_left_x = boxes[i][0]
        top_left_y = boxes[i][1]
        bottom_right_x = boxes[i][2]
        bottom_right_y = boxes[i][3]
        cv2.rectangle(img, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

   
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', help='path to the image')
    parser.add_argument('--annotation', help='path to the annotation')
    args = parser.parse_args()

    if __name__ == '__main__':

        draw_bounding_box(args.img, args.annotation)

