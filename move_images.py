
import os

def move_images(dir,output_folder):
    images=os.listdir(dir)
    for image in images:
        try:
            os.system(f"mv {dir}/{image} {output_folder}")
        except:
            print(f"Error moving {image}")
        


wheel1 = ['2024-1-1','2024-1-3','2024-1-6','2024-1-7','2024-1-8','2024-1-9','2024-1-12']
wheel2 = ['2023-10-14','2023-10-15','2023-10-07','2023-08-29','2023-09-11','2023-09-18','2023-09-23','2023-09-24','2023-09-05']
wheel3 = ['2024-1-1','2024-1-2','2024-1-5','2024-1-6','2024-1-7','2024-1-8','2024-1-9']

wheel1_dir = '/home/bucket-mounts/1'
wheel2_dir   = '/home/bucket-mounts/2'
wheel3_dir = '/home/bucket-mounts/3'

dir1 = [f"{wheel1_dir}/{i}" for i in wheel1]
dir2 = [f"{wheel2_dir}/{i}" for i in wheel2]
dir3 = [f"{wheel3_dir}/{i}" for i in wheel3]

output_folder = '/home/bucket-mounts/annotated_images'

for i in dir1:
    move_images(i,output_folder)
for i in dir2:
    move_images(i,output_folder)
for i in dir3:
    move_images(i,output_folder)