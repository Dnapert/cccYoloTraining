import json

def count_annotations(annotation_file='annotations/merged_dataset.json'):
    '''
    Count number of images in an annotation file
    '''
    with open(annotation_file, 'r') as json_file:
        data = json.load(json_file)
    image_dict = {}
    repeat_images = 0

    for i in data['images']:
        file = i['file_name']
        if file not in image_dict:
            image_dict[file] = 1
        else:
            repeat_images += 1
            #print(f'Repeat Image: {file}')


    print(f'Repeat Images: {repeat_images}')
    print(f'Number of Images in annotations: {len(image_dict)}')
    print(f'Number of Annotations: {len(data["annotations"])}')


count_annotations()