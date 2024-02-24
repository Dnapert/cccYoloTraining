from ultralytics import YOLO
import argparse

def trainv8(data,epochs):
    model = YOLO('yolov8s.pt')
    results = model.train(data=data,epochs=epochs,batch=-1,device=0)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/coco128.yaml', help='dataset.yaml path')
    parser.add_argument('--epochs', type=int, default=100, help='number of epochs')
    args = parser.parse_args()
    trainv8(args.data,args.epochs)