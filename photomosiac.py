from PIL import Image
import os
from math import sqrt
from pathlib import Path

def split_image(img, height, width):
    imgwidth, imgheight = img.size
    rows = imgheight // height
    cols = imgwidth // width
    squares = []

    for i in range(rows):
        for j in range(cols):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            squares.append(img.crop(box))
    return squares

def calculate_average_color(img):
    data = img.getdata()
    avg_red, avg_green, avg_blue = 0, 0, 0
    data_len = len(data)
    for j in range(data_len):
        avg_red += data[j][0]
        avg_green += data[j][1]
        avg_blue += data[j][2]
    return (avg_red // data_len, avg_green // data_len, avg_blue // data_len)

def pixellate(avg_colors, image, height, width, square_size):
    print(len(avg_colors))
    data = image.getdata()
    print(len(data))
        
    im = Image.new(image.mode, image.size)
    #for i in range(height):
    #    for j in range(width):
    #        im.putpixel((i, j), avg_colors[j % len(avg_colors)])
    im.putdata(avg_colors)

    im.show()

def crop_center(im, crop_width, crop_height):
    # https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
    im_width, im_height = im.size
    return im.crop(((im_width - crop_width) // 2,
                    (im_height - crop_height) // 2,
                    (im_width + crop_width) // 2,
                    (im_height + crop_height) // 2))

def crop_max_square(im):
    # https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
    return crop_center(im, min(im.size), min(im.size))

def crop_photos(original_img_path):
    source_dir_path = '/Users/aelk/Code/photomosaics/cropped_source_images/' 
    source_dir = Path(source_dir_path)
    if not source_dir.is_dir():
        os.mkdir(source_dir)

    file_name_base = 'cropped_img'
    count = 0
    for filename in os.listdir(original_img_path):
        im = Image.open(original_img_path + filename)
        im = crop_max_square(im)
        im.save(source_dir_path + file_name_base + str(count), "JPEG")
        count += 1
    return source_dir_path

def get_average_colors_source_images(image_path):
    source_avg_colors = []
    for filename in os.listdir(image_path):
        im = Image.open(image_path + filename)
        source_avg_colors.append(calculate_average_color(im))
    return source_avg_colors

def euclidian_distance(color1, color2):
    dist = 0
    for i in range(len(color1)):
        dist += ((color2[i] - color1[i]) ** 2)
    return sqrt(dist)

if __name__ == '__main__':
    img = Image.open('monkey.jpg')
    height, width = img.size
    square_size = 50
    squares = split_image(img, square_size, square_size)
    # http://vision.stanford.edu/aditya86/ImageNetDogs/
    image_path = 'new_images/'

    square_avg_colors = [calculate_average_color(s) for s in squares]
    #pixellate(avg_colors, img, height, width, square_size)
    cropped_path = crop_photos(image_path)
    source_avg_colors = get_average_colors_source_images(cropped_path)
    
