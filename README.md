# Collection of all our training data and Data augmentation code

```
conda create -n <env_name> python=3.8
conda activate <env_name>
cd <path_to_this_repo>
pip install -r requirements.txt
```

## Data Augmentation Scripts
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
- outputs a file ready fot YOLO training under datasets directory in specified output directory
- Also outputs bar graphs of class distribution in each set
- Usage: `python split_data.py --file_dir <path_to_yolo_labels_directory> --output_dir <path_to_output_dir> --images <path_to_images> --image_type <jpg/png>`
- Check the script for defaults