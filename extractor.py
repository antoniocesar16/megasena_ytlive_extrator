import binascii
import cv2
import os,argparse, io
import pytesseract
import math
from PIL import Image
import numpy as np

RGBS = [{"RGB": (41, 38, 155), "game_name": "quina"}]

def get_text_images_path(path):
    """
        Extract text from images path
    """
    for i in os.listdir(path):
        image_location = path + "/" + i
        image_text = pytesseract.image_to_string(image_location, config=r'--oem 1 --psm 7 --dpi 70').strip()
        print(image_text)
        

def get_text_frame_cv2(frame) -> str:
        image_text = pytesseract.image_to_string(frame, config=r'--oem 1 --psm 7 --dpi 70')
        return image_text

def split_image(img):
    img = cv2.imread(img)
    img = img[825:1100]
    cv2.imwrite("./result.jpg", img) # save file in some path

def get_rgb(image_data):
    cv2.imwrite("./tmp.jpg", image_data)
    im = Image.open("./tmp.jpg")
    #im = Image.open(stream) 2265635207
    rgb = im.convert('RGB') # get three R G B values
    RGB = rgb.getpixel((1, 1))
    return RGB

def get_game_type(rgb1):
    """
    :type rgb: list 
    """
    for game in RGBS:
        game_name = game["game_name"]
        rgb2 = game["RGB"]
        if(euclidean_distance(rgb1, rgb2) < 5.0):
            return game_name
        
    return False

    
def euclidean_distance(color1, color2):
    """
    Distância euclidiana para calcular a distancia entre RGB1 e RGB2.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

image_text = pytesseract.image_to_string("./video-opencv/frame_.jpg", config=r'--oem 1 --psm 7 --dpi 70').strip()
print(image_text)