from PIL import Image

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

if __name__ == '__main__':
    img = Image.open('monkey.jpg')
    print(img.size)
    square_size = 50
    squares = split_image(img, square_size, square_size)

    avg_colors = calculate_average_colors(squares)
    print(len(avg_colors))
    print(avg_colors[2])
