import os
from collections import Counter
from load_image import sample_gen ,cut
import numpy as np
from skimage import io, img_as_float
from skimage.color import rgb2gray
from skimage.feature import corner_fast, corner_peaks, peak_local_max
from skimage.measure import find_contours
from skimage.restoration import *
from skimage.transform import (hough_line, hough_line_peaks,
                               rotate)
from skimage.util import random_noise


class OCR:
    def __init__(self, img: str):
        self.image = (io.imread(img, as_grey=True))
        self.orginal = [a[:] for a in self.image]
        self.lines = 0
        self.h = 0
        self.min = 0
        self.sp = 0
        self.mid_line = []
        self.box = []
        self.space = []
        self.letters =[]
        self.result = []
    def __rotate__(self, rot, cval):
        self.image = rotate(self.image, rot, True, cval=cval,preserve_range=True,order=3)

    def __noise__(self):
        self.image = random_noise(self.image)

    def __param__(self):
        x = [max([b[2] - b[0] for b in a])for a in self.box]
        y = [min([b[2] - b[0] for b in a])for a in self.box]
        z = [np.mean([a[b+1][1] - a[b][3] for b in range(len(a)-1)if a[b+1][1] - a[b][3]>2])for a in self.box]
        self.sp = int((np.mean(z)-1))
        self.h = int(max(x)-2)
        self.min = int(min(y)-2)

    def denoise(self):
        self.image = denoise_nl_means(self.image, multichannel=False)

    def space_place(self):
        for r in self.box:
            tmp =[]
            for t in range(len(r)-1):
                if r[t+1][1]-r[t][3]>=self.sp:
                    z = int((r[t+1][1]-r[t][3])//(self.sp))
                    for i in range(z):
                        tmp.append(t+1)
            self.space.append(tmp)

    def in_box(self,point):
        for i in range(len(self.box)):
            for j in range(len(self.box[i])):
                if self.box[i][j][0]<=point[0]<self.box[i][j][2] and self.box[i][j][1]<point[1]<=self.box[i][j][3]:
                    return (True,i,j)
        return (False,)


    def to_text(self,fonts):
        for h in range(self.h-1,self.h+5):
            self.letter_boxs()
            sample_gen(fonts,h)
            cut(fonts,str(h))
            for name in os.listdir('./sample/' + fonts+"/"+str(h)):
                if os.path.isfile('./sample/' + fonts+"/"+str(h)+"/"+name):
                    nam = './sample/' + fonts+"/"+str(h)+"/"+name
                    char = name[:-4]
                    if name =="question.png":
                        char = "?"
                    elif char in ["l","1"]:
                        amax = 0.98
                    elif char =="i":
                        amax = 0.95
                    elif char =="!":
                        amax = 1
                    elif char in ["g","j"]:
                        amax = 0.93
                    else:
                        amax = 0.91

                    img = img_as_float(rgb2gray(io.imread(nam, as_grey=True)))
                    if char in [".",","]:
                        if self.min == img.shape[1]:
                            poi = []
                            for x in range(len(self.box)):
                                for y in range(len(self.box[x])):
                                    if (self.box[x][y][2] - self.box[x][y][0]-2) == self.min:
                                        poi.append((x,y))
                            for x,y in poi:
                                if (self.box[x][y][3] - self.box[x][y][1]-2) == self.min and char ==".":
                                    self.letters[x][y].append((char,0.95))
                                elif 2*self.min<=(self.box[x][y][3] - self.box[x][y][1]-2) <= 3*self.min and char==",":
                                    self.letters[x][y].append((char,0.95))
                        continue
                    #img = np.pad(img,((1,1),(1,1)),"constant")
                    C=np.real(np.fft.ifft2(np.fft.fft2(self.image)*np.fft.fft2(np.rot90(img,2),s=self.image.shape)))
                    y = np.amax(C)
                    C= C/y
                    C = np.array([[0 if b<amax else (b) for b in a]for a in C])
                    ij = (peak_local_max(C,min_distance=2))
                    for a in ij:

                        t = self.in_box(a)

                        if t[0]:
                            self.letters[t[1]][t[2]].append((char,C[a[0]][a[1]]))


            s=""
            for z in range(len(self.letters)):

                for d in range(len(self.letters[z])):
                    if d in self.space[z]:
                        s+=" "
                    try:
                        s += max(self.letters[z][d],key=lambda e:e[1])[0]
                    except ValueError :
                        s+="#"
                s+="\n"
            self.result.append((h,s))

    def cut_image(self, prec:float = 0.01):
        x = (corner_peaks(corner_fast(self.image, 9), min_distance=1))
        min1 = min(x,key=lambda q:q[0])[0] - int(prec*self.image.shape[0])
        max1 = max(x,key=lambda q:q[0])[0] + int(prec*self.image.shape[0])
        min2 = min(x,key=lambda q:q[1])[1] - int(prec*self.image.shape[1])
        max2 = max(x,key=lambda q:q[1])[1] + int(prec*self.image.shape[1])

        self.image = self.image[min1:max1,min2:max2]

    def rotate(self):
        noisy_image = self.image > np.mean(self.image)
        h, theta, d = hough_line(noisy_image)
        a, b, c = hough_line_peaks(h, theta, d)
        b = Counter(b)
        self.__rotate__(270 + (np.rad2deg(b.most_common(1)[0][0])), 0)

    def count_lines(self):

        ava_list = np.array([np.mean(a) for a in self.image[0:int(self.image.shape[1]),:]]) < \
                   0.7*np.mean(self.image[0:int(self.image.shape[1]),:])

        i = x = y = k = 0

        while i < len(ava_list):
            flag = False
            l = 0
            if ava_list[i]:
                x = i
                l= 1
                flag = True
            while i < len(ava_list)-1 and (ava_list[i] or ava_list[i+l]):
                i += 1
                k += 1
            if flag and k > 3:
                y = i-1
                diffe = x + np.floor((y - x) / 2)

                self.mid_line.append((x, y, diffe))
                self.lines += 1
            i += 1
            k = 0
        self.mid_line.append((len(ava_list)-1,len(ava_list)-1,len(ava_list)-1))


    def boxed(self,img,cval:float=0.3):
        tmp = []
        for i in find_contours(img,cval):
            maxr = np.ceil(max(i,key=lambda e: e[0])[0])+1
            maxc = np.ceil(max(i,key=lambda e: e[1])[1])+1
            minr = np.ceil(min(i,key=lambda e: e[0])[0])-1
            minc = np.ceil(min(i,key=lambda e: e[1])[1])-1
            tmp.append((minr,minc,maxr,maxc))
        for l in range(len(tmp)):
            flag = True
            for i in range((len(tmp))):
                if i != l:
                    if tmp[l][0]>=tmp[i][0] and tmp[l][1]>=tmp[i][1] and tmp[l][2]<=tmp[i][2] and tmp[l][3]<=tmp[i][3]:
                        flag = False
            if flag:
                self.box.append(tmp[l])


        #self.box = sorted(self.box,key=lambda e:(e[1],e[0]))
    def sorted_box(self):
        r_lines = []
        for li in range(len(self.mid_line)-1):
            tmp = []
            for a,b,c,d in self.box:
                if self.mid_line[li][2]<c<self.mid_line[li+1][2] or self.mid_line[li][2]<a<self.mid_line[li+1][2]:
                    tmp.append((a,b,c,d))
            tmp = sorted(tmp,key=lambda e:(e[1],e[0]))

            r_lines.append(tmp)
        for t in r_lines:
            to_del = []
            for i in range(len(t)-1):
                w1 = t[i][3] - t[i][1]
                w2 = t[i+1][3] - t[i+1][1]
                if w1<w2 and (t[i+1][3]>=t[i][3] and t[i+1][1]<=t[i][1]):
                    if t[i][0] <= t[i+1][0]:# and t[i][3]<=t[i+1][0]:
                        m = t[i+1][2]
                        n = t[i][0]
                    else:
                        m = t[i][2]
                        n = t[i+1][0]
                    t[i] = (n,t[i+1][1],m,t[i+1][3])
                    to_del.append(t[i+1])
                if w1>=w2 and (t[i+1][3]<=t[i][3] and t[i+1][1]>=t[i][1]):

                    if t[i][0] <= t[i+1][0]:# and t[i][3]<=t[i+1][0]:
                        m = t[i+1][2]
                        n = t[i][0]
                    else:
                        m = t[i][2]
                        n = t[i+1][0]
                    t[i] = (n, t[i][1], m, t[i][3])
                    to_del.append(t[i+1])
            for to in to_del:

                try:
                    t.remove(to)
                except ValueError:
                    pass
        self.box = r_lines


    def letter_boxs(self):
        self.letters = []
        for r in self.box:
            tmp=[]
            for y in r:
                tmp.append([])
            self.letters.append(tmp)




    def prepare(self, denoise:bool=True, resize:bool=True):
        if denoise:
            self.denoise()
        self.image = 1- self.image
        self.rotate()
        if resize:
            self.cut_image()
        self.count_lines()

        self.boxed(self.image)
        self.sorted_box()

        self.__param__()
        self.space_place()
        #self.image = 1- self.image

    def noise_rot(self,noise:bool=True):
        self.__rotate__(11.3,1)
        if noise:
            self.__noise__()
