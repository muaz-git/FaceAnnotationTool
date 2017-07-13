import cv2
data_folder = './lfw/'

noFacesListFilename = data_folder + 'imagesList.txt'
def loadAnnotatonFile():
    with open(noFacesListFilename) as f:
        elemList = f.read().splitlines()
    return elemList, len(elemList)
elemList, _ = loadAnnotatonFile()
imgIdx = 0
countFaces1 = 0
countFaces2 = 0
countFaces3 = 0
face_cascade1 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
face_cascade2 = cv2.CascadeClassifier(
    '/home/hiwiraum/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
face_cascade3 = cv2.CascadeClassifier(
    '/home/hiwiraum/opencv-3.1.0/data/haarcascades_cuda/haarcascade_frontalface_default.xml')


while True:
    imgDetailList = elemList[imgIdx].split()
    print 'reading ' + imgDetailList[1]
    img = cv2.imread(data_folder+imgDetailList[0]+'/'+imgDetailList[1])

    faces1 = face_cascade1.detectMultiScale(img, 1.3, 5)
    faces2 = face_cascade2.detectMultiScale(img, 1.3, 5)
    faces3 = face_cascade3.detectMultiScale(img, 1.3, 5)
    if len(faces1) > 0:
        countFaces1 += 1
    if len(faces2) > 0:
        countFaces2 += 1
    if len(faces3) > 0:
        countFaces3 += 1

    # if totalFaces > 0:
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    imgIdx+=1
    if imgIdx >= len(elemList):
        break

print 'Total Images ', len(elemList)
print 'Found using 1 = ', countFaces1
print 'Found using 2 = ', countFaces2
print 'Found using 3 = ', countFaces3

# noFacesImagesList.txt
# Total Images  888
# Found using 1 =  6
# Found using 2 =  6
# Found using 3 =  360
# diff = 528

# Total Images  13611
# Found using 1 =  12722
# Found using 2 =  12722
# Found using 3 =  12919
# diff = 692