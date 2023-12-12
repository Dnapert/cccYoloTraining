import json
import numpy as np
from collections import defaultdict
import os
import sys
import shutil
import cv2
from pathlib import Path
from utility_scripts.get_class_dict import get_class_dict
from utility_scripts.labels_per_class import labels_per_class
from utility_scripts.utils import *
import albumentations as A
import copy
from datetime import datetime
import sys
import string
import random
import glob
from random import shuffle
import matplotlib.pyplot as plt



class DatasetBuilder:
    def __init__(self, project_name, annotations, images):
        self.name = project_name
        self.directory = f"experiments/{self.name}"
        self.annotations = annotations
        self.images = images
        self.config_file = f'{self.directory}/config.json'
        self.class_dict = {}

        self.new = self.check_project_exists()
        if not self.new:
            self.check_annotations_exists()
        self.check_images_exist()
        if self.new:
            self.copy_images()
        
    def check_project_exists(self) -> bool:
        '''
        check if the project already exists and if so , load the config file
        '''
        if not os.path.exists(self.directory) or not os.path.isdir(self.directory):
            print(f'Creating new project folder {self.directory}')
            os.mkdir(self.directory)
            class_dict = get_class_dict(self.annotations,False)
            labels = labels_per_class(f"{self.directory}/figures",self.annotations)
            self.class_dict = class_dict
            self.copy_annotations()
            with open(self.config_file, 'w') as f:
                json.dump({'name': self.name, 
                           'annotations': self.annotations, 
                           'images': self.images,
                           'class_dict': class_dict,
                            'labels_per_class': labels
                           }, f, indent=4)
            return True
        else:
            # load the config file
            with open(self.config_file, 'r+') as f:
                data = json.load(f)
                for arg in data:
                    setattr(self, arg, data[arg])

                print(data)
            print(f'{self.directory} already exists, attempting to load config file...')
            return False
    def copy_images(self):
        '''
        copy the images to the project folder
        '''
        print(f'Copying images from {self.images} to {self.directory}')
        if not os.path.exists(f'{self.directory}/images'):
            shutil.copytree(self.images, f'{self.directory}/images')
            self.images = f'{self.directory}/images'
        else:
            print(f'Images already exist in {self.directory}')
    def copy_annotations(self):
        '''
        copy the annotations file to the project folder
        '''
        print(f'Copying {self.annotations} to {self.directory}')
        name = self.annotations.split('/')[-1]
        if not os.path.isfile(f'{self.directory}/{name}'):
            shutil.copy(self.annotations,f'{self.directory}/{name}')
            self.annotations = f'{self.directory}/{name}'
        else:
            print(f'Annotations file {self.annotations} already exists in {self.directory}')
    def check_annotations_exists(self) -> None:
        '''
        check to see if the given annoations and image directory exist, and if so, copy the annotation file to the experiment folder
        '''
        if not os.path.exists(self.annotations) or not os.path.isfile(self.annotations):
            print(f'Error: {self.annotations} does not exist, please check the path and try again, program exiting')
            
        else:
            print(f'Found annotations file {self.annotations}')
            self.copy_annotations()
        # check if the given images directory exists

    def check_images_exist(self):
        '''
        check to see if the given image directory exists
        '''
        if not os.path.exists(self.images) or not os.path.isdir(self.images):
            print(f'Error: {self.images} does not exist, please check the path and try again, program exiting')
            sys.exit()
        else:
            print(f'Found image directory {self.images}')
        # check if the images have already been resized
        if os.path.exists(f"{self.name}/resized_images"):
            num_images = len(os.listdir(f"{self.directory}/resized_images"))
            print(f'Found folder with {num_images} resized images')
            self.images = f'{self.directory}/resized_images'


    def combine_datasets(self, annotation_file2)-> None:
        '''
        Reads two JSON annotation files and merges them with consistent class IDs and names.

        '''
        print("starting")
    
        with open(self.annotations, 'r') as f:
            data1 = json.load(f)
        with open(annotation_file2, 'r') as f:
            data2 = json.load(f)

        class_dict1 = {category['id']: category['name'] for category in data1['categories']}
        class_dict2 = {category['id']: category['name'] for category in data2['categories']}

        all_classes = set(class_dict1.values()).union(set(class_dict2.values()))
    
        class_to_new_id = {name: i for i, name in enumerate(all_classes)}

        def update_annotations(annotations, class_dict) -> list:
            for annotation in annotations:
                class_name = class_dict.get(annotation['category_id'])
                if class_name in class_to_new_id:
                    annotation['category_id'] = class_to_new_id[class_name]
            return annotations

        data1['annotations'] = update_annotations(data1['annotations'], class_dict1)
        data2['annotations'] = update_annotations(data2['annotations'], class_dict2)

        new_categories = [{"id": id, "name": name} for name, id in class_to_new_id.items()]

        combined_annotations = data1['annotations'] + data2['annotations']
        combined_images = data1['images'] + data2['images']

        combined_data = {
            'images': combined_images,
            'annotations': combined_annotations,
            'categories': new_categories
        }

        image_dict = {}

        # add file_name key to annotations, the cvat export didn't have them
        for i in combined_data['images']:
            # another issue with the cvat export, the file_name is the full path so we need to split it
            i['file_name'] = i['file_name'].split('/')[-1]
            if i['id'] not in image_dict:
                image_dict[i['id']] = i['file_name']
        for a in combined_data['annotations']:
            if not 'file_name' in a:
                a['file_name'] = image_dict[a['image_id']]


        file_name = f'{self.directory}/{self.name}_combined.json'
        with open(file_name, 'w') as f:
            json.dump(combined_data, f, indent=4)
        print(f"Combined annotations saved to {file_name}")
        class_dict = get_class_dict(file_name,False)
        os.makedirs(f'{self.directory}/figures', exist_ok=True)
        labels=labels_per_class(f"{self.directory}/figures",file_name)
        self.update_config(annotations=file_name,class_dict=class_dict,labels_per_class=labels,combined_with=annotation_file2,original_annotations=self.annotations)
        self.annotations = file_name
        self.class_dict = class_dict
        self.labels_per_class = labels

    def update_config(self,**kwargs)-> None:
        '''
        Updates the config file for the project.
        '''
        with open(f'{self.directory}/config.json', 'r+') as f:
            data = json.load(f)
            for arg in kwargs:
                data[arg] = kwargs[arg]
                self.arg = kwargs[arg]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
       
        print(f'Updated config file for {self.name}')

    def resize_images(self, target_width)-> None:
            '''
            Resizes all images in a given directory to the target width while maintaining aspect ratio.
            '''
            output_dir = f'{self.directory}/resized_images'
            fn = Path(output_dir) 
            fn.mkdir(parents=True, exist_ok=True)
            images = os.listdir(self.images)
            i = 0
            print('resizing images:')
            for filename in images:
                sys.stdout.write(f'\r {i}/{len(images)}')
                i += 1
                image = cv2.imread(os.path.join(self.images,filename))
                height, width, _ = image.shape
                aspect_ratio = width / height
        
                # Calculate the new height based on the target width and aspect ratio
                target_height = int(target_width / aspect_ratio)
                if target_width >= width:
                    print(f'Image: {filename} is already the same size or smaller than the target width of {target_width}')
                    # move the image to the output directory
                    shutil.move(os.path.join(self.images,filename), output_dir)
                    continue
                image = cv2.resize(image, (int(target_width),int(target_height)), interpolation=cv2.INTER_AREA)
                cv2.imwrite(os.path.join(output_dir,filename), image)
            self.update_config(annotaions = self.annotations, images = output_dir)
            self.images = output_dir

    def add_filename_key(self,annotation) -> None:
        '''
        Adds filename key to annotations file if missing
        '''
        image_dict = {}
        with open(annotation, 'r') as f:
            data = json.load(f)
        for i in data['images']:
            image_dict[i['id']] = i['file_name']
        for a in data['annotations']:
            if not 'file_name' in a:
                a['file_name'] = image_dict[a['image_id']]
        with open(annotation, 'w') as f:
            json.dump(data, f, indent=4)

    def remove_classes(self,classes_to_remove) -> None:
        """
        Remove classes from annotations file remaps class ids, and creates a yaml file for yolo training
        :param classes_to_remove: List of classes to remove
        """
        output_file = f'{self.directory}/{self.name}_removed.json'
        with open(self.annotations, 'r') as f:
            annotations = json.load(f)
                
        class_dict = {}

        for i in  annotations['categories']:
            class_dict[i['id']] = i['name']
        
        print("Classes to remove:")
        print(class_dict)

        for i in classes_to_remove:
            
            print(class_dict[i])

        annotations['annotations'] = [c for c in annotations['annotations'] if c['category_id'] not in classes_to_remove]
        annotations['categories'] = [c for c in annotations['categories'] if c['id'] not in classes_to_remove]

        class_dict.clear()
        # get new class dict
        for i in  annotations['categories']:
            class_dict[i['id']] = i['name']


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
        class_dict = get_class_dict(output_file,False)
        label_dict = labels_per_class(f"{self.directory}/figures",output_file)
        self.update_config(annotations = output_file,class_dict=class_dict,labels_per_class=label_dict)
        self.annotations = output_file
        self.class_dict = class_dict
        print(f"Annotations saved to {output_file}")
        os.makedirs(f'{self.directory}/figures', exist_ok=True)
        with open(f'{self.directory}/figures/{self.name}_class_dict.json', 'w') as f:
            json.dump(class_dict, f, indent=4)

    def remap_classes_to_zero_index(self,annotation_file,overwrite)->dict:
        '''
        given a coco json annotation file, remaps the class_id's to 0 indexed and fixes missing class_id's.
        returns a dictionary of class_id's and class_names
        
        '''
        with open(annotation_file, 'r') as f:
            data = json.load(f)

        class_dict = self.get_class_dict(annotation_file, False)

        class_to_new_id = {class_name: new_id for new_id, class_name in enumerate(class_dict.values())}
        #print(class_to_new_id)
        for category in data['categories']:
            category['id'] = class_to_new_id[category['name']]

        for annotation in data['annotations']:
        
            original_class_name = class_dict[annotation['category_id']]
            annotation['category_id'] = class_to_new_id[original_class_name]    
        file_name = f'{self.directory}/{annotation_file}'
        if not os.path.exists(file_name):
            self.write_json_file(data, file_name)
        else:
            if overwrite:
                os.remove(file_name)
                self.write_json_file(data, file_name)
            else:
                file_name = file_name.split('.', 1)[0] + '_remapped.json'
                self.write_json_file(data, file_name)
        return class_to_new_id
    
    def write_json_file(data, file_name):
        '''
        writes a json file to the given file name
        '''
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def augment_classes(self,augmentations):
        '''
        Augments images based on the number of augmentations specified in the augmentations dictionary.
        '''
        with open(self.annotations, "r") as f:
            data = json.load(f)

        annotations = data["annotations"]
        updated_annotations = []
        annotations_length = len(annotations)
        print(f'Annotations Length: {annotations_length}')
        
        image_template = {
            "file_name": "",
            "height": 4104,
            "width": 7296,
            "id": 2020120011100728
        }

        def augment_and_save_image(image, file_name, output_folder, version):
            # Save the augmented image in the same folder as the original image
            new_file_name = f"{os.path.splitext(file_name)[0]}_{version}.jpg"
            output_path = os.path.join(output_folder, new_file_name)
            os.makedirs(output_folder, exist_ok=True)
            if os.path.exists(output_path):
                print('File already exists')
            else: 
                # Define your augmentation pipeline using Albumentations
                transform = A.Compose([
                    # Add your desired transformations here
                    #A.RandomBrightnessContrast(p=0.25),
                    A.MedianBlur(p=0.25),
                    #A.RandomFog(p=0.1),
                    A.RandomSnow(p=0.2),
                    A.RandomShadow(p=0.2),
                    A.RandomRain(p=0.2),
                ])
                # Apply the transformations to the image
                augmented_image = transform(image=image)["image"]
                cv2.imwrite(output_path, augmented_image)
                #print(f"Augmented image saved as: {output_path}")
            return new_file_name
        
        for annotation in annotations:
            if annotation["category_id"] in augmentations:
                #print(annotation["category_id"])
                file_name = annotation["file_name"]
                image_path = os.path.join(self.images, file_name)
                image = cv2.imread(image_path)

                if image is not None:
                    file_name = f'{annotation["file_name"]}_augmented'
                    for i in range(augmentations[annotation["category_id"]]):
                        # Moved the new_annotation creation here
                        new_annotation = copy.copy(annotation)

                        new_id = int(''.join(random.choices(string.digits, k=16)))
                        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                        version = res
                        new_file_name = augment_and_save_image(image, file_name, self.images, version)

                        new_annotation['file_name'] = new_file_name
                        new_annotation['image_id'] = new_id
                        annotations_length += 1
                        new_annotation['id'] = new_id
                        updated_annotations.append(new_annotation)
                        #print(f'Total new annotations: {len(updated_annotations)}')
                        new_image = copy.copy(image_template)
                        new_image['file_name'] = new_file_name
                        new_image['id'] = new_id
                        data["images"].append(new_image)
            else:
                updated_annotations.append(annotation)
                    
        data["annotations"] += updated_annotations
        
        print(len(data["annotations"]))

        updated_annotations_file = os.path.splitext(self.annotations)[0] + "_updated.json"
       
        with open(updated_annotations_file, "w") as f:
            json.dump(data, f, indent=4)
        self.annotations = updated_annotations_file
        self.update_config(annotations=updated_annotations_file, class_dict=class_dict)
        print(f'Annotations saved to {updated_annotations_file}')
        class_dict = get_class_dict(updated_annotations_file,False)
        self.class_dict = class_dict
        self.annotations = updated_annotations_file
        os.makedirs(f'{self.directory}/figures', exist_ok=True)
        with open(f'{self.directory}/figures/{self.name}_class_dict.json', 'w') as f:
            json.dump(class_dict, f, indent=4)
    
    def data_yaml_file(self):
        '''
        Creates a data.yaml file for use with YOLOv5 and v8.
        '''
        with open(self.annotations, 'r') as f:
            data = json.load(f)
        with open(f"{self.directory}/data/data.yaml","w") as f:
            f.write("train: train/images\n")
            f.write("test: test/images \n")
            f.write("val: val/images\n")
            f.write(f"nc: {len(self.class_dict)}\n")
            f.write(f"names: {list(self.class_dict.values())}")
        print(f'Created data.yaml file for {self.name}')

    def to_yolo(self):
        '''
        Converts COCO annotations to YOLO format, compatible with v5 and v8.
        '''
        counter = 0
    
        with open(self.annotations) as f:
            fn = Path(self.directory) / 'labels'   # folder name
            fn.mkdir(exist_ok=True, parents=True)  # make folder
        
            data = json.load(f)
            print('Number of images:', len(data['images']))
            print('Number of annotations:', len(data['annotations']))
            print(f'Converting {self.annotations}...')

            # Create image dict
            #images = {x['id']: x for x in data['images']}
            images = {}
            for x in data['images']:
                
                if x['id'] not in images:
                    images[x['id']] = x
                else:
                    counter += 1
                    #sys.stdout.write(f'\r {counter} duplicate images found')
                    

            # Create image-annotations dict
            imgToAnns = defaultdict(list)
            ann_counter = 0
            for ann in data['annotations']:
                ann_counter += 1
                imgToAnns[ann['image_id']].append(ann)
        
            print(f'Number of duplicate images: {counter}')
            print(f'annotations length: {len(imgToAnns)}')
            # Write labels file
            for img_id, anns in imgToAnns.items():
                img = images[img_id]
                h, w, f = img['height'], img['width'], img['file_name']
                # if fixed_size:
                #     h = int(height)
                #     w = int(width)

                bboxes = []
                for ann in anns:
                    
                    # The COCO box format is [top left x, top left y, width, height]
                    box = np.array(ann['bbox'], dtype=np.float64)
                    box[:2] += box[2:] / 2  # xy top-left corner to center
                    box[[0, 2]] /= w  # normalize x
                    box[[1, 3]] /= h  # normalize y
                    if box[2] <= 0 or box[3] <= 0:  # if w <= 0 and h <= 0
                        continue

                    cls = ann['category_id']
                    box = [cls] + box.tolist()
                    if box not in bboxes:
                        bboxes.append(box)
                
                # Write
                with open((fn / f).with_suffix('.txt'), 'a') as file:
                    #print(f, w, h, file=file)  # filename width height # no need to write this, messes up the training parser
                    for i in range(len(bboxes)):
                        line = *(bboxes[i]),  # cls, box or segments
                        file.write(('%g ' * len(line)).rstrip() % line + '\n')
        
   
    def split_indices(self,x, train, test, validate):
        '''
        splits the indices of the data into train, test, and validation sets.
        '''
        n = len(x)
        v = np.arange(n)
        i = round(n * train)  # train
        j = round(n * test) + i  # test
        k = round(n * validate) + j  # validate
        return v[:i], v[i:j], v[j:k]  # return indices
    
    def split_data(self, train, test, validate,seed):
        '''
        Splits the data into train, test, and validation sets and moves the images to the proper data sets.
        provide the ratios of train test and validate in decimal percentage.
        provide a seed for the random shuffle for reproducibility (optional).
        '''
        output_dir = f'{self.directory}/data'
        files = os.listdir(self.directory + '/labels')
        if files == []:
            print('No label files found, please check the path and try again')
            sys.exit()
        
        print(len(files))
        if seed == None:
            seed = 42
        random.Random(seed).shuffle(files)
        self.update_config(annotations=self.annotations, images=self.images, seed=seed)
        i, j, k = self.split_indices(files, train, test, validate)
        datasets = {'train': i, 'test': j, 'val': k}
        print('train: ',len(datasets['train']),'test: ',len(datasets['test']), 'val: ', len(datasets['val']))
        for dataset in datasets:
            make_dirs(f'{output_dir}/{dataset}')
            directory = f'{output_dir}/{dataset}/labels'
            for index in datasets[dataset]:
                image_name = files[index].split('.')[0] + '.' + 'jpg'
                shutil.copy(f'{self.images}/{image_name}', f'{output_dir}/{dataset}/images')
                shutil.copy(f'{self.directory}/labels/{files[index]}', directory)
        print('done')
        for keys in datasets:
            counts = self.output_num_labels(f'{output_dir}/{keys}/labels')
            self.bar_graph(counts, output_dir, keys)
            print(keys, counts)
            
        self.data_yaml_file()
    
    def output_num_labels(self,file_dir):
        """
        outputs the number of labels per class in data set.
        """
        files = os.listdir(file_dir)
        label_dict = {}
        for file in files:
            
            with open(f'{file_dir}/{file}', 'r') as f:
                lines = [line.rstrip('\n').split() for line in f]
                for line in lines:
                    if(len(line) == 0) or len(line[0]) > 2:
                        continue
                    if int(line[0]) not in label_dict:
                        label_dict[int(line[0])] = 1
                    else:
                        label_dict[int(line[0])] += 1
        return label_dict
    def bar_graph(self,label_dict, file_path, dataset_name):
    
        labels, values = zip(*sorted(label_dict.items()))
        indexes = np.arange(len(labels))
        width = .8
        plt.bar(indexes, values, width)
        plt.xticks(indexes , labels)
        plt.xlabel('labels')
        plt.ylabel('number of labels')
        plt.title('number of labels per class')
        os.makedirs(f'{file_path}/figures', exist_ok=True)
        plt.savefig(f'{file_path}/figures/{dataset_name}.png')
        plt.close()

    def load_annotation_file(self,annotation_file):
        if not os.path.exists(annotation_file):
            print(f'Did not find {annotation_file}')
        else:
            self.remap_classes_zero_index(annotation_file)
            self.add_filename_key(annotation_file)
    def get_class_dict(self,annotation_file,write:bool)->dict:
        '''
        reads a json annotation file and returns a dictionary of class_id's and class_names
        optionally writes the dictionary to a json file with the name <annotation_file>.json
        '''
        class_dict = {}
        with open(annotation_file, 'r') as f:
            data = json.load(f)
        for i in  data['categories']:
            class_dict[i['id']] = i['name']
        #print(class_dict)
        #split file name and extension
        if write:
            annotation_file = annotation_file.split('/',1)[-1]
            annotation_file = annotation_file.split('.',1)[0]
            annotation_file +='_dict.json'
            with open(annotation_file, 'w') as f:
                json.dump(class_dict, f, indent=4)
            print(f'Class dict written to {annotation_file}')
        return class_dict