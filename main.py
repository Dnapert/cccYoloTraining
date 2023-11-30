from dataset_builder import DatasetBuilder


new_dataset = DatasetBuilder(project_name='demo_2',annotations='annotations/11-13-combined.json',images='images/resized_images')


new_dataset.remove_classes([2,3,4,6,7,8,9,10,11,14])
new_dataset.to_yolo()
new_dataset.split_data(.8,.1,.1,12345)



