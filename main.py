import numpy as np
import cv2
#
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# create if not exist, make an index file which lists all the images in some order
# Iterate through all the images, resume from last saving state
# detect faces in an image
# display face and wait for an input, input can be face, no face, go back, close annotation process only if all faces of one file is annotated
# After each input file will be updated with label, in case of going back it updates last line, updated file only if all faces are shown
# annotation file format = Number of faces ImgFolder ImgName <x, y, w, h> <annotation>
# f : 1048678
# n : 1048686
# left arrow : 1113937
# right arrow : 1113939
# Esc : 1048603

import os
data_folder = './lfw/'
imagesListFilename = data_folder + 'imagesList.txt'
noFacesListFilename = data_folder + 'noFacesImagesList.txt'
annotationFilename = data_folder + 'annotation.txt'
face_cascade = cv2.CascadeClassifier('/home/hiwiraum/opencv-3.1.0/data/haarcascades_cuda/haarcascade_frontalface_default.xml')
face_cascade2 = cv2.CascadeClassifier('/home/hiwiraum/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
face_cascade3 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

# img = cv2.imread(data_folder+'Abdullah/Abdullah_0001.jpg')
# cv2.imshow('img', img)
# k = cv2.waitKey()
# print k
# exit()

def checkIfFileExist(fileName):
    try:
        open(fileName, 'r')
        return True
    except:
        return False

def createImagesList():
    fileObj = open(imagesListFilename, 'w')
    noFacesFileObj = open(noFacesListFilename, 'w')

    dirs = [d for d in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, d))]

    dirs.sort()
    for d, x in zip(dirs, range(len(dirs))):
        print 'reading ', d
        # if x > 10:
        #     fileObj.close()

        for _, _, files in os.walk(data_folder+d):
            files.sort()
            for f in files:
                img = cv2.imread(data_folder + d + '/' + f, 0)
                faces = face_cascade.detectMultiScale(img, 1.3, 5)
                totalFaces = len(faces)

                lineToWrite = d + ' ' + f # folderName <space> fileName
                if totalFaces > 0:
                    # if totalFaces > 1:
                    #     print ''
                    lineToWrite += ' '
                    for (x, y, w, h) in faces:
                        lineToWriteTmp = (lineToWrite + '.')[:-1]
                        lineToWriteTmp += str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
                        fileObj.write(lineToWriteTmp + '\n')
                else:
                    faces2 = face_cascade2.detectMultiScale(img, 1.3, 5)
                    faces3 = face_cascade3.detectMultiScale(img, 1.3, 5)

                    if len(faces2) == 0 and len(faces3) == 0 :
                        # fileObj.write(lineToWrite+'\n')
                        noFacesFileObj.write(lineToWrite+'\n')
                    else:
                        if len(faces2)>1:
                            faces = faces2
                        else:
                            faces = faces3
                        lineToWrite += ' '
                        for (x, y, w, h) in faces:
                            lineToWriteTmp = (lineToWrite + '.')[:-1]
                            lineToWriteTmp += str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
                            fileObj.write(lineToWriteTmp + '\n')

    fileObj.close()
    exit()

def createAnnotationFile():
    fileObj = open(annotationFilename, 'w')

    idxImgList = 0
    return fileObj, idxImgList

def loadAnnotatonFile():
    fileObj = open(annotationFilename, 'a')
    with open(annotationFilename) as f:
        elemList = f.read().splitlines()
    return fileObj, len(elemList)

def readImgList():
    with open(imagesListFilename) as f:
        imgList = f.read().splitlines()
    return imgList

def fetchImgs(imgDetailList):
    imgPath = data_folder + imgDetailList[0] + '/' + imgDetailList[1]
    img = cv2.imread(imgPath)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img#, gray

def keyAction(k):
    adv_idx = None
    label = None
    escFlag = False
    if k == 1048603: # code for Esc
        # print 'Escaped pressed. Saving annotation for current image and closing.'
        escFlag = True
    elif k == 1048678: # code for f = face
        # print 'f pressed. will fetch next image and mark current as face.'
        adv_idx = 1
        label = 1
    elif k == 1048686: # code for n = no face
        # print 'n pressed. will fetch next image and mark current as NO face.'
        adv_idx = 1
        label = 0
    elif k == 1113937: # code for left arrow in order to read the previous image again
        # print 'left arrow pressed. will fetch next image and mark current as NO face.'
        adv_idx = -1
    else:
        print 'press either f = face, n = no face, Esc to close, left arrow to go back'

    return adv_idx, label, escFlag

def handleFaces(imgDetail):
    # faces = face_cascade.detectMultiScale(img, 1.3, 5)
    # totalFaces = len(faces)  # can be zero, 1 or multiple
    # display box on each face, and ask weather it is a face or not
    containsFace = True
    try:
        imgDetail[2]
    except:
        containsFace = False
    displImg = fetchImgs(imgDetail)

    if containsFace:
        x, y, w, h = int(imgDetail[2]), int(imgDetail[3]), int(imgDetail[4]), int(imgDetail[5])
        cv2.rectangle(displImg, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        return 1, 0, False # return that view next image, and label on current image is zero, where escape was not pressed
    while True:
        cv2.imshow(imgDetail[1], displImg)
        key = cv2.waitKey(0)
        adv_idx, label, escFlag = keyAction(key)

        if escFlag or not(adv_idx==None)or not(label==None):
            cv2.destroyAllWindows()
            return adv_idx, label, escFlag

def deleteLastLineOfAnnotation():
    readFile = open(annotationFilename)
    lines = readFile.readlines()
    lines = lines[:-1]
    readFile.close()
    w = open(annotationFilename, 'w')
    w.writelines([item for item in lines])
    w.close()

# create ImageList file if it doesn't exist, in order to track annotated files
if not(checkIfFileExist(imagesListFilename)):
    createImagesList()

if checkIfFileExist(annotationFilename):
    # load the image which needs to be annotated, and provide file pointer to write
    # annotationFileObj = None
    annotationFileObj, imgListIdx = loadAnnotatonFile()
else:
    # load the first image to be annotated , and provide file pointer to write
    annotationFileObj, imgListIdx = createAnnotationFile()

imgList = readImgList()



while True:
    if imgListIdx >= len(imgList):
        break
    imgDetailList = imgList[imgListIdx].split()


    adv_idx, label, escFlag = handleFaces(imgDetailList)
    if escFlag:
        print '\nClosing...'
        break

    if adv_idx == -1:
        print 'need to remove last entry from annotation if there is.',imgListIdx
        annotationFileObj.close()
        deleteLastLineOfAnnotation()
        print imgListIdx
        annotationFileObj, imgListIdx = loadAnnotatonFile()

    else:
        lineToWrite = imgList[imgListIdx] + ' ' + str(label)
        annotationFileObj.write(lineToWrite + '\n')

        imgListIdx += adv_idx


annotationFileObj.close()
