import cv2
import albumentations as A

# Define the augmentation pipeline
transform = A.Compose([
    A.ToGray(p=1),  # Convert image to grayscale
    A.RandomBrightnessContrast(brightness_limit=(.2,.2), contrast_limit=(.7,.7), p=1),  # Adjust brightness and contrast
    #A.GaussNoise(var_limit=(5.0, 5.0), p=0.5),  # Add Gaussian noise
])

# Load your image
image = cv2.imread('data/resized_images/wpb_harriscreek_20201100_10300005.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

# Apply the transformation
augmented_image = transform(image=image)['image']

# Optionally save or visualize the augmented image
cv2.imwrite('night_vision_effect.jpg', cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
