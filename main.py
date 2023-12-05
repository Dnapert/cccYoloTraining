from dataset_builder import DatasetBuilder
import argparse
import os
import json
import copy
run = True
def get_input(input_phrase):
    print(input_phrase)
    path = input()
    if path == '':
        print('You did not enter anything! Please try again.')
        path = get_input(input_phrase)
    if path == 'c' or path == 'cancel':
        return 'c'
    elif path == 'q' or path == 'quit':
        exit()
    else:
        return path
def handle_change_config(project):
    with open(f'experiments/{project}/config.json', 'r+') as f:
        config = json.load(f)
    data = copy.deepcopy(config)
    images = config['images']
    annotations = config['annotations']
    name = config['name']
    print(f'Loaded project {name}\n with image directory {images}\n and annotations {annotations} ')
    
    new_images = get_input('Would you like to change the path to the images?')
    if new_images == 'y' or new_images == 'yes':
        data['images'] = get_directory('Please enter the path to the directory containing the images you would like to use: ')
    elif new_images == 'c' or new_images == 'cancel' or new_images == 'n' or new_images == 'no':
        print("Skipping image directory change...")
    new_annotations = get_input('Would you like to change the path to the annotations?')
    if new_annotations == 'y' or new_annotations == 'yes':
        data['annotations'] = get_directory('Please enter the path to the annotations file you would like to use: ')
    elif new_annotations == 'c' or new_annotations == 'cancel' or new_annotations == 'n' or new_annotations == 'no':
        print("Skipping annotations change...")
    with open(f'experiments/{name}/config.json', 'w') as f:
        f.seek(0)
        json.dump(data, f,indent=4)
        f.truncate()
    return data
            

def handle_augmentations(class_names):
        class_augmentation_dict = {}
        for class_name in class_names:
            print(f'Would you like to augment the {class_name} class?')
            answer = get_input('')
            if answer == 'y' or answer == 'yes':
                num = get_input('How many images would you like to augment?')
                if not num.isdigit():
                    print('You did not enter a valid number!')
                    num = get_input('How many images would you like to augment?')
                if num == 'c':
                    return 'c'
                else:
                    class_augmentation_dict[class_name] = num
               
            print(f'Augmenting {class_augmentation_dict}')
            get_input(f'Press c to confirm or r to restart')
            if get_input('') == 'r':
                class_augmentation_dict = handle_augmentations(class_names)
            return class_augmentation_dict

def handle_class_removal(class_dict):
    print("Current Classes:\n")
    for k, v in class_dict.items():
        print(f'{k}: {v}\n')

    class_ids = get_input("Enter the class ID's you would like to remove, separated by a comma. i.e. 1,2,3 or c to cancel")
    if class_ids.lower() in ['c', 'cancel']:
        return []

    class_ids = class_ids.split(',')  # Split the string into a list
    class_ids = [id.strip() for id in class_ids]  # Remove whitespace

    valid_class_ids = []
    for class_id in class_ids:
        if class_id not in class_dict:
            print(f'Class {class_id} does not exist!')
        elif not class_id.isdigit():
            print(f'{class_id} is not a valid class ID!')
        else:
            valid_class_ids.append(int(class_id))
    print(f'Removing classes:')
    for class_id in valid_class_ids:
        print(f'{class_dict[str(class_id)]}\n')
    proceed = get_input('Enter p to proceed or r to restart')
    if proceed == 'r':
        classes = handle_class_removal(new_dataset.class_dict)
    if proceed == 'p':
        return valid_class_ids

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False 

def handle_data_split():
    split_ratio = get_input('Please enter the ratio you would like to split the dataset by test,train,and val: ex. .8,.1,.1 ')
    test,train,val = split_ratio.split(',')
    list_split = [test,train,val]
    for i in list_split:
        if not is_float(i):
            print('You did not enter a valid number!')
            split_ratio = handle_data_split()
    

    split_seed = get_input('Please enter the seed you would like to use for the split: ')
    return float(test),float(train),float(val), split_seed

def get_directory(text)->str:
    print(text)
    path = input()
    if path == '':
        print('You did not enter anything! Please try again.')
        path = get_directory(text)
    elif path == 'c' or path == 'cancel':
        return 'c'
    elif not os.path.exists(path):
        print('The path you entered does not exist!')
        path = get_directory(text)

    else:
        return path
def exit():
    print('Exiting...')
    con = False
    quit()

