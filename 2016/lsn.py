class Warehouse(object):
    def __init__(self, id,x,y,product):
        self.id = id
        self.x = x
        self.y = y
        n = list(range(len(product)))
        self.product = dict(zip(n,list(map(int,product))))

class drone(object):
    def __init__(self,x,y,id, capacity,inventory):
        self.x = x
        self.y = y
        self.id = id
        self.capacity = capacity
        self.inventory = inventory

class order(object):
    def __init__(self,products,id,x,y):
        self.products = products
        self.id = id
        self.x = x 
        self.y = y
        self.turn = 0

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
            x_order, y_order = map(int, file.readline().strip().split())
            num_item = int(file.readline().strip())
            item_num = file.readline().strip().split()
            _dict = dict(zip(n,n_zeros))
            for it in item_num:
                _dict[int(it)] += 1 

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


# 输入的文件名字
row, col, nturn, list_warehouse, list_drone, list_order, weight_dist = readfile("/Users/lnan951/course/EIT/hashcode/2016/qualification_round_2016.in/redundancy.in")


