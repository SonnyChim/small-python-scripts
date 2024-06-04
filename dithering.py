import numpy as np
import cv2 as cv

def main():
    import time
    import timeit
    original_image = cv.imread("rcimglq.png")
    if original_image is None:
        print("image not found")
        return
    # original_image = np.dstack((np.broadcast_to(np.repeat(np.arange(255, dtype= np.uint8),1),(255,255)),np.rot90(np.broadcast_to(np.repeat(np.arange(255, dtype= np.uint8),1),(255,255)),-1),np.full((255,255),0,dtype=np.uint8)))
    # original_image = cv.imread(input("Input file name: "))
    # original_image = np.full((100,200),128,dtype=np.uint8)
    print(original_image.shape)
    # palette = np.array(((65,80,110),(240,240,240),(190,100,85),(220,205,92),(40,40,60),(170,80,80),(75,110,85))) # 7 color e paper 
    palette = np.array(((0,0,0),(255,255,255))) # Black and white
    # palette = np.array(((0,0,255),(0,255,0),(255,0,0),(0,0,0),(255,255,255),(0,255,255),(255,0,255),(255,255,0))) # RGB CMY Black and white
    # palette = np.array(((0,0,255),(0,255,0),(255,0,0),(0,0,0),(255,255,255))) # RGB Black and white
    # palette = np.array(((0,255,255),(255,0,255),(255,255,0),(0,0,0),(255,255,255))) # CMY Black and white
    # palette = np.array(((255,0,0),(0,255,0),(0,0,255))) # RGB
    # palette = np.array(((0,0,0),(85,85,85),(170,170,170),(255,255,255))) # 4 color greyscale

    for i,color in enumerate(palette):
        palette[i] = np.array((color[2],color[1],color[0]))
    # for i,color in enumerate(palette):
    #     cv.imshow(str(i),np.full((100,100,3),color,np.uint8))
    if original_image is None:
        print('Could not open or find the image')
        raise SystemExit
    # if np.array(original_image.shape).shape == (3,):
    #     cv.imshow("grey", np.mean(original_image,2).astype(np.uint8))
    # else:
    cv.imshow("input", original_image)
    # cv.imshow("output1",closest_color(original_image,palette))
    # cv.imshow("output1",average_dithering(original_image))
    # cv.imshow("output2",random_dithering(original_image))
    # cv.imshow("output3",ordered_dithering(original_image))

    # cv.namedWindow("progress")
    # cv.waitKey()
    
    # original_image = np.repeat(np.expand_dims(np.mean(original_image,2).astype(np.uint8),2),3,2)
    start = time.perf_counter_ns()

    outimg = floyd_steinberg(original_image,palette)
    cv.imshow("output4",outimg)
    print((time.perf_counter_ns()-start)/10**9)
    if cv.waitKey() != ord("q"):
        cv.imwrite("ditheringOut.png",outimg)

    
    # print(timeit.timeit("ordered_dithering(original_image)", "original_image = cv.imread('ditheringexample.png')", globals=globals(),number=3000))
    # print(timeit.timeit("floyd_steinberg(original_image,palette)", "original_image = cv.imread('ditheringexample.png');palette = np.array(((0,0,255),(0,255,0),(255,0,0),(0,0,0),(255,255,255)))", globals=globals(),number=5))

def closest_color(input,palette,show_progress = True):
    if type(input) == int:
        return palette[(np.square(palette[:,0]-input)+np.square(palette[:,1]-input)+np.square(palette[:,2]-input)).argmin()]
    elif input.shape == (3,):
        return palette[(np.square(palette[:,0]-input[0])+np.square(palette[:,1]-input[1])+np.square(palette[:,2]-input[2])).argmin()]
    else:
        output = np.full_like(input,0,dtype=np.uint8)
        for y,row in enumerate(input):
            for x,value in enumerate(row):
                output[y][x] = palette[(np.square(palette[:,0]-value[0])+np.square(palette[:,1]-value[1])+np.square(palette[:,2]-value[2])).argmin()]
            if not y%(input.shape[0]//10):
                if show_progress:
                    cv.imshow("progress",output)
                if cv.waitKey(1) == ord("q"):
                    break
        if show_progress:
            cv.destroyWindow("progress")
            cv.waitKey(1)
            return output

def average_dithering(input_image):
    if np.array(input_image.shape).shape == (3,):
        greyscale_image = np.mean(input_image,2)
    else:
        greyscale_image = input_image
    average_value = np.mean(greyscale_image)
    # output_image = np.repeat(np.expand_dims(np.where(greyscale_image < average_value,0 ,255),2),3,2).astype(np.uint8)
    output_image = np.where(greyscale_image < average_value,0 ,255).astype(np.uint8)
    return output_image

def random_dithering(input_image):
    if np.array(input_image.shape).shape == (3,):
        greyscale_image = np.mean(input_image,2)
    else:
        greyscale_image = input_image
    random_map = np.random.default_rng().integers(0,256,greyscale_image.shape,dtype=np.uint8)
    # output_image = np.repeat(np.expand_dims(np.where(greyscale_image <= random_map,0 ,255),2),3,2).astype(np.uint8)
    output_image = np.where(greyscale_image <= random_map,0 ,255).astype(np.uint8)
    return output_image

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

"""
        1  3        1  9  3 11        These patterns (and their rotations

        4  2       13  5 15  7        and reflections) are optimal for a

                    4 12  2 10        dispersed-pattern ordered dither.

                   16  8 14  6
"""

def floyd_steinberg(input_image,palette = np.array(((0,0,0),(255,255,255))),show_progress = True):
    shape = input_image.shape
    output_image = np.zeros(shape,dtype=np.uint8)
    # output_image = np.copy(input_image)
    input_image = np.pad(input_image,((0,1),(0,1),(0,0))).astype(np.int16)
    for y in range(shape[0]):
        for x in range(shape[1]):
            old_pixel = np.clip(input_image[y][x],0,255)
            new_pixel = closest_color(np.full((3,),old_pixel),palette)
            output_image[y][x] = new_pixel
            quantization_error = old_pixel - new_pixel
            input_image[y    ][x + 1] += (quantization_error * 0.4375).astype(np.int16) # 7 / 16
            input_image[y + 1][x - 1] += (quantization_error * 0.1875).astype(np.int16) # 3 / 16
            input_image[y + 1][x    ] += (quantization_error * 0.3125).astype(np.int16) # 5 / 16
            input_image[y + 1][x + 1] += (quantization_error * 0.0625).astype(np.int16) # 1 / 16
        if not y%(shape[0]//10):
            if show_progress:
                cv.imshow("progress",output_image)
            if cv.waitKey(1) == ord("q"):
                break
    if show_progress:
        cv.destroyWindow("progress")
        cv.waitKey(1)
    return output_image

if __name__ == "__main__":
    main()