import json

def add_key(annotation,output):
    '''
    Adds file name key to annotations file if missing
    '''
    image_dict = {}
    with open(annotation, 'r') as f:
        data = json.load(f)
    for i in data['images']:
        image_dict[i['id']] = i['file_name']
    for a in data['annotations']:
        if not 'file_name' in a:
            a['file_name'] = image_dict[a['image_id']]
    with open(output, 'w') as f:
        json.dump(data, f, indent=4)

add_key('annotations/exp10.json','annotations/exp101.json')