from test import voiture



class garage(object):
    def __init__(self,v1,v2,v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3



if __name__=="__main__":
    dataVoiture = [[voiture(i,i,i),voiture(i,i,i),voiture(i+1,i+2,i)] for i in range(10)]
    garages = [garage(L[0],L[1],L[2]) for L in dataVoiture]
    for g in garages:
        g = garages