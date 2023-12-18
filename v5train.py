from ultralytics import YoloV5
import argparse

def trainv5(data,epochs):
    model = YoloV5('yolov5s.pt')
    results = model.train(data=data,epochs=epochs,device=0)
 
    
argparser = argparse.ArgumentParser()
argparser.add_argument('--data', type=str, default='data/coco128.yaml', help='dataset.yaml path')
argparser.add_argument('--epochs', type=int, default=100, help='number of epochs')
args = argparser.parse_args()

if __name__ == '__main__':
    trainv5(args.data,args.epochs)