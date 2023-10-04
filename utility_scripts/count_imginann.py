import json

def count_annotations():
    with open('data/modified/modified_annotations_updated.json', 'r') as json_file:
        data = json.load(json_file)
    image_dict = {}
    repeat_images = 0

    for i in range(0,len(data['annotations'])):
        file = data['annotations'][i]['file_name']
        if file not in image_dict:
            image_dict[file] = 1
        else:
            repeat_images += 1
            #print(f'Repeat Image: {file}')


    print(f'Repeat Images: {repeat_images}')
    print(f'Number of Images in annotations: {len(image_dict)}')
    print(f'Number of Annotations: {len(data["annotations"])}')


count_annotations()