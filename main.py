from PIL import Image,ImageDraw
import cv2
import numpy as np

fileName = "papillon.mp4"
asciiChars = ".-*+\oO#&%89@ "
asciiList = list(asciiChars)
asciiLen = len(asciiList)

ratio = 0.08
frameRate = 30
asciiWidth = 10
asciiHeight = 10

def getAsciiChar(i):
    return asciiList[int(asciiLen - i * asciiLen / 256 - 1)]

def resizeImage(img):
    img = Image.fromarray(img)
    width,height = img.size
    img = img.resize((int(ratio * width), int(ratio * height)), Image.NEAREST)
    return (img)

def fillAscii(d, pixel, height, width):
    for i in range(height):
        for j in range(width):
            r,g,b=pixel[j,i]
            index = int((r + g + b) / 3) #using the average of r,g,b as brightness index
            d.text((j * asciiWidth, i * asciiHeight), getAsciiChar(index), fill=(r,g,b))

cap = cv2.VideoCapture(fileName)
imgArray = []
success,img = cap.read()

while success:
    
    img = resizeImage(img)
    width,height = img.size
    n = Image.new("RGB", (asciiWidth * width, asciiHeight * height), color = (0,0,0)) #creating image with black background
    d = ImageDraw.Draw(n)
    pixel = img.load()

    fillAscii(d, pixel, height, width)

    result = np.array(n)
    imgArray.append(result)

    success,img = cap.read()

cap.release()

height, width, layers = imgArray[0].shape
size = (width,height)

out = cv2.VideoWriter('result.avi',cv2.VideoWriter_fourcc(*'XVID'), frameRate, size)

for i in range(len(imgArray)):
    out.write(imgArray[i])

out.release()