# Collection of all our training data prep code

Contents:

- [Collection of all our training data prep code](#collection-of-all-our-training-data-prep-code)
- [Basic workflow for dataset creation](#basic-workflow-for-dataset-creation)
- [The Dataset Builder Class](#the-dataset-builder-class)
- [What the cli does](#what-the-cli-does)
- [A note on Image sets](#a-note-on-image-sets)
- [Copying the dataset to the VM from a bucket](#copying-the-dataset-to-the-vm-from-a-bucket)
- [Be mindful of memory usage](#be-mindful-of-memory-usage)
  - [Data Augmentation Scripts](#data-augmentation-scripts)
    - [coco2yolo.py](#coco2yolopy)
    - [auto\_map\_classes.py](#auto_map_classespy)
    - [remove\_classes.py](#remove_classespy)
    - [augment\_classes.py](#augment_classespy)
    - [combine\_datasets.py](#combine_datasetspy)
    - [split\_data.py](#split_datapy)
    - [resize.py](#resizepy)
- [Uploading the Data to the VM](#uploading-the-data-to-the-vm)
  - [Uploading the dataset](#uploading-the-dataset)
  - [Uploading to a bucket and downloading to the VM](#uploading-to-a-bucket-and-downloading-to-the-vm)
- [Training yolov5](#training-yolov5)
- [Misc. scripts](#misc-scripts)

If working on the VM, make sure to activate the yolo environment
```
conda activate yolo
```
If you're working on a different machine, you'll need to create a new environment and install the requirements
```
conda create -n <env_name> 
conda activate <env_name>
cd <path_to_this_project>
pip install -r requirements.txt
```
# Basic workflow for dataset creation
- Create an `images` directory, and put all of your images there.
   - If your image directory contains nested folders, use the flatten_image_dirs.sh script to flatten the directory [A note on Image sets](#a-note-on-image-sets).
- Create an `annotations` directory, and put all of your annotations there.

  - If these are new annotations from CVAT, make sure they are 0 indexed. If not using the [main.py](#what-the-cli-does) cli, or the [dataset builder](#the-dataset-builder-class) class, Use the auto_map_classes.py script to do this. See [Data Augmentation Scripts](#data-augmentation-scripts).

- Add your annotations to the annotations directory.
If the `experiments` directory doesn't exist, create it.

The [main.py](#what-the-cli-does) cli works as an interface for the dataset_builder class.Once you have your images and annotations in the correct directories, you can use the cli to create a new project, or add to an existing project.
The simplest thing to do, is run ```python main.py``` in the terminal.
You will be guided through generating your dataset.

# The Dataset Builder Class
The dataset_builder.py file contains the dataset_builder class, which is the main class for creating and modifying datasets. There is a bit too much to cover here, but main things to know are:
- The dataset_builder class is initialized with a name, a coco json annotation file, and a directory of images.
- You can combine other datasets 
- Remove classes
- Augment images 
- Convert annotations to yolo format
- Split the dataset into train, test, and val sets
  


# What the cli does
- Creates a dataset_builder class instance
- Given the name of an existing project, the config file is loaded and the dataset_builder is initialized with the project's config
- Given a new project name, creates a new project directory under the experiments directory with the name you provide
- Creates and maintains a config file for the project

- *The config file*:
     - The config file is like the state management and history of your project, it keeps track of the images and annotations you've added to the dataset, and the data augmentation operations you've performed, and allows you to pick up where you left off, or make changes to the dataset.
      - The config file is a json file, and is created in the project directory when you create a new project.
      - You can manually edit the config file BEFORE you run the cli, but it's best to let the cli handle it.
 
# A note on Image sets
Sometimes, the datasets exported from CVAT have nested folders, and we need all our images in one directory to work with the scripts here. Edit the flatten_image_dirs.sh script to quickly flatten a folder of images that contains nested folders. Make sure to edit the script to point to the correct directory. Then run the script
```
./flatten_image_dirs.sh
```
If you get a permissions error, run 
```
chmod +x flatten_image_dirs.sh
```
Another small hiccup, ensure all the images have the same extension. Some of our older datasets have a capitalized .JPG, modify and use the change_file_extension.sh script for this.This is also a handy template for making other changes to file names, so keep it in mind.
```
./change_file_extension.sh
```
 Same deal with the permissions
```
chmod +x change_file_extension.sh
```
# Copying the dataset to the VM from a bucket
```
gsutil cp gs://<bucket_name>/<file_name>.zip 
```

# Be mindful of memory usage
 Once you have a dataset, and you've perfomed your training, move the dataset off the VM. It's okay to keep the main set of images, since the cli will copy the files into your experiment directory, but, the VM has limited memory. We have storage buckets in GCP, so use them. To move a dataset to a bucket, zip the whole dataset directory, and upload it to a bucket with gsutil, then delete the dataset from the VM. You can always download it again later.To use gsutil:

 zip the dataset directory
 ```
 zip -r <new_name> <data_dir>
 ```
 
 copy the zip file to a bucket
  ```
  gsutil cp <file_name>.zip gs://<bucket_name>
  ```
  remove the dataset from the VM
  ```
  rm -r <data_dir>
  ```

## Data Augmentation Scripts
There are a host of data augmentations scripts in the utility_scripts directory. If you want to perform single operations on a dataset, look there. Here's a list of some of the available scripts.
Always check the script for defaults and usage! There is no undo button!
### coco2yolo.py

 - Converts COCO annotations to YOLO format
- Usage: `python coco2yolo.py --dir <directory to save annoations> --annotation_file <json annotations file> `


### auto_map_classes.py
- given a coco json annotation file, remaps the class_id's to 0 indexed and fixes missing class_id's.
- returns a dictionary of class_id's and class_names
    outputs a data.yaml file for use with yolov5 and v8 with the class name list and number of classes
- Usage: `python auto_map_classes.py --annotations_path <path to annotations> --write <boolean to write the class dictionary to a file> `
### remove_classes.py
- Removes all instances of specified classes from a COCO JSON annotation file
- Usage:`python remove_classes.py --annotations_path <path to annotations> --output_file <path to output annotations> --classes <list of classes to remove sperated by space 1 2 3 etc. >`

### augment_classes.py
- Augments images of given category ID's
  and adds specified number of annotations to those new augmented images. 
- Please see the script for defaults and usage
- Usage:`python augment_classes.py --annotations_path <path_to_annotations> --image_folder <path_to_original_images> --output_folder <path_to_new_augmented_images> --augment_categories <string list of id's and number of augmentations to add to each id '0,2 1,3' etc.> `

### combine_datasets.py
- given two json annotation files, combines them, creating consistent class_id's and a single annotation file.
- Usage: `python combine_datassets.py --annotations1 <path_to_annotations1> --annotations2 <path_to_annotations2>`

### split_data.py
- Splits a dataset into train, val and test sets
- outputs files ready for YOLO training under datasets directory in specified output directory
- Also outputs bar graphs of class distribution in each set
- Usage: `python split_data.py --file_dir <path_to_yolo_labels_directory> --output_dir <path_to_output_dir> --images <path_to_images> --image_type <jpg/png>`
- Check the script for defaults

### resize.py
- Resizes all images in a directory to a specified size, default is 640 width
- Usage: `python resize.py --image_dir <path_to_images> --output_dir <path_to_output_dir> --target_width <width>`

# Uploading the Data to the VM

If you didn't use the main.py cli to generate your dataset, make sure to check some things before you proceed.

Make sure that you have a data.yaml file in your data directory with the correct number of classes and the class names list, use the data.yaml in the data directory as a template

 The order of the classes in the class name list matters, the index of each class name needs to correspond to the category_id in the annotations. For example, if the first class in the list is "person", then the category_id for all the person annotations needs to be 0. The second class in the list needs to have the category_id 1, and so on.

 The paths to the directories in the data.yaml need to be checked as well, if you attempt to train and receive an error about the path to the train, val, or test directory, check the path in the data.yaml file and make sure it is correct.

  ## Uploading the dataset
  If you're triaing on a different machine, it's best to zip your dataset.
 - Go ahead and zip your new data directory
  ```
  zip -r <new_name> <data_dir>
  ```

 ## Uploading to a bucket and downloading to the VM
   - Upload the zip file to a bucket in GCP (you can use the web interface or gsutil)

   - with gsutil
   ```
   gsutil cp <file_name>.zip gs://<bucket_name>
   ```
   - On the VM, download the zip file using gsutil
   ```
   gsutil cp gs://<bucket_name>/<file_name>.zip 
   ```
   
   - Unzip the file
   ```
   unzip <file_name>.zip
   ```
   - You should now have all the data unzipped and ready to train
 

 # Training yolov5
 The Vm is already set up with a virtual environment and the yolov5 project. Once logged into the machine, navigate to the yolov5 directory

 once the dataset is uploaded, you can train
 
``` 
cd yolov5
```
And activate the virtual environment
```
conda activate yolo
```
You can now train with your new dataset
```
python train.py --weights yolov5s.pt --epochs <num_epochs> --data <your_data_dir>/data.yaml
```
-See the Ultralytics [yolov5](https://github.com/ultralytics/yolov5) github for more info on training


# Misc. scripts
   There are a number of utility scripts in the utility_scripts directory to help with data auditing and other things

   - count_annotations.py :
       - Counts the number of annotations in a coco json file
   and repeat images, good to check if any augmentation created duplicate images
    
   - count_images.py :
       - counts the number of images in a directory
   - count_img_in_ann.py :
      - counts the number of images in a json annotation file
   - count_labels.py:
      - counts the number of label files in a directory
   - draw_boxes.py
       - draw bounding boxes on an image provided a label file and image
   - format_json.py:
       - makes a json file more readable
   - labels_per_class.py
       - outputs a graph of number of labels per class in an annotation file
   - get_class_dict.py
       - outputs a dictionary of class names and their corresponding category_id from a json annotation file
