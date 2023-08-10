# Collection of all our training data and Data augmnetation code

```
conda create -n <env_name> python=3.8
conda activate <env_name>
pip install -r requirements.txt
```

## Data Augmentation Scripts
### resize.py:
   - Resizes all images in a directory to a specified size
   - Usage: `python resize.py --image_dir <path_to_directory> --output_dir <image utput directory> --width <width> --height <height>`

### coco2yolo.py

 - Converts COCO annotations to YOLO format
- Usage: `python coco2yolo.py --json_dir <path_to_directory_with_json> --use_segments <True/False optional> ---cls91to80 <True/False optional> --fixed_size <True/False> --width <width> --height <height>`
 -  The fixed_size arg is to be used if you want the annotations converted to a fixed image size. If you want the annotations to be converted to the original image size, set fixed_size to False, or don't use the arg at all. It defaults to false. If set to true, specify the --width and --height args.