import os

def count_images():
    # Count number of images in folder
    image_dir = 'data/resized_images'
    image_files = os.listdir(image_dir)
    print(f'Number of images: {len(image_files)}')
    return len(image_files) 
count_images()