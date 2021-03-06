"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""


import utils
import numpy as np
import json
import time


def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    
    org_row=len(img)
    org_col=len(img[0])
    img=img.flatten()
    m=len(img)
    
    pixels=np.unique(img)
    length_unique=len(pixels)
    combo=[]

    for i in range(length_unique):
        for j in range(i+1,length_unique):
                temp_list=[pixels[i],pixels[j]]
                combo.append(temp_list)
                
    fc=[]
    fl=[]
    temp_pl=[]
    d=np.array([]).reshape(m,0)
    minimum_sum=99999999999999999   
    
    for i in range(len(combo)):
        centers=combo[i]
        updated_centers=[]   

        while(centers!=updated_centers):
    
            updated_centers=centers.copy()
            d=np.array([]).reshape(m,0)
    
            for j in range(k):
                d=np.c_[d,abs(img-centers[j])]
        
            temp_pl=np.argmin(d,axis=1)
    
            centers=list(np.array([img[temp_pl==z].mean(axis=0) for z in range(k)]))

        d_min=np.sum(np.amin(d,axis=1))
        
        if(d_min<minimum_sum):
            minimum_sum=d_min
            fc=centers
            fl=np.reshape(temp_pl,(org_row,org_col))
    
    
    return (fc,fl,minimum_sum)


def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.
    
    rows=len(labels)
    cols=len(labels[0])
    visualimg=np.zeros((rows,cols))
    
    for i in range(rows):
        for j in range(cols):
            if(labels[i][j]==0):
                visualimg[i][j]=centers[0]
            else:
                visualimg[i][j]=centers[1]
     
    
    return visualimg.astype(np.uint8)

     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
