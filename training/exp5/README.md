classes in this datset:

            0:"plastic_bag",
            1:"plastic_bottle",
            2:"plastic_cap",
            3:'plastic_container',
            4:"plastic_wrapper",
            5:"plastic_other",
            6:"foam_container",
            7:"Foam_other",
            8:"glass_bottle",

Train/val/test split: 0.8/0.1/0.1

100 epochs  
starting weights: yolov5s.pt

Labels:
<img src="training/exp5/../../labels.jpg" alt="labels.jpg"></img>

Augmented classes 0, 3, 6, 8 with 3, 3, 3, 5 images respectively.

The augmentation command used:
```
python augment_classes.py --annotations_path data/modified/modified.json --augment_categories '0,3 3,3 6,3 8,5' --image_folder data/resized_images --output_folder data/resized_images
```
    
    
* 0: 428
* 1: 2334
* 2: 1132
* 3: 156
* 4: 1086
* 5: 1838
* 6: 348
* 7: 3202
* 8: 85