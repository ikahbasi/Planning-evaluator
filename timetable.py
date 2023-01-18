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


class Week:
    def __init__(self):
        self.Saturday = Day('Saturday', 0)
        self.Sunday = Day('Sunday', 1)
        self.Monday = Day('Monday', 2)
        self.Tuesday = Day('Tuesday', 3)
        self.Wednesday = Day('Wednesday', 4)
        self.Thursday = Day('Thursday', 5)
        self.Friday = Day('Friday', 6)
        
    def listing_actions(self):
        listactions = []
        for name, day in self.__dict__.items():
            for action, time in day.plan.items():
                listactions.append(action)
        return listactions
    
    def mk_cmap_actions(self):
        actions = list(set(self.listing_actions()))
        cmap = plt.cm.get_cmap('PiYG', len(actions))    # 11 discrete colors
        # cmap = plt.cm.get_cmap('Spectral')
        cmap = {action:cmap(indx) for indx, action in enumerate(actions)}
        return cmap
                
    def plot(self):
        import matplotlib.dates as mdates
        fig, ax = plt.subplots(figsize=(10, 7))
        cmap = self.mk_cmap_actions()
        for name, day in self.__dict__.items():
            day.handel_interference()
            print(name, day.day_name)
            for action, time in day.plan.items():
                print(action, time)
                y = day.day_number
                plt.plot((time.stime, time.etime), (y+time.offset, y+time.offset), linewidth=20, c=cmap[action])
                plt.text(time.stime,
                          y+time.offset,
                          action,
                           horizontalalignment='right',
                          verticalalignment='center',
                          rotation=90,
                          # c=cmap[action],
                          # backgroundcolor='k',
                          size='x-small'
                          )
                # plt.hlines(y=self.Saturday.day_number,
                #            xmin=time.stime,
                #            xmax=time.etime,
                #            linewidth=2, label=action)
        # plt.legend()
        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)
        # beautify the Y-labels
        ylabels = [name for name, day in self.__dict__.items()]
        ax.set_yticks(range(7))
        ax.set_yticklabels(ylabels, minor=False, rotation=0)
        # plt.xlim([Time(day=1, hour=0, minute=0, second=0, year=2023, month=1),
        #           Time(day=1, hour=23, minute=59, second=0, year=2023, month=1)])
        plt.show()
    def pie(self):
        for name, day in self.__dict__.items():
            print(name, day.day_name)
            day.plot()
            
    def update_routine(self, routine, except_day=[]):
        for name, day in self.__dict__.items():
            if name in except_day:
                continue
            day.plan.update(routine)
    def update_plans(self, plans):
        for keys, vals in plans.items():
            self.__dict__[keys].plan.update(vals)