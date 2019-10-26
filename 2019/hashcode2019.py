
import math

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


def readfile(filename):
    with open(filename) as file:
        Number_of_photos = int(file.readline().strip())
        photos = []
        for i in range(Number_of_photos):
            data = file.readline().strip().split()
            photos.append(photo(orientation = data[0],photo_id = i,number_of_tags = int(data[1]),tags =data[1:]))
        return photos

def write2file(results,filename):
    with open(str(filename[0])+".txt","w") as output:
        output.write(str(len(results))+"\n")
        for slide in results:
            if len(slide.slide) == 2:
                res = str(slide.slide[0].photo_id)+" "+ str(slide.slide[1].photo_id) + "\n"
            elif len(slide.slide) == 1:
                res = str(slide.slide[0].photo_id)+"\n"
            output.write(res)

def scoring(slide1,slide2):
    s1 = slide1.tags
    s2 = slide2.tags
    s3 = set(s1).intersection(s2)
    return min(len(s1),len(s2),len(s3))

def createslide(photos):
    slides = []
    indexSet = set()
    for i in range(len(photos)):
        if(i in indexSet):
            continue
        if(photos[i].orientation == "H"):
            slides.append(slide([photos[i]]))
            indexSet.add(i)
        else:
            #print(photos[i].orientation)
            minCommon = math.inf
            minIndex = -1
            for y in range(len(photos)):
                if(y in indexSet):
                    continue
                if(photos[y].orientation == "H"):
                    continue
                if(photos[i].commontag(photos[y]) < minCommon):
                    minIndex = y

            slides.append(slide([photos[i],photos[minIndex]]))
            indexSet.add(i)
            print([i,minIndex])
            indexSet.add(minIndex)


    return slides

def solution(slides):
    #resultats = []
    numberofslides = len(slides)
    scoreFinal = 0
    iterateur = [slides[0]]
    slides.pop(0)
    while len(slides) != 0:
        s = iterateur[-1]
        maxscore = 0
        maxIndex = -1
        for j in range(len(slides)):
            score = scoring(s,slides[j])
            if(score > maxscore):
                maxIndex = j
                maxscore = score
        scoreFinal+= maxscore
        iterateur.append(slides[maxIndex])
        #print(scoreFinal)
        slides.pop(maxIndex)
        print(scoreFinal,str(len(iterateur))+"/"+str(numberofslides))

    return iterateur,scoreFinal



names = ["a_example.txt","b_lovely_landscapes.txt","c_memorable_moments.txt","d_pet_pictures.txt","e_shiny_selfies.txt"]


if __name__ == "__main__":
    pictures = readfile("b_lovely_landscapes.txt")

    slides = createslide(pictures)
    res,score = solution(slides)
    write2file(res,"test")

    
