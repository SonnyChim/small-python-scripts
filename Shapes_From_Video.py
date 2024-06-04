import cv2 as cv
import numpy as np
import time

groupsizerectangles = 5
groupsizetriangles = 0
groupsizecircles = 0
groupsizetotal = groupsizerectangles + groupsizetriangles + groupsizecircles
grouptop = 20
children = groupsizetotal//grouptop
targetshapes = 300
targetdiff = 0

def randrectnumbers():
    x1 = np.random.randint(0,imgx-1)
    x2 = np.random.randint(x1+1,imgx)
    y1 = np.random.randint(0,imgy-1)
    y2 = np.random.randint(y1+1,imgy)
    return np.array([x1,x2,y1,y2])

def randtrinumbers():
    x1 = np.random.randint(0,imgx)
    x2 = np.random.randint(0,imgx)
    x3 = np.random.randint(0,imgx)
    y1 = np.random.randint(0,imgy)
    y2 = np.random.randint(0,imgy)
    y3 = np.random.randint(0,imgy)
    return np.array([[x1,y1],[x2,y2],[x3,y3]],dtype=np.int32)

def randcirnumbers():
    x = np.random.randint(0,imgx)
    y = np.random.randint(0,imgy)
    r = np.random.randint(0,np.maximum(imgx,imgy))
    return np.array([x,y,r])

def drawrect(img,values):
    cv.rectangle(img,(int(values[0]),int(values[2])),(int(values[1]),int(values[3])),(int(values[4]),int(values[5]),int(values[6])),-1)

def drawtri(img,values):
    cv.fillPoly(img,[np.array([[values[0],values[1]],[values[2],values[3]],[values[4],values[5]]],dtype=np.int32)],(values[6],values[7],values[8]))

def drawcir(img,values):
    cv.circle(img,(int(values[0]),int(values[1])),int(values[2]),(values[3],values[4],values[5]),-1)

def gen0(img,diffold):
    groupval = np.zeros((groupsizetotal,9))
    groupdiff = np.zeros(groupsizetotal)
    shape = np.empty(groupsizetotal,dtype=str)
    for i in range(groupsizerectangles):
        geoimg = img.copy()
        coords = randrectnumbers()
        values = np.append(coords,np.mean(orig_img[coords[2]:coords[3]+1,coords[0]:coords[1]+1],axis = (0,1)))
        shapediffbefore = np.sum(np.abs(np.subtract(orig_img[coords[2]:coords[3]+1,coords[0]:coords[1]+1],geoimg[coords[2]:coords[3]+1,coords[0]:coords[1]+1],dtype = np.int16)))
        drawrect(geoimg,values)
        shapediffafter = np.sum(np.abs(np.subtract(orig_img[coords[2]:coords[3]+1,coords[0]:coords[1]+1],geoimg[coords[2]:coords[3]+1,coords[0]:coords[1]+1],dtype = np.int16)))
        diff = diffold - shapediffbefore + shapediffafter
        groupval[i] = np.append(values,[0,0])
        groupdiff[i] = diff
        shape[i] = "r"
    for i in range(groupsizetriangles):
        geoimg = img.copy()
        mask = np.zeros((imgy, imgx, 3),dtype=np.uint8)
        coords = randtrinumbers()
        cv.fillPoly(mask,[coords],(1,1,1))
        values = np.append(coords,np.sum(orig_img*mask,axis = (0,1))/np.count_nonzero(mask)*3)
        drawtri(geoimg,values)
        diff = np.sum(np.abs(np.subtract(orig_img,geoimg,dtype = np.int16)))
        groupval[i+groupsizerectangles] = values
        groupdiff[i+groupsizerectangles] = diff
        shape[i+groupsizerectangles] = "t"
    for i in range(groupsizecircles):
        geoimg = img.copy()
        mask = np.zeros((imgy, imgx, 3),dtype=np.uint8)
        coords = randcirnumbers()
        cv.circle(mask,(coords[0],coords[1]),coords[2],(1,1,1),-1)
        values = np.append(coords,np.sum(orig_img*mask,axis = (0,1))/np.count_nonzero(mask)*3)
        drawcir(geoimg,values)
        diff = np.sum(np.abs(np.subtract(orig_img,geoimg,dtype = np.int16)))
        groupval[i+groupsizerectangles+groupsizetriangles] = np.append(values,[0,0,0])
        groupdiff[i+groupsizerectangles+groupsizetriangles] = diff
        shape[i+groupsizerectangles+groupsizetriangles] = "c"
    return groupval,groupdiff,shape

def evolve(img,diffold):
    a,b,c = gen0(img,diffold)
    arr1inds = b.argsort()
    return a[arr1inds][0],b[arr1inds][0],c[arr1inds][0]
    

def createshape(diffold, timeold):
    while True:
        values,diff,shape = evolve(imgout,diffold)
        if diff<diffold or (time.perf_counter_ns() >= timeold):
            if shape == "r":
                drawrect(imgout,values)
            if shape == "t":
                drawtri(imgout,values)
            if shape == "c":
                drawcir(imgout,values)
            diffold = np.sum(np.abs(np.subtract(orig_img,imgout,dtype = np.int16)))
            print(f"difference: {diffold/(imgx*imgy*3)}")
            return diffold,time.perf_counter_ns()+500_000_000
        

def generateimage():
    global orig_img
    diffold = np.sum(np.abs(np.subtract(orig_img,imgout,dtype = np.int16)))
    shapes = 0
    timeold = 0
    while True:
        _, orig_img = imge.read()
        cv.imshow("input",orig_img)
        diffold, timeold = createshape(diffold, timeold)
        shapes += 1
        cv.imshow("out",imgout)
        cv.imshow("difference",np.abs(np.subtract(orig_img,imgout,dtype = np.int16)).astype(np.uint8))
        if cv.waitKey(1) == ord("q"):
            break
    print(f"{shapes} shapes")


imge = cv.VideoCapture(0)
_, orig_img = imge.read()
imgy = orig_img.shape[0]
imgx = orig_img.shape[1]
imgout = np.zeros((imgy, imgx, 3),dtype=np.uint8)
start = time.perf_counter_ns()
generateimage()
end = time.perf_counter_ns()
