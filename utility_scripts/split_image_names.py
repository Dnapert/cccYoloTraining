import json

def split_image_names(annotations,depth):
    '''
    cut leading directories from image names in annotations
    :param annotations: path to annotations file
    :param depth: number of directories (slashes) to cut i.e. 3 for data/images/2020/2020120111100728.jpg
    '''
    with open(annotations, 'r') as f:
        data = json.load(f)
    for i in data['images']:
        file_name = i['file_name']
        file_name = file_name.split('/',depth)[-1]
        i['file_name'] = file_name
        print(file_name)
    with open('annotations/output_split.json', 'w') as f:
        json.dump(data, f, indent=4)


split_image_names('annotations/output.json',3)