from collections import namedtuple
import numpy as np
import pycuda.autoinit
from pycuda import gpuarray
from time import time
from pycuda.elementwise import ElementwiseKernel
from pycuda.compiler import SourceModule
import pycuda.autoinit
import sys
coordinate = namedtuple("coordinate",["x","y"])
from time import time
names = ["a_example","b_should_be_easy","c_no_hurry","d_metropolis","e_high_bonus"]

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

def write2file(results,filename):
    with open(str(filename[0])+".txt","w") as output:
        for car in results:
            res = " ".join([str(ride) for ride in car.booked_rides_id])
            output.write(str(len(car.booked_rides_id)) + " "+ res + "\n")


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#"int *car_coord_x , int *ride_id_start_coord_x , int *car_coord_y , int *ride_id_start_coord_y , int *ride_finish_x , int *ride_start_x , int *ride_finish_y , int *ride_start_y , int ride_endTime, int stepTime" ,

gpu_waittime = ElementwiseKernel(
"int *dist_x , int *dist_y , int *ride_startTime ,int stepTime , int *waittime" ,
"waittime[i] = ride_startTime[i] - (dist_x[i] + dist_y[i]) - stepTime",
name= "gpu_waittime"
)

def distance(x,y):
    gpu_dist_x = x-y
    return gpu_dist_x.__abs__()

def waittime(car_x , car_y , ride_start_x , ride_start_y , ride_start_time , step_time ):
    device_waittime = gpuarray.empty_like(car_x)
    x , y = distance(car_x , ride_start_x) , distance(car_y,ride_start_y)
    gpu_waittime(x,y,ride_start_time,step_time,device_waittime)
    return device_waittime



def computepoints(car_x , car_y , ride_start_x , ride_start_y , ride_finish_x , ride_finish_y , ride_start_time , bonus ,step_time,ride_reward,hasDone):
    
    x, y  = distance(ride_finish_x,ride_start_x) , distance(ride_finish_y,ride_finish_x)
    dist = x + y
    wait_time = waittime(car_x , car_y , ride_start_x , ride_finish_y , ride_start_time, step_time)
    x , y = distance(car_x,ride_start_x) , distance(car_y,ride_start_y)
    wait_distance = x + y
    x  = x.get()
    B = []
    cpu_wait_time = wait_time.get()
    for i in range(len(cpu_wait_time)):
        if cpu_wait_time[i] >= 0 : 
            B.append(bonus)
        else :
            B.append(0)
            cpu_wait_time[i] = 0 #change constants for metropolis , beware of / by 0 
    B2 = gpuarray.to_gpu(np.array(B))
    wait_time2 = gpuarray.to_gpu(cpu_wait_time)

    ratio_ride_gain = (dist*100) + B2
    distance_to_ride = (wait_time2 + ride_reward*5 + wait_distance*2 +1)

    ratio = ratio_ride_gain / distance_to_ride      #ratio ride_gain / distance_to_ride 

    return (ratio*hasDone).get() , ((dist + B2)*hasDone).get() , (step_time + dist + wait_time +wait_distance).get()

