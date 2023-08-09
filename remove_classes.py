import json

baltimore_ai_class_dict={ 0:"plastic_bag",
            1:"plastic_bottle",
            2:"plastic_cap",
            3:'plastic_container',
            4:"plastic_wrapper",
            5:"plastic_other",
            6:"foam_container",
            7:"Foam_other",
            8:"glass_bottle",
            9:"paper_container",
            10:"paper_other",
            11:"Metal_cap",
            12:"Metal_can",
            13:"ppe",
            14:"misc"
            }

def remove_classes_from_annotations(annotations_path, classes_to_remove, output_path,class_dict)->None:
    
    """
    Remove classes from annotations file
    :param annotations_path: Path to annotations file
    :param classes_to_remove: List of classes to remove
    :param output_path: Path to output file
    :return: None
    """

    print("Classes to remove:")
    for i in classes_to_remove:
        print(class_dict[i])
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)

    annotations['annotations'] = [c for c in annotations['annotations'] if c['category_id'] not in classes_to_remove]
    annotations['categories'] = [c for c in annotations['categories'] if c['id'] not in classes_to_remove]


    with open(output_path, 'w') as f:
        json.dump(annotations, f)
        
classes_to_remove = [9,10,11,12,13,14]   
annotations_path = "annotation_coco_format.json"
output_path = "annotation_coco_format_3.json"
class_dict = baltimore_ai_class_dict

remove_classes_from_annotations(annotations_path, classes_to_remove, output_path,class_dict)
