from PIL import Image
import os
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

def calculate_average_colors(squares):
    average_colors = []
    for i in range(len(squares)):
        im = squares[i].getdata()
        #print("squares[i].getdata()=", im)
        #print("len of squares[i].getdata()=", len(im))
        avg_red, avg_green, avg_blue = 0, 0, 0
        im_len = len(im)
        for j in range(im_len):
            avg_red += im[j][0]
            avg_green += im[j][1]
            avg_blue += im[j][2]
        average_colors.append( \
            (avg_red // im_len, avg_green // im_len, avg_blue // im_len) \
        )
    return average_colors

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

if __name__ == '__main__':
    img = Image.open('monkey.jpg')
    height, width = img.size
    square_size = 50
    squares = split_image(img, square_size, square_size)
    # http://vision.stanford.edu/aditya86/ImageNetDogs/
    image_path = 'Images/n02086240-Shih-Tzu/'

    avg_colors = calculate_average_colors(squares)
    #pixellate(avg_colors, img, height, width, square_size)
    crop_photos(image_path)
