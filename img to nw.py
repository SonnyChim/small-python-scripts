import cv2 as cv
import numpy as np
greyscale = True
dither = True

binary = True
characters  = False
chunksize = 16
img = cv.imread("image.png")

if img is None:
    print("image not found")
    raise SystemExit

if dither:
    import dithering
    img = np.repeat(np.expand_dims(np.mean(img,2),2),3,2).astype(np.uint8)
    cv.imshow("image",img)
    img = dithering.floyd_steinberg(img,np.array(((0,0,0),(255,255,255))))
pixelsize = min(320//img.shape[1],222//img.shape[0])
cv.imshow("out",img)

if binary:
    if characters:
        out = f"from kandinsky import fill_rect,color\ndef l(input):\n  global y\n  for i in range({img.shape[1]//chunksize}):\n    binary = bin(ord(input[i]))\n    for x in range(len(binary)-2):\n      fill_rect((i*{chunksize}+x)*{pixelsize}+{(320-pixelsize*img.shape[1])//2},y*{pixelsize}+{(222-pixelsize*img.shape[0])//2},{pixelsize},{pixelsize},binary[-x-1]) \n  y += 1\ny = 0\nfill_rect(0,0,320,222,(0,0,0))\n"
    else:
        out = f"from kandinsky import fill_rect,color\ndef l(input):\n  global y\n  for i in range({img.shape[1]//chunksize}):\n    binary = bin(input[i])\n    for x in range(len(binary)-2):\n      fill_rect((i*{chunksize}+x)*{pixelsize}+{(320-pixelsize*img.shape[1])//2},y*{pixelsize}+{(222-pixelsize*img.shape[0])//2},{pixelsize},{pixelsize},binary[-x-1]) \n  y += 1\ny = 0\nfill_rect(0,0,320,222,(0,0,0))\n"
else:
    if greyscale:
        out = f"from kandinsky import fill_rect,color\ndef l(img):\n  global y\n  n = 0\n  for x in range({img.shape[1]}):\n    fill_rect(x*{pixelsize}+{(320-pixelsize*img.shape[1])//2},y*{pixelsize}+{(222-pixelsize*img.shape[0])//2},{pixelsize},{pixelsize},color(img[n],img[n],img[n]))\n    n += 1\n  y += 1\ny = 0\nfill_rect(0,0,320,222,(0,0,0))\n"
    else:
        out = f"from kandinsky import fill_rect,color\ndef l(img):\n  global y\n  n = 0\n  for x in range({img.shape[1]}):\n    fill_rect(x*{pixelsize}+{(320-pixelsize*img.shape[1])//2},y*{pixelsize}+{(222-pixelsize*img.shape[0])//2},{pixelsize},{pixelsize},color(img[n],img[n+1],img[n+2]))\n    n += 3\n  y += 1\ny = 0\nfill_rect(0,0,320,222,(0,0,0))\n"

if binary:
    if characters:
        chunksize = 8
        img = np.mean(img,2).astype(np.uint8)
        img = np.where(img == 255, 1,0).astype(np.uint8)
        data = np.full((img.shape[0],int(np.ceil(img.shape[1]/chunksize))),0,dtype=np.uint32)
        for y,row in enumerate(img):
            for i,x in enumerate(row):
                data[y,i//chunksize] += x*(2**(i%chunksize))
        for y in data:
            out += "l(("
            for x in y:
                out += f"{chr(x)},"
            out = out[:-1] + "))\n"
    else:
        img = np.mean(img,2).astype(np.uint8)
        img = np.where(img == 255, 1,0).astype(np.uint8)
        data = np.full((img.shape[0],np.ceil(img.shape[1]/chunksize)),0,dtype=np.uint32)
        for y,row in enumerate(img):
            for i,x in enumerate(row):
                data[y,i//chunksize] += x*(2**(i%chunksize))
        for y in data:
            out += "l(("
            for x in y:
                out += f"{x},"
            out = out[:-1] + "))\n"
else:
    if greyscale:
        for row in range(img.shape[0]):
            out += "l(("
            for column in img[row]:
                out += f"{(int(column[0])+int(column[1])+int(column[2]))//3},"
            out = out[:-1] + "))\n"
    else:
        for row in range(img.shape[0]):
            out += "l(("
            for column in img[row]:
                out += f"{column[2]},{column[1]},{column[0]},"
            out = out[:-1] + "))\n"

print(out)
if cv.waitKey() == ord("q"):
    raise SystemExit
out.encode("latin_1")
output = open("pxout.txt","w")
output.write(out)
output.close