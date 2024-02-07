from PIL import Image
from ultralytics import YOLO

model = YOLO('best.pt')
results = model('images/resized_images/20231011_080844_1_2_013930.jpg')  # results list
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image