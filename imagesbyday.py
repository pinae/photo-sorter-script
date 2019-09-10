image_folder = "/home/pina/Bilder/20190906-Toskana/"
output_folder = "/home/pina/Bilder/20190906-Toskana-by-day/"

from exif import Image
from datetime import datetime
import os
import sys
import shutil
import re
filename_regex = r"(?P<filename>.*)\.(?P<extension>JPG|jpg|jpeg|PNG|png|tiff|tif|TIF|BMP|bmp)"

# Count the images for the progress bar
image_count = 0
for subfolder in os.listdir(image_folder):
    for image in os.listdir(os.path.join(image_folder, subfolder)):
        filename_matches = re.finditer(filename_regex, image, re.UNICODE)
        filename, extension = None, None
        for match in filename_matches:
            filename, extension = match.groups()
        if not filename or not extension:
            continue
        image_count += 1

# Do the actual work
progressbar_width = 40
bar_str = "[%s]" % (" " * progressbar_width)
sys.stdout.write(bar_str)
sys.stdout.flush()
sys.stdout.write("\b" * len(bar_str))
copied_image_count = 0
for subfolder in os.listdir(image_folder):
    for image in os.listdir(os.path.join(image_folder, subfolder)):
        filename_matches = re.finditer(filename_regex, image, re.UNICODE)
        filename, extension = None, None
        for match in filename_matches:
            filename, extension = match.groups()
        if not filename or not extension:
            continue
        with open(os.path.join(image_folder, subfolder, image), 'rb') as file:
            image_obj = Image(file)
        if image_obj.has_exif:
            image_time = datetime.strptime(image_obj.datetime, "%Y:%m:%d %H:%M:%S")
        else:
            print("The file " + os.path.join(image_folder, subfolder, image) + "has no exif data.")
            image_time = os.path.getmtime(os.path.join(image_folder, subfolder, image))
        day_str = image_time.strftime("%Y_%m_%d-%A")
        if not os.path.exists(os.path.join(output_folder, day_str)):
            os.makedirs(os.path.join(output_folder, day_str))
        shutil.copy2(
            os.path.join(image_folder, subfolder, image),
            os.path.join(output_folder, day_str, image_time.strftime("%H%M%S_") + subfolder + "_" + filename + "." + extension.lower()))
        copied_image_count += 1
        progress = copied_image_count / image_count
        bar_str = "[%s] %d%%" % (
            "=" * int(progress*progressbar_width) + " " * (progressbar_width - int(progress*progressbar_width)),
            (progress * 100))
        sys.stdout.write(bar_str)
        sys.stdout.flush()
        sys.stdout.write("\b" * len(bar_str))
sys.stdout.write("\n")
