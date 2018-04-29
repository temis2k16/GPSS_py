# d = {}
# t = 0
# new = 3
# d[t] = []
# print d
# for i in range(new):
#     d[t].append(i)
# print d
# del d[t][0]
# print d


class Tr:
    def __init__(self, id):
        self.id = id
        self.time = 0
        self.next_block = 1
        self.curr_block = 0

    def show_attr(self):
        print [self.id, self.time, self.curr_block, self.next_block]


t = []
for i in range(10):
    t.append(Tr(i))
# t1 = Tr(1)
t[9].show_attr()
