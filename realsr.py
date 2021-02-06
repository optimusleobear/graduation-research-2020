import subprocess
import os
import cv2
from shutil import copy


def realsr(img_file, os_type, gpu_number):
    linux_folder = 'realsr-linux/'
    macos_folder = 'realsr-macos/'
    gpu = '-g ' + str(gpu_number)

    target_folder = None
    if os_type == 'macos':
        target_folder = macos_folder
    else:
        target_folder = linux_folder

    # copy original file to reasr folder
    true_file_name = img_file.split('/')[-1]
    ori_path = img_file.rsplit('/', 1)[0]
    print('>>> ' + true_file_name)
    copy(img_file, target_folder)

    # RealSR cncc Vulkan
    os.chdir(target_folder)
    # Denoise
    image = cv2.imread(true_file_name)
    # image_blur = cv2.GaussianBlur(image, (3, 3), 0)
    image_denoise = cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 7, 21)
    cv2.imwrite('image_denoise.jpg', image_denoise)
    # RealSR process
    output_file = true_file_name.split('.')[0] + '_hires.jpg'
    command = '! ./realsr-ncnn-vulkan -i image_denoise.jpg -o ' + output_file + ' -s 4 -x -m models-DF2K ' + gpu
    subprocess.call(command, shell=True)
    os.remove('image_denoise.jpg')
    os.chdir('..')

    # copy hires picture to original path
    hires_file = target_folder + output_file
    copy(hires_file, ori_path)

    # delete cache file
    os.remove(target_folder + true_file_name)
    os.remove(target_folder + output_file)

    print('RealSR finished.')
