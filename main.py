import random
import numpy.random as rand


class Tr:
    def __init__(self, id):
        self.id = id
        self.time = 0.0
        self.next_block = 1
        self.curr_block = 0
        self.working = 0.0
        self.obsl = 7200.0

    def __repr__(self):
        return "[%d, %d, %d, %d, %.1f, %.1f]" % (self.id, self.time, self.curr_block, self.next_block, self.working, self.obsl)

    def show_attr(self):
        print([self.working, self.obsl])

    def gen_working(self):  # 1st advance
        self.working = 400.0 + rand.exponential(200.0)  # 400 = min, 400+200 = mean

    def init_obsl(self):
        self.obsl = 7200.0

    def reduce_obsl(self, w):
        self.obsl = self.obsl - w


FEC = {}
CEC = {}
N = 5

Item = 0
sys_time = 0.0
FEC[sys_time] = []
for i in range(N):
    FEC[sys_time].append(Tr(i))

print("CEC:\n", CEC)
print("FEC:\n", FEC)
# correction phase
CEC[sys_time] = FEC.pop(sys_time)
print("CEC:\n", CEC)
print("FEC:\n", FEC)
# look up phase
