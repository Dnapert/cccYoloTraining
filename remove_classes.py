import json
import argparse

baltimore_ai_class_dict={ 
            0:"plastic_bag",
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

def remove_classes_from_annotations(annotations_path, classes_to_remove, output_file,class_dict)->None:
    
    """
    Remove classes from annotations file
    :param annotations_path: Path to annotations file
    :param classes_to_remove: List of classes to remove
    :param output_file: Path to output file
    :return: None
    """

    print("Classes to remove:")
    for i in classes_to_remove:
        print(class_dict[i])
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)

    annotations['annotations'] = [c for c in annotations['annotations'] if c['category_id'] not in classes_to_remove]
    annotations['categories'] = [c for c in annotations['categories'] if c['id'] not in classes_to_remove]


    with open(output_file, 'w') as f:
        json.dump(annotations, f)
        
parser = argparse.ArgumentParser(description='Remove classes from annotations file')
parser.add_argument('--annotations_path', type=str, help='Path to annotations file')
parser.add_argument('--classes_to_remove', nargs='+',type=int, help='List of classes to remove seperated by space i.e. 0 1 2')
parser.add_argument('--output_file', type=str, help='Path to output file')
args = parser.parse_args()

classes_to_remove = args.classes_to_remove   
annotations_path = args.annotations_path
output_file = args.output_file
class_dict = baltimore_ai_class_dict

remove_classes_from_annotations(annotations_path, classes_to_remove, output_file,class_dict)
