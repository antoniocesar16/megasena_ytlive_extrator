import binascii
import cv2
import os,argparse, io
import pytesseract
from PIL import Image
import numpy as np


def get_text_images_path(path):
    """
        Extract text from images path
    """
    for i in os.listdir(path):
        image_location = path + "/" + i
        image_text = pytesseract.image_to_string(image_location)
        print(image_text)
        

def get_text_frame_cv2(frame):
        image_text = pytesseract.image_to_string(frame, config='--oem 1 --psm 7 --dpi 70')
        return image_text

def split_image(img):
    img = cv2.imread(img)
    img = img[825:1100]
    cv2.imwrite("./result.jpg", img) # save file in some path

def get_rgb(image_data):
    cv2.imwrite("./tmp.jpg", image_data)
    im = Image.open("./tmp.jpg")
    #im = Image.open(stream)
    rgb = im.convert('RGB') # get three R G B values
    RGB = rgb.getpixel((1, 1))
    return RGB


#type = get_type("result.jpg")
#split_image('./video-opencv/frame2.jpg')
#text = get_text_frame_cv2('./video-opencv/frame.jpg')
#print(text)