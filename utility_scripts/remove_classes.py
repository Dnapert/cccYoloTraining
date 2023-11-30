import json
import argparse


def remove_classes_from_annotations(annotations_path, classes_to_remove, output_file):
    
    """
    Remove classes from annotations file remaps class ids, and creates a yaml file for yolo training
    :param annotations_path: Path to annotations file
    :param classes_to_remove: List of classes to remove
    :param output_file: Path to output file
    :return: None
    """
  
    
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)
            
    class_dict = {}

    for i in  annotations['categories']:
        class_dict[i['id']] = i['name']
    
    print("Classes to remove:")

    for i in classes_to_remove:
        print(class_dict[i])

    annotations['annotations'] = [c for c in annotations['annotations'] if c['category_id'] not in classes_to_remove]
    annotations['categories'] = [c for c in annotations['categories'] if c['id'] not in classes_to_remove]

    class_dict.clear()
    # get new class dict
    for i in  annotations['categories']:
        class_dict[i['id']] = i['name']

    # write  to yaml file
    with open(f"{output_file}.yaml","w") as f:
        f.write(f"nc: {len(class_dict)}\n")
        f.write(f"names: {list(class_dict.values())}")

    # Create a mapping from class_name to a new id
    class_to_new_id = {class_name: new_id for new_id, class_name in enumerate(class_dict.values())}
    #print(class_to_new_id)

    # Update the 'id' in categories using the new mapping
    for category in annotations['categories']:
        category['id'] = class_to_new_id[category['name']]

    # Update the 'category_id' in annotations using the new mapping
    for annotation in annotations['annotations']:
      
        original_class_name = class_dict[annotation['category_id']]
        annotation['category_id'] = class_to_new_id[original_class_name] 

   
    with open(output_file, 'w') as f:
        json.dump(annotations, f)
   
    print(f"Annotations saved to {output_file}")


argparse = argparse.ArgumentParser()
argparse.add_argument('--annotations_path',default='annotations/original_annotations.json', type=str, help='Path to annotations file')
argparse.add_argument('--classes_to_remove',default=[1], nargs='+',type=int, help='List of classes to remove seperated by space i.e. 0 1 2')
argparse.add_argument('--output_file',default='annotations/testing.json', type=str, help='Path to output file')

args = argparse.parse_args()

if __name__ == '__main__':
    print(args)
    remove_classes_from_annotations(args.annotations_path, args.classes_to_remove, args.output_file)