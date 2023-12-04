# Collection of all our training data and Data augmentation code

Contents:

- [Collection of all our training data and Data augmentation code](#collection-of-all-our-training-data-and-data-augmentation-code)
- [Basic workflow for training](#basic-workflow-for-training)
  - [Data Augmentation Scripts](#data-augmentation-scripts)
  - [A note on image sets](#a-note-on-image-sets)
    - [coco2yolo.py](#coco2yolopy)
    - [remove\_classes.py](#remove_classespy)
    - [augment\_classes.py](#augment_classespy)
    - [split\_data.py](#split_datapy)
    - [resize.py](#resizepy)
- [Uploading the Data](#uploading-the-data)
- [HELP: I can't enter the yolov5 directory!](#help-i-cant-enter-the-yolov5-directory)
  - [Uploading the dataset](#uploading-the-dataset)
  - [Uploading directly to the VM](#uploading-directly-to-the-vm)
  - [Uploading to a bucket and downloading to the VM](#uploading-to-a-bucket-and-downloading-to-the-vm)
- [Training Yolov5](#training-yolov5)
- [Utility Scripts](#utility-scripts)
```
conda create -n <env_name> 
conda activate <env_name>
cd <path_to_this_project>
pip install -r requirements.txt
```
# Basic workflow for training
Create an images directory, and put all of your images there.
Add your annotations to the annotations directory, doesn't need to be here, but that's what I do.
The main.py cli app works as an interface for the dataset_builder.py module.
The simplest thing to do, is run ```python main.py``` in the terminal.
You will be guided through generating your dataset.
# A note on Image sets
Sometimes, the datasets exported from CVAT have nested folders, and we need all our images in one directory to work with the scripts here. Edit the flatten_image_dirs.sh script to quickly flatten a folder of images that contains nested folders. If you get a permissions error, run 
```
chmod +x flatten_image_dirs.sh
```
Another small hiccup, ensure all the images have the same extension. Some of our older datasets have a capitalized .JPG, modify and use the change_file_extension.sh script for this.This is also a handy template for making other changes to file names, so keep it in mind. Same deal with the permissions
```
chmod +x change_files_to_jpg.sh
```

## Data Augmentation Scripts
There are a host of data augmentations scripts in the utility_scripts directory. If you want to perdform single operations on a dataset, look there. Here's a list of some of the available scripts.
### coco2yolo.py

 - Converts COCO annotations to YOLO format
- Usage: `python coco2yolo.py --dir <directory to save annoations> --annotation_file <json annotations file> `

  
### remove_classes.py
- Removes all instances of specified classes from a COCO JSON annotation file
- Usage:`python remove_classes.py --annotations_path <path to annotations> --output_file <path to output annotations> --classes <list of classes to remove sperated by space 1 2 3 etc. >`

### augment_classes.py
- Augments images of given category ID's
  and adds specified number of annotations to those new augmented images. 
- Please see the script for defaults and usage
- Usage:`python augment_classes.py --annotations_path <path_to_annotations> --image_folder <path_to_original_images> --output_folder <path_to_new_augmented_images> --augment_categories <string list of id's and number of augmentations to add to each id '0,2 1,3' etc.> `

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


# Utility Scripts
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
   - remap_classes.py
       - remaps the category_id's in a json annotation file to be 0 indexed
       - also easily modified to remap to any index if you've removed classes from the dataset (it is necessary to have the category_id's be 0 indexed for training and not have missing indices)