
from collections import namedtuple
import numpy as np
coordinate = namedtuple("coordinate",["x","y"])


class  car(object):
    def __init__(self,id):
        self.coord = coordinate(0,0)
        self.id = id
        self.booked_rides_id = []
        self.booked_ride_info = []
        self.riding= False
        self.is_assigned = False
        self.rewards = 0
        self.available_time = 0


class Ride(object):
    def __init__(self,id,start_time,end_time,start_coord,finish_coord):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.start_coord = start_coord
        self.finish_coord = finish_coord
        self.done = False
        self.reward = 0



def readfile(filename):
    with open(filename) as file:
        row,col,cars,rides,Bonus,Tick = map(int, file.readline().strip().split())
        fleet = [car(id) for id in range(cars)]
        rides_list = []
        for ride_id in range(rides):
            a,b,x,y,start,finish = map(int, file.readline().strip().split())
            start_coord = coordinate(a,b)
            end_coord = coordinate(x,y)
            ride = Ride(ride_id,start,finish,start_coord,end_coord)
            rides_list.append(ride)
        
        return {"row":row,"col":col,"bonus":Bonus,"Time":Tick,"fleet":fleet,"rides_list":rides_list}

names = ["a_example","b_should_be_easy","c_no_hurry","d_metropolis","e_high_bonus"]

def write2file(results,filename):
    with open(str(filename[0])+".txt","w") as output:
        for car in results:
            res = " ".join([str(ride.id) for ride in car.booked_rides_id])
            output.write(str(len(car.booked_rides_id)) + " "+ res + "\n")



def checkride(car,ride_id,step_time):
    distance_from_ride = abs(car.coord.x- ride_id.start_coord.x)+abs(car.coord.y - ride_id.start_coord.y)
    distance = abs(ride_id.finish_coord.x - ride_id.start_coord.x)+abs(ride_id.finish_coord.y-ride_id.start_coord.y)
    possible_timing = ride_id.end_time - step_time
    if distance_from_ride + distance <= possible_timing :
        return True
    else:
        return False

def waittime(car,ride_id,step_time):
    distance_from_ride = abs(car.coord.x- ride_id.start_coord.x)+abs(car.coord.y - ride_id.start_coord.y)
    return ride_id.start_time - distance_from_ride - step_time

def computepoints(car,ride_id,bonus,step_time):
    distance = abs(ride_id.finish_coord.x - ride_id.start_coord.x)+abs(ride_id.finish_coord.y-ride_id.start_coord.y)
    wait_time = waittime(car,ride_id,step_time)
    wait_distance = abs(car.coord.x - ride_id.start_coord.x)+abs(car.coord.y-ride_id.start_coord.y)
    B= 0 
    if wait_time >= 0 : 
        B = bonus
    elif wait_time <0: 
        B = 0
        wait_time = 0 #change constants for metropolis , beware of / by 0 
    ratio = (distance*100 + B)/(wait_time + ride_id.reward*5 + wait_distance*2 +1) #ratio ride_gain / distance_to_ride 
    return ratio , distance + B , step_time + distance + wait_time +wait_distance

#-------------------------------------

#-------------------------------------Solutions


class solution(object):
    def __init__(self,T,bonus,fleet,rides_list,R,C,filename =""):
        self.fleet=fleet
        self.rides_list = rides_list
        self.bonus= bonus
        self.T=T
        self.R=R
        self.C=C
        self.filename = filename
    
    def compute(self):
        time = 0
        scores = 0 
        while time < self.T:
            print("current tick :",time,"/",self.T ,' real score:',scores, " filename :",self.filename)
            for car in self.fleet:
                car.booked_ride_info = []
                if car.available_time <= time:




                    for ride in self.rides_list:
                        if ride.done == False:
                            if checkride(car,ride,time):
                                pts , score ,finish_time = computepoints(car,ride,self.bonus,time)
                                car.booked_ride_info.append({"id":ride.id,"pts":pts,"score":score,"done":finish_time})
                    best = max(car.booked_ride_info ,key=lambda x:x["pts"],default=None)
                    if best:
                        selected = self.rides_list[best["id"]]
                        scores += best["score"]
                        car.booked_rides_id.append(selected)
                        selected.done = True
                        car.available_time = best["done"]   
                        car.coord = coordinate(selected.finish_coord.x,selected.finish_coord.y) 
                    else:
                        car.is_assigned = False
            time += 1 
        return scores


if __name__=="__main__":
    names = ["a_example.in","b_should_be_easy.in","c_no_hurry.in","d_metropolis.in","e_high_bonus.in"]
    #names = ["d_metropolis.in"] too slow 
    for name in names:
        data = readfile(name)
        res = solution(data["Time"],data["bonus"],data["fleet"],data["rides_list"],data["row"],data["col"],name)
        res.compute()
        write2file(res.fleet,name)
        print(name)



#        return {"row":row,"col":col,"bonus":Bonus,"Time":Tick,"fleet":fleet,"rides_list":rides_list}
                                      

            
        

    
              








