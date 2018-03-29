import random


class User(object):


    def __init__(self, name):
        self.name = name
        self.totaldept = 0
        self.depts = dict()

    def add_dept(self, owner, cost):
        if owner in self.depts:
            self.depts[owner] +=cost
        else:
            self.depts[owner] = cost
        self.__total_dept__()

    def __total_dept__(self):
        self.totaldept = sum(self.depts.values())

    def __str__(self):
        t = self.name + " ["
        for x in self.depts.items():
            t += x[0].name + ": " + str(x[1]) + ", "
        return t[:-2] + ']'
    def minimalize_dept(self):
        t = list(self.depts.items())
        #print(t)
        x = [d for d in t if t[1] == 0]
        for m in x:
            del self.depts[m]
        t = [d for d in t if t[1] != 0]
        t.sort(key=lambda o : o[1])
        while (t[0][1]<0 and t[len(t)-1][1] > 0 ):
            tmp1 = t[0]
            tmp2 = t[len(t)-1]
            if(abs(tmp1[1])>abs(tmp2[1])):
                del self.depts[tmp2[0]]
                self.depts[tmp1[0]] += tmp2[1]
                tmp1[0].add_dept(self,tmp2[1])
                tmp1[0].add_dept(tmp2[0],-tmp2[1])
                tmp2[0].add_dept(self,-tmp2[1])
                tmp2[0].add_dept(tmp1[0],tmp2[1])


                del t[len(t)-1]
            elif (abs(tmp1[1]) < abs(tmp2[1])):
                del self.depts[tmp1[0]]
                self.depts[tmp2[0]] += tmp1[1]
                tmp1[0].add_dept(self, - tmp1[1])
                tmp1[0].add_dept(tmp1[0], tmp1[1])
                tmp2[0].add_dept(self, tmp1[1])
                tmp2[0].add_dept(tmp1[0], - tmp1[1])
                del t[0]
            elif (tmp2[1] + tmp1[1] == 0 ):
                del self.depts[tmp1[0]]
                del self.depts[tmp2[0]]
                tmp1[0].add_dept(self, tmp1[1])
                tmp1[0].add_dept(tmp2[0], -tmp1[1])
                tmp2[0].add_dept(self, tmp2[1])
                tmp2[0].add_dept(tmp1[0], -tmp2[1])
                del t[len(t) - 1]
                del t[0]



class Trip(object):

    def __init__(self):
        self.trip_peronel = []

    def add_person(self, person):
        self.trip_peronel.append(person)

    def minimalize(self):
        x = [(t, t.totaldept) for t in self.trip_peronel if t.totaldept != 0]
        x.sort(key=lambda t: t[0])



x = "ABCD"

tmp = [User(t) for t in x]
trip = Trip()
for l in range(16):
    ch = random.sample(tmp,2)
    x = random.randint(-10,10)
    ch[0].add_dept(ch[1], x)
    ch[1].add_dept(ch[0],-x)
for t in tmp:
    trip.add_person(t)
    print(t.totaldept)




for t in tmp:
    print(t)
    #print(t.totaldept)

for t in tmp:
    t.minimalize_dept()

for t in tmp:
   # print(t.totaldept)
    print(t)