import math
import pdb
import copy
# io return
# weight_dist

class Warehouse(object):
    def __init__(self, id,x,y,product):
        self.id = id
        self.x = x
        self.y = y
        n = list(range(len(product)))
        # self.product = {'item_type': item_num}
        self.product = dict(zip(n,list(map(int,product))))
    
    def update(self, _order, item_type):
        self.product[item_type] -= _order.product[item_type]
        # print(self.product[item_type])
        assert self.product[item_type] >= 0
        
class drone(object):
    def __init__(self,x,y,id, capacity,inventory):
        self.x = x
        self.y = y
        self.id = id
        self.capacity = capacity
        self.currentCapacity = 0
        self.inventory = {}
        self.available = 0
        self.commands = []
    def load(self, warehouse, type_product, num=1):
        self.commands.append("{0} L {1} {2.id} {3}".format(self.id, type_product, warehouse, num))
    def deliver(self, warehouse, type_product, num=1):
        self.commands.append("{0} D {1} {2.id} {3}".format(self.id, type_product, warehouse, num))
    def output(self):
        print(len(self.commands))
        for command in self.commands:
            print(command)



class order(object):
    def __init__(self,product,id,x,y,nturn):
        self.product = product
        self.id = id
        self.x = x 
        self.y = y
        self.turn = 0
        self.T = nturn
        self.done = False
    def score(self):
        return math.ceil(((self.T - self.turn)/self.T )* 100 ) # round up to next integer
    
    def __str__(self):
        return str(self.product) 


    
def readfile(filename):
    with open(filename) as file:
        nrow, ncol, ndrone, nturn, maxLoad = map(int, file.readline().strip().split())
        num_product = int(file.readline())
        weight_dist = dict(zip(list(range(num_product)),list(map(int, file.readline().strip().split()))))
        
        num_warehouse = int(file.readline().strip())
        list_warehouse = []
        for warehouse_id in range(num_warehouse):
            x, y = map(int, file.readline().strip().split())
            _product = file.readline().strip().split()

            list_warehouse.append(Warehouse(warehouse_id, x,y, _product))
        # Order
        num_order = int(file.readline().strip())
        n = list(range(num_product))
        n_zeros = [0]*num_product

        list_order = []
        for _order in range(num_order):
            _dict = {}
            x_order, y_order = map(int, file.readline().strip().split())
            num_item = int(file.readline().strip())
            item_num = file.readline().strip().split()
            # _dict = dict(zip(n,n_zeros))
            for it in item_num:
                if int(it) not in _dict:
                    _dict[int(it)] = 1 
                else:
                    _dict[int(it)] = 0
            list_order.append(order(_dict, _order, x_order, y_order,nturn))
        
        # drone
        list_drone = []
        for i in range(ndrone):
            list_drone.append(drone(0,0,i,maxLoad,{}))
        # weight_dist = {product type : weight of the product }
        # list_warehouse = {id : warehouse实例}
        # list_drone = {id : drone实例}
        # list_order = {id : order实例}

        return nrow, ncol, nturn, list_warehouse, list_drone, list_order, weight_dist


def distance(x1,y1,x2,y2):
    return math.ceil(math.sqrt((x1-x2)**2 + (y1-y2)**2))


