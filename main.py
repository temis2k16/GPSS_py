import numpy.random as rand
from collections import OrderedDict as ODict


class Tr:
    def __init__(self, id):
        self.__init_obsl = 7200.0
        self.id = id
        self.time = 0.0
        self.next_block = 1
        self.curr_block = 0
        self.working = 0.0
        self.obsl = self.__init_obsl

    def __repr__(self):
        return ":%d, %.1f, %d, %d, %.1f, %.1f:" % (self.id, self.time, self.curr_block, self.next_block, self.working, self.obsl)

    def show_attr(self):
        print([self.working, self.obsl])

    def gen_working(self):  # 1st advance
        self.working = 400.0 + rand.exponential(200.0)  # 400 = min, 400+200 = mean

    def init_obsl(self):
        self.obsl = self.__init_obsl

    def reduce_obsl(self):
        self.obsl = self.obsl - self.working

    def set_pos_adv1(self):
        self.curr_block = 5
        self.next_block = 6

    def set_pos_test_return(self):
        self.curr_block = 9
        self.next_block = 5

    def set_pos_fixing(self):
        self.curr_block = 13
        self.next_block = 14


class Fixer:
    # he has queue and takes transacts from queue
    def __init__(self):
        self.M = 40  # number of fixers
        self.Queue = []
        self.Processing = []
        self.OutputProcessing = []
        self.sum_q = 0.0
        self.sum_nal = 0.0

    def process(self, sys_time):
        self.OutputProcessing.clear()
        if len(self.Processing) < self.M:
            self.OutputProcessing.extend(self.Queue[0:self.M])
            del(self.Queue[0:self.M])
            for j in self.OutputProcessing:
                j.time = sys_time + Fixer.gen_processing()
            self.Processing.extend(self.OutputProcessing)
        # print("PROCESSING: ", self.Processing)
        # print("QUEUE: ", self.Queue)
        self.sum_q += len(self.Queue)
        self.sum_nal += len(self.Processing)/2
        return self.OutputProcessing

    def end_fixing(self, sys_time):
        for q in self.Processing:
            if q.time == sys_time:
                self.Processing.pop(0)

    @staticmethod
    def gen_processing():
        return 600.0 + rand.exponential(400.0)  # 600 = min, 600+400 = mean


fixing = Fixer()
FEC = ODict()
CEC = ODict()
N = 40  # transact quantity
Item = 0
ToRepair = 0
# entry phase
sys_time = 0.0
FEC[sys_time] = []
for i in range(N):
    FEC[sys_time].append(Tr(i))
# correction phase
FEC = ODict(sorted(FEC.items()))
sys_time = list(FEC.keys())[0]
CEC[sys_time] = FEC.pop(sys_time)
# look up phase
# before "WORK" cycle
for i in CEC[sys_time]:
    i.gen_working()
# in "WORK" cycle
while sys_time < 86400:
    # first advance
    for i in CEC[sys_time]:
        i.time += i.working
        i.reduce_obsl()
        i.set_pos_adv1()
        FEC[i.time] = []
        FEC[i.time].append(i)
    CEC.pop(sys_time)
    FEC = ODict(sorted(FEC.items()))
    # new correction phase
    # after advance
    sys_time = list(FEC.keys())[0]
    CEC[sys_time] = FEC.pop(sys_time)
    index = 0
    for i in CEC[sys_time]:
        Item += 1
        i.set_pos_test_return()
        i.gen_working()  # generate future working time
        if i.working >= i.obsl:
            i.set_pos_fixing()
            CEC.pop(sys_time)
            ToRepair += 1
            i.init_obsl()
            fixing.Queue.append(i)
            processed = []
            processed.extend(fixing.process(sys_time))
            for j in processed:
                if j:
                    FEC[j.time] = []
                    FEC[j.time].append(j)
            FEC = ODict(sorted(FEC.items()))
            sys_time = list(FEC.keys())[0]
            CEC[sys_time] = FEC.pop(sys_time)
        index += 1
    fixing.end_fixing(sys_time)
print("repair", ToRepair)
print("Items = ", Item)
print("sum_q = ", fixing.sum_q)
print("mean q = ", fixing.sum_q/ToRepair)
print("mean nal = ", fixing.sum_nal/ToRepair)
print("Koef nal = ", fixing.sum_nal/ToRepair/fixing.M)
