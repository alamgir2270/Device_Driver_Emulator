import os

relative_path = '../art/IoE/SmartDevices/camera_image' + str(imageLoop) + '.png'
absolute_path = os.path.abspath(relative_path)
print("Image path is:", absolute_path)
