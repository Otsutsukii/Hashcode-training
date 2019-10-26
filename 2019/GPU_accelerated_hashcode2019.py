
import math
import numpy as np
import pycuda.autoinit
from pycuda import gpuarray
from time import time
from pycuda.elementwise import ElementwiseKernel
from pycuda.compiler import SourceModule
import pycuda.autoinit
import sys


allPhotosTags = []

class photo(object):
    
    def __init__(self,orientation,photo_id,number_of_tags,tags):
        self.orientation = orientation
        self.photo_id = photo_id
        self.number_of_tags = number_of_tags
        self.tags = tags

    def commontag(self,photo):
        settags1 = set(self.tags)
        settags2 = set(photo.tags)
        return len(settags1.intersection(settags2))

class slide(object):
    
    def __init__(self, photos):
        self.slide = photos
        if len(photos) > 1:
            self.id = [photos[0].photo_id,photos[1].photo_id]
            self.number_of_tags = photos[0].number_of_tags + photos[1].number_of_tags
            settags1 = set(photos[0].tags)
            settags2 = set(photos[1].tags)
            self.tags = settags1.union(settags2)
        else:
            self.id = photos[0].photo_id
            self.number_of_tags = photos[0].number_of_tags
            self.tags = photos[0].tags


#score_matrix = gpuarray.empty_like()

def sortSol(photo):
    tmp = sorted(photo,key = lambda x:x.number_of_tags)


    return sorted(photo,key = lambda x:x.number_of_tags)


def computeScore

def toGpuArray(listOfPhoto,keyword):
    computeMatrix = []
    NoT = []
    for i in range(len(listOfPhoto)):
        row = []
        for j in range(len(listOfPhoto)):
            cell = [[keyword[listOfPhoto[i].tags[k]] for k in range(len(listOfPhoto[i].tags))] ,
                    [keyword[listOfPhoto[j].tags[k]] for k in range(len(listOfPhoto[j].tags))]]
            row.append(cell)
            print(row)
    
        computeMatrix.append(row)
        NoT.append(listOfPhoto[i].number_of_tags)
    print(computeMatrix)
    nparray = np.array(computeMatrix)
    nparray2 = np.array(NoT)
    return gpuarray.to_gpu(nparray),gpuarray.to_gpu(nparray2)


ker_distance_score = """
    #define _WIDTH = (blockDim.x*gridDim.x)
    #define _HEIGHT = (blockDim.y*gridDim.y)
    #define _XM(x) = ((x+ _WIDTH)%_WIDTH)
    #define _YM(x) ((y + _HEIGHT)%_HEIGHT)
    #define _INDEX(x,y) ( _XM(x)  + _YM(y) * _WIDTH )
    __global__ void computeScore(int **vector ,  int **result){

        
    }


"""

def produce_matrix_score(gpu2Dkeyword,gpuNoT):
    gpu_matrix_res = gpuarray.empty_like(gpu2Dkeyword)




def readfile(filename):
    keyword= dict()
    with open(filename) as file:
        Number_of_photos = int(file.readline().strip())
        photos = []
        allTags = []
        for i in range(Number_of_photos):
            data = file.readline().strip().split()
            photos.append(photo(orientation = data[0],photo_id = i,number_of_tags = int(data[1]),tags =data[1:]))

            allTags.extend(data[1:])
        allphoto = list(set(allTags))
        print(allphoto)
        for i in range(len(allphoto)):
            keyword[allphoto[i]] = i 
        return photos, keyword

def write2file(results,filename):
    with open(str(filename[0])+".txt","w") as output:
        output.write(str(len(results))+"\n")
        for slide in results:
            if len(slide.slide) == 2:
                res = str(slide.slide[0].photo_id)+" "+ str(slide.slide[1].photo_id) + "\n"
            elif len(slide.slide) == 1:
                res = str(slide.slide[0].photo_id)+"\n"
            output.write(res)


if __name__ == "__main__":
    arg = sys.argv[1]
    photos, keyword = readfile(arg)
    res = sortByLength(photos)
    for elem in res:
        print(elem.number_of_tags)
    #res1 , res2 = toGpuArray(photos,keyword) take too many time for CPU to build GPU matrix input 