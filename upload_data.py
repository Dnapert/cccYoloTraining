import requests
import argparse
import os

url = "https://us-central1-cleancurrentscoalition.cloudfunctions.net/upload-images"


def upload_data(device_id, raw_image_path, annotated_image_path, data):
    files = {
        "device_id": (None, device_id),
        "contents_data": (None, data),
        "raw_image_file": ("", open(raw_image_path, "rb")),
        "annotated_image_file": ("", open(annotated_image_path, "rb")),
    }
    
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Images uploaded successfully.")
    else:
        print(f"Error uploading images. Status code: {response.status_code}")
        print(response.text)



parser = argparse.ArgumentParser(description='Upload raw and annotated images and trash collected data to the server')
parser.add_argument('--device_id', type=int, help='unique id of device')
parser.add_argument('--raw_image_path', type=argparse.FileType('rb'), help='directory path to raw image of trash on the trashwheel')
parser.add_argument('--annotated_image_path', type=argparse.FileType('rb'), help='directory path to annotated image of trash on the trashwheel')
parser.add_argument('--data', type=str, default={}, help='collected trash data')

if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.raw_image_path) or not os.path.exists(args.annotated_image_path):
        print("One or both image files do not exist or paths are invalid.")
    else:
        upload_data(device_id=args.device_id, raw_image_path=args.raw_image_path, annotated_image_path=args.annotated_image_path, data=args.data)