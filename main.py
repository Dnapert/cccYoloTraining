from dataset_builder import DatasetBuilder
import argparse
import os

run = True
def get_input(input_phrase):
    print(input_phrase)
    path = input()
    if path == '':
        print('You did not enter anything! Please try again.')
        path = get_input(input_phrase)
    elif path == 'q' or path == 'quit':
        exit()
    else:
        return path
def handle_augmentations(class_names):
        class_augmentation_dict = {}
        for class_name in class_names:
            print(f'Would you like to augment the {class_name} class?')
            if get_input('') == 'y' or 'yes':
                num = get_input('How many images would you like to augment?')
                if not num.isdigit():
                    print('You did not enter a valid number!')
                    num = get_input('How many images would you like to augment?')
                if num == 'c':
                    continue
                else:
                    class_augmentation_dict[class_name] = num
               
            print(f'Augmenting {class_augmentation_dict}')
            get_input(f'Press c to confirm or r to restart')
            if get_input('') == 'r':
                class_augmentation_dict = handle_augmentations(class_names)
            return class_augmentation_dict


def exit():
    print('Exiting...')
    con = False
    quit()

def main():
  
    while run:
        print('Welcome to the dataset builder!\n At any time, you can quit by typing "q" or "quit"')
        name = get_input("Enter the project name you would like to create, or the name of an existing project:")

        if os.path.exists(f'experiments/{name}'):
            print('Found a project with that name!')
            print("If you would like to continue, enter 'y' or 'yes'")
            if not get_input('') == 'y' or 'yes':
                exit() 
            with open(f'experiments/{name}/config.json', 'r') as f:
                config = json.load(f)
            print('Would you like to change the project name?')
            if get_input('') == 'y' or 'yes':
                name = get_input('Please enter the new project name: ')
            print('Would you like to change the path to the images?')
            if get_input('') == 'y' or 'yes':
                images = get_input('Please enter the path to the directory containing the images you would like to use: ')
                if not os.path.exists(images):
                    print('The path you entered does not exist!')
                    images = get_input('Please enter the path to the directory containing the images you would like to use: ')

        images = get_input('Please enter the path to the directory containing the images you would like to use: ')
        if not os.path.exists(images):
            print('The path you entered does not exist!')
            images = get_input('Please enter the path to the directory containing the images you would like to use: ')
        annotations = get_input('Please enter the path to the annotations file you would like to use: ')
        if not os.path.exists(annotations):
            print('The path you entered does not exist!')
            annotations = get_input('Please enter the path to the annotations file you would like to use: ')
        new_dataset = DatasetBuilder(project_name=name, annotations=annotations, images=images)
        print('Do you want to combine another dataset with this one?')
        if get_input('') == 'y' or 'yes':
            annotations2 = get_input('Please enter the path to the annotations file you would like to use or c to cancel: ')
            if annotations2 == 'c':
                continue
            if not os.path.exists(annotations2):
                print('The path you entered does not exist!')
                annotations2 = get_input('Please enter the path to the annotations file you would like to use or c to cancel: ')
            new_dataset.combine_datasets(annotations2)
        print('Are you resizing the images?(y/n)')
        answer = get_input('')
        if answer == 'y' or 'yes':
            new_dataset.resize_images(640)
        if answer == 'n' or 'no':
            print('Skipping resizing...')
        print(f'Current classes{new_dataset.class_dict} ')
        print('Do you want to remove any classes?(y/n)')
        answer = get_input('')
        if answer == 'y' or 'yes':
            print('Enter the classes you want to remove, separated by a comma')
            classes = get_input('')
            classes = classes.split(',')
            print(classes)
        if answer == 'n' or 'no':
            print('Skipping class removal...')
        print('Are you augmenting the images?(y/n)')
        augment = get_input('')
        if augment == 'y' or 'yes':
            augmentations = handle_augmentations(new_dataset.class_dict.values())
            #new_dataset.augment_images(augmnetations)
        elif augment == 'n' or 'no':
            print('Skipping augmentations...')
        



main()