class solution(object):
    def __init__(self, nrow, ncol, list_drone, weight_dist,T):
        self.orders = SortedOrder
        self.warehouse = SortedWarehouses
        self.drone = list_drone
        self.row = nrow
        self.col = ncol
        self.T = T
        self.weight = weight_dist

    
    def solution(self):
        score = 0
        drones = self.drone
        orders = self.orders
        nearstWarehouses = self.warehouse
        t = 0 
        T = self.T
        while t < T:
            available_drones = [drones[i] for i in range(len(drones)) if drones[i].available < t and drones[i].x < self.row and drones[i].y < self.col ]
            if available_drones != [] and orders != []:

                orders = [ orders[j] for j in range(len(orders)) if orders[j].done is False]

                for i_order in range(len(orders)):
                    t_score = 0 
                    nearstWarehouses = sorted( nearstWarehouses , key=lambda x : distance(orders[i_order].x , orders[i_order].y , x.x , x.y) )
                    for item_type,item_num in orders[i_order].product.items():
                        selected_warehouses = []
                        for i_warehouse in range(len(nearstWarehouses)):
                            
                            if nearstWarehouses[i_warehouse].product[item_type] > 0 :
                                quantity = nearstWarehouses[i_warehouse].product[item_type] - item_num
                                if quantity > 0  : 
                                    nearstWarehouses[i_warehouse].product[item_type] -= quantity
                                    orders[i_order].product[item_type] = 0
                                elif quantity == 0 : 
                                    nearstWarehouses[i_warehouse].product[item_type] = 0 
                                    orders[i_order].product[item_type] = 0
                                elif quantity < 0 :
                                    nearstWarehouses[i_warehouse].product[item_type] = 0 
                                    orders[i_order].product[item_type] -= quantity
                                selected_warehouses.append(i_warehouse)
                        for w in selected_warehouses:
                            Ndrones = math.ceil((item_num*self.weight[item_type]) / available_drones[0].capacity)
                            nearstDrones = sorted( available_drones , key= lambda x: distance(nearstWarehouses[w].x , nearstWarehouses[w].y , x.x , x.y))
                            for i in range(Ndrones):
                                nearstDrones[i].available += distance(nearstWarehouses[w].x , nearstWarehouses[w].y , nearstDrones[i].x , nearstDrones[i].y) +1 
                                nearstDrones[i].x , nearstDrones[i].y = nearstWarehouses[w].x , nearstWarehouses[w].y
                                while nearstDrones[i].currentCapacity + self.weight[item_type] <= nearstDrones[i].capacity  : 
                                    if item_type in nearstDrones[i].inventory:
                                        nearstDrones[i].inventory[item_type] +=1
                                        nearstDrones[i].currentCapacity += self.weight[item_type]
                                        item_num -= 1 
                                    else:
                                        nearstDrones[i].inventory[item_type] =1
                                        nearstDrones[i].currentCapacity += self.weight[item_type]
                                        item_num -= 1 
                                nearstDrones[i].available += distance(orders[i_order].x , orders[i_order].y, nearstDrones[i].x , nearstDrones[i].y) +1 
                                nearstDrones[i].x , nearstDrones[i].y = orders[i_order].x , orders[i_order].y
                                t_score = max(t_score,nearstDrones[i].available)
                                
                        for i_drones in range(len(drones)):
                            for j_drones in range(len(nearstDrones)):
                                if drones[i_drones].id == nearstDrones[j_drones].id and drones[i_drones].available < nearstDrones[j_drones].available: 
                                    drones[i_drones].available = nearstDrones[j_drones].available
                                    
                    if sum(orders[i_order].product.values())== 0 :
                        orders[i_order].done = True
                        if t_score < T:
                            orders[i_order].turn = t_score
                            score += orders[i_order].score()   

            else:
                nextAvailableDrone = min(drones,key=lambda x:x.available)
                t+=1
            print(str(t) + "/"+str(self.T)+" scores : "+ str(score))

             
                    
if __name__ == '__main__':
    # 输入的文件名字
    file_name = "mother_of_all_warehouses.in"
    file_name = "busy_day.in"
    file_name = "redundancy.in"
    
    
    
    # file_name = "busy_day.in"
    row, column, nturn, list_warehouse, list_drone, list_order, weight_dist = readfile(file_name)
    # 全局时间
    T = nturn

    SortedOrder = sorted(list_order,key= lambda x: x.x+x.y)
    SortedWarehouses = sorted(list_warehouse, key = lambda x:x.x+x.y)

    Solution = solution(row, column, list_drone, weight_dist,T)
    Solution.solution()


    