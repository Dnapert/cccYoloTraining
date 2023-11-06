# Collection of all our training data and Data augmentation code

Contents:

- [Collection of all our training data and Data augmentation code](#collection-of-all-our-training-data-and-data-augmentation-code)
- [Basic workflow for training](#basic-workflow-for-training)
- [!! Important Notes, READ THIS !!](#-important-notes-read-this-)
  - [Data Augmentation Scripts](#data-augmentation-scripts)
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
- [Training](#training)
- [Creating this VM on GCP for training Yolov5](#creating-this-vm-on-gcp-for-training-yolov5)
- [Utility Scripts](#utility-scripts)
```
conda create -n <env_name> python=3.8
conda activate <env_name>
cd <path_to_this_project>
pip install -r requirements.txt
```
# Basic workflow for training
1. put all your images in a directory named images
2. remove any classes you don't want to train on from the annotations
3. resize all images to 640 width
4. optionally do any augmentation you want
5. convert the coco annotations to yolo format
6. split the data into train, val, and test sets
7. upload the data to the VM
8. train
   
# !! Important Notes, READ THIS !!
   - We train on 640x480 images, so before augmenting, make sure all images are that size. The resize.py script will do this for you. This also speeds up the augmentation process.
   - Look at the class_id's in any new json annotation file, sometimes when exporting an annotated dataset from CVAT, the class_id's will be 1 indexed. A quick way to check is to use the get_class_dict.py script, they need to be 0 indexed. If this is the case use the remap_classes.py script to remap the class_id's to be 0 indexed.
   - If you remove classes from the dataset, make sure to remap the class_id's to be 0 indexed, and have no missing indices,otherwise the training could fail.
   - The image names in the annotations should just be the name, not paths with slashes, i.e. /path/to/image.jpg, it should just be image.jpg. To remove leading slashes from the image names in the annotations, use the split_image_names.py script.
## Data Augmentation Scripts



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

# Uploading the Data

 After you have your data converted, you should have a directory named split_data.
- Make sure that you have a data.yaml file in your split_data directory with the correct number of classes and the class names list, use the data.yaml in the data directory as a template

 The order of the classes in the class name list matters, the index of each class name needs to correspond to the category_id in the annotations. For example, if the first class in the list is "person", then the category_id for all the person annotations needs to be 0. The second class in the list needs to have a category_id of 1, and so on.

 The paths to the directories in the data.yaml need to be checked as well, if you attempt to train and receive an error about the path to the train, val, or test directory, check the path in the data.yaml file and make sure it is correct.
# HELP: I can't enter the yolov5 directory!
   if a user cannot enter the yolov5 directory, i.e. the directory appears as a folder to a user, the owner (person who created the folder) needs to change the permissions of the directory to allow other users to enter it. This can be done with the following command:
   to allow a user to enter a directory:
   ```
   chmod o+rx <directory_name>
   ```
   if all else fails and you're tired of trying to figure out permissions, just re clone the yolov5 repo
   ```
   git clone https://github.com/ultralytics/yolov5.git
```
   
  ## Uploading the dataset
 - Go ahead and zip your new data directory for uploading to the vm
  ```
  zip -r <new_name> <data_dir>
  ```

   ## Uploading directly to the VM
   - once uploaded to the vm, move your zip file to the yolov5 directory and unzip it
   ```
   mv <file_name>.zip ~/yolov5
   cd yolov5
   unzip <file_name>.zip
   ```
 - You should now have the directory with all the data unzipped and ready to train
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
   - You should now have the directory inside the yolov5 directory with all the data unzipped and ready to train
 
 The Vm is already set up with a virtual environment and the yolov5 project. Once logged into the machine, navigate to the yolov5 directory

 # Training

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

# Creating this VM on GCP for training Yolov5

1. Go to the GCP dashboard and select compute engine
2. Select Create Instance
3. Give it a name
4. Select GPU's tab
   - under GPU type, select NVIDIA T4
   - Under number of GPUs, leave 1
   - Under Machine type, select n1-standard-8

![Alt text](<readme_images/Screenshot 2023-08-15 at 11.44.50 AM.png>)

4. When you scroll down, you will see a grey dialog box that reads "The current selected image requires you to install NVIDIA CUDA stack manually ...etc"
5. Click the switch image button
   
![Alt text](<readme_images/Screenshot 2023-08-15 at 11.45.07 AM.png>)

 - Operating system should be Deep Learning on Linux
 - Version Deep-Learning VM with CUDA 11.3 M110
 - Boot disk type SSD persistent
 - size 300GB
![Alt text](<readme_images/Screenshot 2023-08-15 at 11.45.45 AM.png>)

6. Click select

7. Create the instance
8. Once created, it should be listed under the VM's tab
9. Use the dropdown to connect via SSH in browser
    ![Alt text](<readme_images/Screenshot 2023-08-15 at 12.01.22 PM.png>)
10. After you connect you should have a command line 
11. Foollow the termina instructions and install the nvidia drivers
12. Next, install anaconda 
    ```
    curl -O https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

    ```
    ```
    bash Anaconda3-2020.11-Linux-x86_64.sh
    ```
   - You will have to hit enter and read through the TOS and agree, just follow the terminal prompts and use the default paths
   - When asked if you want to initalize anaconda, type yes
   - Conda should now be active , check by entering 
  ``` conda --version```

Optionally, install nano for easier text editing, you can use the built in vim editor if you want
```
 sudo apt install nano
```

13.  Next, clone the yolov5 repo
```
   git clone https://github.com/ultralytics/yolov5.git
```
14.  Create a virtual environment with conda
```
   conda create -n yolo python=3.8
```

- After a moment you will be asked to install a bunch of packages, enter y
15.   enter the yolov5 directory
```
    cd yolov5
```
16. modify the requirements.txt file
```
sudo nano requirements.txt
```
   - Comment out the torch and torchvision lines with a #
   - Save and exit (in nano its shift + o, enter, shift+x)
17. Activate the Virtual environment
```
conda activate yolo
```
18. Install dependencies
```
pip install -r requirements.txt
```
19. Now we need to install the correct versions of torch and torchvision. 
   ```
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
   ```
 20. Export the CUDA path (needs to be on one line in the terminal)
```
export PATH=/usr/local/cuda-11.0/bin${PATH:+:${PATH}}

```
Same here
```
export LD_LIBRARY_PATH=/usr/local/cuda-11.0/lib64/{LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
And thats it!

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