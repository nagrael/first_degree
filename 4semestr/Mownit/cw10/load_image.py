import os
from collections import Counter
import numpy as np
from skimage import io, img_as_float
from skimage.feature import peak_local_max, corner_fast, corner_peaks
from skimage.restoration import *
from skimage.transform import (hough_line, hough_line_peaks,
                               rotate)
from skimage.util import random_noise
import matplotlib.pyplot as plt
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import string

def generate_text(text, width,height, font, size):
    font = ImageFont.truetype(font,size)
    img=Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    x = int(0.2*size)
    for tex in text:
        draw.text((0, x),tex,font=font,fill="black")
        x += size + int(0.2*size)
        draw = ImageDraw.Draw(img)
    img.save("a_test.png")


def sample_gen(fonts,size):
    font = ImageFont.truetype(fonts+".ttf",size)

    os.makedirs("sample/"+fonts, exist_ok=True)
    os.makedirs("sample/"+fonts+"/"+str(size), exist_ok=True)
    for tex in string.ascii_lowercase:
        #print(tex,fonts)
        img=Image.new("RGB", (size+10,size+10), "black")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0),tex,font=font,fill="white")
        draw = ImageDraw.Draw(img)
        x = "sample/"+fonts+"/"+str(size)+"/"+tex+".png"
        img.save(x,"PNG")
    for tex in string.digits:
        #print(tex,fonts)
        img=Image.new("RGB", (size+10,size+10), "black")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0),tex,font=font,fill="white")
        draw = ImageDraw.Draw(img)
        x = "sample/"+fonts+"/"+str(size)+"/"+tex+".png"
        img.save(x,"PNG")
    pre = [".",",","!","?"]
    for tex in pre:
        #print(tex,fonts)
        img=Image.new("RGB", (size+1,size+1), "black")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0),tex,font=font,fill="white")
        draw = ImageDraw.Draw(img)
        if tex == "?":
            tex = "question"
        x = "sample/"+fonts+"/"+str(size)+"/"+tex+".png"
        img.save(x,"PNG")

def cut(fonts,size):

    for name1 in os.listdir('./sample/' + fonts+"/"+size):
        if os.path.isfile('./sample/' + fonts+"/"+size+"/"+name1):
            nam = './sample/' + fonts+"/"+size+"/"+name1
            #print(name1)
            image = img_as_float(io.imread(nam, as_grey=True))
            row = np.array([np.mean(a) for a in image]) > 0
            col = np.array([np.mean(a) for a in image.T]) > 0
            min1 = min2 = max1 = max2 = 0
            flag = True
            for x in range(len(row)-1):
                if row[x] and flag:
                    min1 = x
                    max1 = min1
                    flag = False
                if ~row[x+1] and row[x] :
                    max1 = x+1
            if max1 == min1:
                max1 = image.shape[0]

            flag =True
            for x in range(len(col)-1):
                if col[x] and flag:
                    min2 = x
                    max2 = min2
                    flag = False
                if ~col[x+1] and col[x]:
                    max2 = x+1
            if max2 == min2:
                max2 = image.shape[1]
            if min1<0:
                min1 =0
            if min2<0:
                min2=0
            io.imsave(nam, image[min1:max1,min2:max2])
if __name__ == "__main__":
    generate_text(["ala ma kota, a kot ma ale ","niekonieczna koniecznosc bycia! ","teoretyczny spokuj ducha? ",
                   "alfabet aby czy lacinkis?! ","1000 albo i 999. ","1 2 3 4 5 6 7 8 9 albo i 11 "]
                  , 500, 250, "times.ttf",35)