def main():
    new_project = False
    while run:
        print('\n At any time, you can quit by typing "q" or "quit"')
        name = get_input("Enter the project name you would like to create, or the name of an existing project:")

        if os.path.exists(f'experiments/{name}'):
            print('Found a project with that name!')
            answer = input("Do you want to load the project? (y/n)")
            print(answer)
            if answer == 'y' or answer =='yes':
                config = handle_change_config(name)
                new_dataset = DatasetBuilder(project_name=name, annotations=config['annotations'], images=config['images'])
            elif answer == 'n' or answer == 'no':
                exit()
        else:
            print('Creating a new project...')
            new_project = True
        if new_project:
            images = get_directory('Please enter the path to the directory containing the images you would like to use: ')
            annotations = get_directory('Please enter the path to the annotations file you would like to use: ')
            new_dataset = DatasetBuilder(project_name=name, annotations=annotations, images=images)
            print('Do you want to combine another dataset with this one?')
            ans = get_input('')
            if ans == 'y' or ans == 'yes':
                annotations2 = get_input('Please enter the path to the annotations file you would like to use or c to cancel: ')
                if annotations2 == 'c':
                    print('cancelled combining datasets')
                if not os.path.exists(annotations2):
                    print('The path you entered does not exist!')
                    annotations2 = get_input('Please enter the path to the annotations file you would like to use or c to cancel: ')
                new_dataset.combine_datasets(annotations2)

        resize = get_input('Are you resizing the images?(y/n)')
        if resize == 'y' or answer == 'yes':
            image_size = get_input('Please enter the target width you would like to resize the images to: ')
            new_dataset.resize_images(image_size)
        elif resize == 'n' or answer == 'no' :
            print('Skipping resizing...')
        print(f'Current classes{new_dataset.class_dict} ')
        
        answer = get_input('Do you want to remove any classes?(y/n)')
        if answer == 'y' or answer == 'yes':
            classes = handle_class_removal(new_dataset.class_dict)
            new_dataset.remove_classes(classes)
        if answer == 'n' or answer == 'no':
            print('Skipping class removal...')
        print('Are you augmenting the images?(y/n)')
        augment = get_input('')
        if augment == 'y' or  answer == 'yes':
            augmentations = handle_augmentations(new_dataset.class_dict.values())
            #new_dataset.augment_images(augmnetations)
        elif augment == 'n' or answer == 'no':
            print('Skipping augmentations...')
        #check if dataset is in yolo format
        if os.path.exists(f'experiments/{name}/labels'):
            print('Found a dataset in YOLO format, skipping conversion...')
            ans = get_input('If this is incorrect, type "convert", otherwise type n or no to continue')
            if ans == 'convert':
                new_dataset.to_yolo()
            else:
                print('continuing...')
        else:
            convert= get_input('Are you ready to conver to YOLO format?(y/n)')
            if convert == 'y' or convert == 'yes':
                new_dataset.to_yolo()
            elif convert == 'n' or convert == 'no':
                print('Skipping conversion...')
                print('Would you like to do anything else?\n to change the config file, type "config"\n to convert the dataset, type "convert"\n to exit, type "q" or "quit"')
                answer = get_input('')
                if answer == 'config':
                    config = handle_change_config(name)
                    new_dataset = DatasetBuilder(project_name=name, annotations=config['annotations'], images=config['images'])
                elif answer == 'convert':
                    answer = get_input('Are you ready to conver to YOLO format?(y/n)')
                    if answer == 'y' or answer == 'yes':
                        new_dataset.to_yolo()
                    elif answer == 'n' or answer == 'no':
                        print('Skipping conversion...')
                elif answer == 'q' or answer == 'quit':
                    exit()

        split = get_input('Are you splitting the dataset?(y/n)')
        if split == 'y' or split == 'yes':
            if not os.path.exists(f'experiments/{name}/labels'):
                print('You must convert the dataset to YOLO format before splitting!')
                convert = get_input('Would you like to convert the dataset now?(y/n)')
                if convert == 'y' or convert == 'yes':
                    new_dataset.to_yolo()
                elif convert == 'n' or convert == 'no':
                    print('Skipping conversion...')
            else:    
                test,train,val,seed = handle_data_split()
                new_dataset.split_data(test,train,val,seed)
                ans = get_input('Would you like to do anything else?\n to change the config file, type "config"\n  to exit, type "q" or "quit"')
                if ans == 'config':
                    config = handle_change_config(name)
                    new_dataset = DatasetBuilder(project_name=name, annotations=config['annotations'], images=config['images'])
                elif ans == 'q' or ans == 'quit':
                    exit()

main()



