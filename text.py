class Vector:
    def __init__(self, point_list):
        self.point_list = point_list

    def print_list(self):
        for i in self.point_list:
            print(i)

f = Vector([1,2,3,1])
f.print_list()