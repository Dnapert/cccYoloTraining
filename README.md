# Collection of all our training data and Data augmentation code

```
conda create -n <env_name> python=3.8
conda activate <env_name>
cd <path_to_this_repo>
pip install -r requirements.txt
```

## Data Augmentation Scripts

### export_training_dataset.py
- Removes all instances of specified classes from a COCO annotation file
- Converts COCO annotations to YOLO format
- Augments images of given category ID's
- Splits a dataset into train, val and test sets
- Ouputs files ready for YOLO training under datasets directory in specified output directory
- Also outputs bar graphs of class distribution in each set
- Usage: Place images in data directory under images folder and annotations in data directory
- `python export_training_dataset.py --remove <list of class ID's to remove seperated by spaces ex 1 2 3 --augment <list of class ID's to augment seperated by spaces ex 1 2 3> `
### resize.py:
   - Resizes all images in a directory to a specified size
   - Usage: `python resize.py --image_dir <path_to_directory> --output_dir <image output directory> --width <width> --height <height>`

### coco2yolo.py

 - Converts COCO annotations to YOLO format
- Usage: `python coco2yolo.py --json_dir <path_to_directory_with_json> --use_segments <True/False optional> ---cls91to80 <True/False optional> --fixed_size <True/False> --width <width> --height <height>`
 -  The fixed_size arg is to be used if you want the annotations converted to a fixed image size. If you want the annotations to be converted to the original image size, don't use the arg, it defaults to false. If set to true, specify the --width and --height args.
  
### remove_classes.py
- Removes all instances of specified classes from a COCO annotation file
- Usage:`python remove_classes.py --annotations_path <path_to_annotations> --output_file <path_to_output_annotations.json> --classes <list of classes to remove sperated by space 1 2 3 etc. >`

### augment_classes.py
- Augments images of category IDs 0, 3, 6, 8 and adds annotations to those new augmented images
- Usage:`python augment_classes.py <path_to_annotations> <path_to_original_images> <path_to_new_augmented_images>`

### split_data.py
- Splits a dataset into train, val and test sets
- outputs files ready for YOLO training under datasets directory in specified output directory
- Also outputs bar graphs of class distribution in each set
- Usage: `python split_data.py --file_dir <path_to_yolo_labels_directory> --output_dir <path_to_output_dir> --images <path_to_images> --image_type <jpg/png>`
- Check the script for defaults
# Training on the yolo_training VM on GCP


### After you have your data converted, you should have a directory named split_data.
- Make sure that you have a data.yaml file in your split_data directory with the correct number of classes and the class names list, use the data.yaml in the data directory as a template
 - Go ahead and zip this directory for uploading to the vm
  ```
  zip -r <new_name> split_data/
  ```
  - once uploaded to the vm, move your zip file to the yolov5 directory and unzip it
  ```
  mv <file_name>.zip ~/yolov5
  cd yolov5
  unzip <file_name>.zip
  ```
 - You should now have the directory with all the data unzipped and ready to train

 
### The Vm is already set up with a virtual environment and the yolov5 project. Once logged into the machine, navigate to the yolov5 directory
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