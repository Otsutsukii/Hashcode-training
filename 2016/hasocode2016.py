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
    def __init__(self, nrow, ncol, list_drone, weight_dist):
        self.orders = SortedOrder
        self.warehouse = SortedWarehouses
        self.drone = list_drone
        self.row = nrow
        self.col = ncol
        self.T = T
        self.weight = weight_dist

    
    def solution(self):
        Warehouses = self.warehouse
        order_num = 0
        score = 0
        drones = self.drone
        for i,_order in enumerate(self.orders):
            _order_drone = copy.deepcopy(_order)
            t = 0
            print("第%d个order" % i)
            _max = 0
            Warehouses = sorted(Warehouses,key = lambda w:distance(w.x,w.y,_order.x,_order.y))
            warehouse_list = []
            for warehouse in Warehouses:
                for item_type, item_num in _order.product.items():
                    if warehouse.product[item_type] == 0:
                        continue
                    if warehouse.product[item_type] >= item_num: 
                        warehouse_list.append(warehouse)
                        #print("product_warehouse %d" % warehouse.product[item_type])
                        #print("product_order %d" % _order.product[item_type])
                        warehouse.update(_order, item_type)
                        _order.product[item_type] = 0
                    else:
                        warehouse_list.append(warehouse)
                        _order.product[item_type] -= warehouse.product[item_type]
                        warehouse.update(warehouse, item_type)

                # print("warehouse_list 长度 %d" % len(warehouse_list))
                for warehouse in warehouse_list:
                    x1, y1 = warehouse.x,warehouse.y
                    # nearstAvailable = sorted(self.drone, key=lambda x:distance(x1,y1,x.x,x.y) )
                    # nearstAvailable = sorted(nearstAvailable,key = lambda x: x.avaible)
                    nearstAvailable = sorted(drones, key = lambda x: x.available + distance(x1,y1,x.x,x.y) + distance(x1, y1, _order.x, _order.y))
                    t = nearstAvailable[0].available
                    while _order_drone.product[item_type] > 0:
                    # while warehouse.product[item_type] > 0: 

                        for drone in range(len(nearstAvailable)):
                            if nearstAvailable[drone].available <= t: 
                                capacity = nearstAvailable[drone].capacity
                                loaded = 0
                                quantity = 0
                                while capacity >= loaded + self.weight[item_type]:
                                    if item_type not in nearstAvailable[drone].inventory:
                                        nearstAvailable[drone].inventory[item_type] = 1
                                    else:
                                        nearstAvailable[drone].inventory[item_type] +=1
                                    quantity+=1
                                    loaded += self.weight[item_type]
                                    # warehouse.product[item_type] -=1
                                    _order_drone.product[item_type] -= 1
                                nearstAvailable[drone].load(warehouse, item_type, quantity)
                                nearstAvailable[drone].currentCapacity = loaded
                                nearstAvailable[drone].available += distance(nearstAvailable[drone].x,nearstAvailable[drone].y,warehouse.x,warehouse.y) + 1 
                                nearstAvailable[drone].available += distance(_order.x,_order.y,warehouse.x,warehouse.y) + 1
                                nearstAvailable[drone].deliver(_order,item_type,nearstAvailable[drone].inventory[item_type])
                                nearstAvailable[drone].x = _order.x
                                nearstAvailable[drone].y = _order.y
                                _max = max(_max, nearstAvailable[drone].available)
                            nearstAvailable = sorted(drones,key = lambda x: x.available + distance(x1,y1,x.x,x.y) + distance(x1, y1, _order.x, _order.y))
                    
            order_num += 1         
            if t > T:
                # print(t)
                break
            # pdb.set_trace()
            print(str(t) + "/" + str(T))
            _order.turn = _max
            score += _order.score()
            print("score : %d" %score)
        print("total order num: %d" % order_num)


             
                    
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
    SortedWarehouses = sorted(list_warehouse, key = lambda x:distance(0,0,x.x,x.y))

    Solution = solution(row, column, list_drone, weight_dist)
    Solution.solution()


    