from random import *
from time import *
import os
amount = 70
nums = []
max = 100
for i in range(amount):
    nums.append(randrange(1,max,1))

def bar():
    yrange = 20
    bargraph = ""
    # bargraph = []
    for y in range(yrange):
        line = ""
        d = max - (max/yrange*(y+1))
        for x in range(amount):
            if nums[x] > d:
                line = line + "█ "
            else:
                line = line + "  "
        bargraph += line + "\n"
    os.system("cls" if os.name == "nt" else "clear")
    print(bargraph)
    #     bargraph.append(line)
    # os.system("cls")
    # for y in range(yrange):
    #     print(bargraph[y])

for i in range(amount-1):
    numsleft = amount - i
    sorted = True
    for i in range(numsleft-1):
        bar()
        #print(nums)
        if nums[i] > nums[i+1]:
            a = nums[i]
            sorted = False
            nums[i] = nums[i+1]
            nums[i+1] = a
    if sorted:
        break

bar()
