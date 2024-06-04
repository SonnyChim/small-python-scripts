import cv2 as cv
import numpy as np
def ordered_dithering(input_image):
    bayer_pattern = np.array([[  0, 128,  32, 160],
                              [192,  64, 224,  96],
                              [ 48, 176,  16, 144],
                              [240, 112, 208,  80]],dtype=np.uint8)
    if np.array(input_image.shape).shape == (3,):
        greyscale_image = np.mean(input_image,2)
    else:
        greyscale_image = input_image
    bayer_image = np.tile(bayer_pattern,(input_image.shape[0]//4+1,input_image.shape[1]//4+1))[0:greyscale_image.shape[0],0:greyscale_image.shape[1]]
    output_image = np.where(greyscale_image <= bayer_image,0 ,255).astype(np.uint8)
    return output_image
characters = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# img = np.full((700,300,3),0,dtype=np.uint8)
# cv.putText(img,"fweiweiwge",(50,40),cv.FONT_ITALIC,0.5,(255,255,255))
# cv.imshow("daw",img)
# cv.waitKey()
# raise SystemExit
imge = cv.VideoCapture(0)
choose = True
choose = False
import time
_, orig_img = imge.read()
print(orig_img.shape)
fps = [0 for _ in range(20)]
while choose:
    last_time = time.perf_counter()
    _, orig_img = imge.read()
    # cv.imshow("input",orig_img)
    imgout = ordered_dithering(orig_img)
    cv.imshow("out",imgout)
    if cv.waitKey(1) == ord("q"):
        break
    fps.insert(0,1/(time.perf_counter()-last_time))
    fps.pop()
    print(np.average(fps),fps[0])

scaling = 2
areasize = 12//scaling
while not choose:
    _, orig_img = imge.read()
    # cv.imshow("input",orig_img)
    values = np.full((orig_img.shape[0]//areasize),"",dtype=object)
    imgout = np.full((orig_img.shape[0]*scaling,orig_img.shape[1]*scaling,3),255,dtype=np.uint8)
    for y in range(orig_img.shape[0]//areasize):
        letters = ""
        for x in range(orig_img.shape[1]//areasize):
            # print(np.floor(np.mean(orig_img[y*areasize:y*areasize+areasize,x*areasize:x*areasize+areasize])/255*70))
            letters += characters[np.floor(np.mean(orig_img[y*areasize:y*areasize+areasize,x*areasize:x*areasize+areasize])/255*69).astype(int)]
        values[y] = letters
    for y,row in enumerate(values):
        for x,val in enumerate(row):
            cv.putText(imgout,str(val),(x*12,y*12+12),cv.FONT_ITALIC,0.5,(0,0,0))
    cv.imshow("out",imgout)
    if cv.waitKey(1) == ord("q"):
        break