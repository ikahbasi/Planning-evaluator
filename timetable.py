from datetime import datetime as dt
import matplotlib.pyplot as plt



def Time(hour, minute, second, year=2023, month=1, day=1):
    return dt(year, month, day, hour, minute, second)


class ToDo:
    def __init__(self, stime, etime):
        self.stime = Time(*stime)
        self.etime = Time(*etime)
        self.offset = 0


class Day:
    def __init__(self, day_name, day_number):
        self.day_name = day_name
        self.day_number = day_number
        self.plan = {}
    def _list_time(self):
        self.lst_stimes = []
        self.lst_etimes = []
        self.lst_works  = []
        for key, val in self.plan.items():
            self.lst_stimes.append(val.stime)
            self.lst_etimes.append(val.etime)
            self.lst_works.append(key)
    def handel_interference(self):
        self._list_time()
        offset = 0.1
        print(self.lst_etimes)
        print(self.lst_stimes)
        for ii in range(len(self.lst_works)):
            try:
                if (self.lst_stimes[ii] < self.lst_etimes[ii-1]) or (self.lst_etimes[ii] > self.lst_stimes[ii+1]):
                    self.plan[self.lst_works[ii]].offset = offset
            except:
                pass
            # self.interface1 = [val.stime < etime for etime in self.lst_etimes]
            # self.interface2 = [val.etime > stime for stime in self.lst_stimes]
            # if any(self.interface1) or any(self.interface2):
                # offset += 0.1
                # val.offset = offset
            
            
    def plot(self):
        dic = {name: (time.etime-time.stime).seconds / (24*3600) for name, time in self.plan.items()}
        print(dic)
        # fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        # wedges, texts, autotexts = ax.pie(dic.values(), autopct=dic.keys(),
        #                                   textprops=dict(color="w"))
        
        fig, ax = plt.subplots()
        plt.title(self.day_name)
        ax.pie(dic.values(), labels=dic.keys(), autopct='%1.1f%%',
                startangle=270, normalize=False)

        plt.show()