def checkride(car_x,car_y, ride_start_x , ride_start_y , ride_finish_x , ride_finish_y , ride_endTime , step_time):
    distance_from_ride = (distance(car_x,ride_start_x ) + distance(car_y,ride_start_y)).get()
    dist = (distance(ride_finish_x,ride_start_x) + distance(ride_finish_y,ride_start_y)).get()
    possible_timing = (ride_endTime - step_time).get()
    available_ride = np.zeros_like(ride_start_x)
    for i in range(len(ride_start_x)):
        if distance_from_ride[i] + dist[i] <= possible_timing[i] :
            available_ride[i] = 1
    return available_ride

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
        self.ride_transform = dict()
    
    def transform_ride_list(self):
        id = []
        start_time = []
        end_time = []
        start_x = [] 
        start_y = [] 
        finish_x = [] 
        finish_y = []
        isDone = []
        reward = []
        for ride in self.rides_list:
            id.append(ride.id)
            start_time.append(ride.start_time)
            end_time.append(ride.end_time)
            start_x.append(ride.start_coord[0])
            start_y.append(ride.start_coord[1])
            finish_x.append(ride.finish_coord[0])
            finish_y.append(ride.finish_coord[1])
            isDone.append(ride.done)
            reward.append(ride.reward)
        self.ride_transform = {
            "id":np.array(id) , "start_time":np.array(start_time) ,"end_time":np.array(end_time),
            "start_x":np.array(start_x) , "start_y" :np.array(start_y),"finish_x":np.array(finish_x),
            "finish_y":np.array(finish_y) , "isDone" : np.array(isDone) ,"reward":np.array(reward)
        }

    def get_updated_ride(self,time):
        isDone = [1 for i in range(len(self.ride_transform["isDone"])) ]
        timestart = self.ride_transform["start_time"]
        id = []
        start_time = []
        end_time = []
        start_x = [] 
        start_y = [] 
        finish_x = [] 
        finish_y = []
        reward = []
        for i in range(len(isDone)):
            if isDone[i] == 1 :
                id.append(self.ride_transform["id"][i])
                start_time.append(self.ride_transform["start_time"][i])
                end_time.append(self.ride_transform["end_time"][i])
                start_x.append(self.ride_transform["start_x"][i])
                start_y.append(self.ride_transform["start_y"][i])
                finish_x.append(self.ride_transform["finish_x"][i])
                finish_y.append(self.ride_transform["finish_y"][i])
                reward.append(self.ride_transform["reward"][i])
        return (id , gpuarray.to_gpu(np.array(start_time))  , gpuarray.to_gpu(np.array(end_time)), 
            gpuarray.to_gpu(np.array(start_x)) , gpuarray.to_gpu(np.array(start_y)), gpuarray.to_gpu(np.array(finish_x)), 
            gpuarray.to_gpu(np.array(finish_y)), gpuarray.to_gpu(np.array(reward)),gpuarray.to_gpu(np.array(isDone)) )
            
    
    def compute(self):
        self.transform_ride_list()
        time = 0
        scores = 0 
        id , start_time , end_time , start_x , start_y , finish_x , finish_y , reward,hasDone = self.get_updated_ride(time)
        while time < self.T:
            print("current tick :",time,"/",self.T ,' real score:',scores, " filename :",self.filename)
            

            for car in self.fleet:
                car.booked_ride_info = []
                if car.available_time <= time:

                    if id != []:
                        car_x , car_y = gpuarray.to_gpu(np.array([car.coord[0]]*len(id))) , gpuarray.to_gpu(np.array([car.coord[1]]*len(id)))
                        # available_ride = checkride(car_x,car_y,start_x,start_y,finish_x,finish_y,end_time,time)
                        pts , score ,finish_time = computepoints(car_x,car_y,start_x,start_y,finish_x,finish_y,start_time,self.bonus,time,reward,hasDone)
                        best_i = np.argmax(pts) 
                        best_id = id[best_i]
                        scores += score[best_i]
                        car.booked_rides_id.append(best_id)
                        self.ride_transform["isDone"][best_i] = 0
                        hasDone = hasDone.get()
                        hasDone[best_i] = 0
                        somme = sum(hasDone)
                        hasDone = gpuarray.to_gpu(hasDone)
                        if somme == 0 or somme <= 2  :
                            time = time + self.T
                        car.available_time = finish_time[best_id]  
                        car.coord = coordinate(finish_x.get()[best_i],(finish_y.get())[best_i] )

            time += 1 
        return scores


if __name__=="__main__":
    
    #names = ["a_example.in","b_should_be_easy.in","c_no_hurry.in","d_metropolis.in","e_high_bonus.in"]
    #names = ["d_metropolis.in"] too slow 
    name = sys.argv[1]
    data = readfile(name)
    res = solution(data["Time"],data["bonus"],data["fleet"],data["rides_list"],data["row"],data["col"],name)
    t1 = time()
    res.compute()
    t2 = time()
    print(t2-t1)
    write2file(res.fleet,name)
    print(name)