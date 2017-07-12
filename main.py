# import numpy as np
# import cv2
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# create if not exist, make an index file which lists all the images in some order
# Iterate through all the images, resume from last saving state
# detect faces in an image
# display face and wait for an input, input can be face, no face, go back, close annotation process only if all faces of one file is annotated
# After each input file will be updated with label, in case of going back it updates last line, updated file only if all faces are shown
# annotation file format, ImgListIdx ImgFolder ImgName <x, y, w, h> <annotation>

import os
data_folder = './lfw/'
imagesListFilename = data_folder + 'imagesList.txt'
annotationFilename = data_folder + 'annotation.txt'

def checkIfFileExist(fileName):
    try:
        open(fileName, 'r')
        return True
    except:
        return False

def createImagesList():
    fileObj = open(imagesListFilename, 'w')

    dirs = [d for d in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, d))]

    dirs.sort()
    for d in dirs:
        for _, _, files in os.walk(data_folder+d):
            files.sort()
            for f in files:
                lineToWrite = d + ' ' + f # folderName <space> fileName
                fileObj.write(lineToWrite+'\n')


    fileObj.close()

def createAnnotationFile():
    fileObj = open(annotationFilename, 'w')

    idxImgList = 0
    return fileObj, idxImgList

def readImgList():
    with open(imagesListFilename) as f:
        imgList = f.read().splitlines()
    return imgList

# create ImageList file if it doesn't exist, in order to track annotated files
if not(checkIfFileExist(imagesListFilename)):
    createImagesList()

if checkIfFileExist(annotationFilename):
    # load the image which needs to be annotated, and provide file pointer to write
    # annotationFileObj = None
    annotationFileObj, imgListIdx = createAnnotationFile()
else:
    # load the first image to be annotated , and provide file pointer to write
    annotationFileObj, imgListIdx = createAnnotationFile()

imgList = readImgList()
print imgList[imgListIdx].split()



annotationFileObj.close()
