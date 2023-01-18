from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 


def Time(hour, minute, second, year=2023, month=1, day=1):
    return dt(year, month, day, hour, minute, second)


class ToDo:
    def __init__(self, name, stime, etime):
        self.name = name
        self.stime = Time(*stime)
        self.etime = Time(*etime)
        self.offset = 0


class Day:
    def __init__(self, day_name, day_number):
        self.day_name = day_name
        self.day_number = day_number
        self.plans = []

    def _list_plans(self):
        self.lst_stimes = [plan.stime for plan in self.plans]
        self.lst_etimes = [plan.etime for plan in self.plans]
        self.lst_works  = [plan.name for plan in self.plans]

    def handel_interference(self):
        self._list_plans()
        for indx, plan in enumerate(self.plans):
            if indx == 0:
                continue
            try:
                if (plan.stime < self.plans[indx-1].etime) or (plan.etime > self.plans[indx+1].stime):
                    plan.offset = self.plans[indx-1].offset + 0.05
                # if (self.lst_stimes[ii] < self.lst_etimes[ii-1]) or (self.lst_etimes[ii] > self.lst_stimes[ii+1]):
                #     self.plan[self.lst_works[ii]].offset = offset
            except Exception as error:
                print(error)
            
            
    def pie_plot(self, colors=None):
        dic = {plan.name: (plan.etime-plan.stime).seconds / (24*3600) for plan in self.plans}
        # print(dic)
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.title(self.day_name)
        ax.pie(dic.values(), labels=dic.keys(), autopct='%1.1f%%',
                startangle=270, normalize=False, colors=colors)
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
        
    def listing_all_works(self):
        self.lst_works = set()
        for name, day in self.__dict__.items():
            print(day)
            if isinstance(day, Day):
                day._list_plans()
                self.lst_works.update(day.lst_works)
        self.lst_works = list(self.lst_works)
    
    def mk_cmap_actions(self):
        self.listing_all_works()
        cmap = plt.cm.get_cmap('hsv', len(self.lst_works))    # 11 discrete colors
        # cmap = plt.cm.get_cmap('Spectral')
        self.cmap = {action:cmap(indx) for indx, action in enumerate(self.lst_works)}
        self.color_patch = [mpatches.Patch(color=color, label=action) for action, color in self.cmap.items()]
                
    def plot_timetable(self):
        import matplotlib.dates as mdates
        fig, ax = plt.subplots(figsize=(10, 7))
        self.mk_cmap_actions()
        for name, day in self.__dict__.items():
            if not isinstance(day, Day):
                continue
            y = day.day_number
            plt.plot_date((Time(day=1, hour=0, minute=0, second=0, year=2023, month=1),
                           Time(day=1, hour=23, minute=59, second=0, year=2023, month=1)),
                          (y, y),
                          linewidth=1, c='k',
                          fmt=':')
            day.handel_interference()
            for plan in day.plans:
                plt.plot_date((plan.stime, plan.etime),
                              (y+plan.offset, y+plan.offset),
                              linewidth=3, c=self.cmap[plan.name],
                              fmt='-', label=plan.name)
                plt.text(plan.stime,
                          y+plan.offset+0.05,
                          plan.name,
                          # horizontalalignment='right',
                          # verticalalignment='center',
                          rotation=90,
                          # c=cmap[action],
                          # backgroundcolor='k',
                          size='x-small'
                          )
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)
        # beautify the Y-labels
        ylabels = [name for name, day in self.__dict__.items() if isinstance(day, Day)]
        # print(ylabels)
        ax.set_yticks(range(7))
        ax.set_yticklabels(ylabels, minor=False, rotation=0)
        plt.xlim([Time(day=1, hour=0, minute=0, second=0, year=2023, month=1),
                  Time(day=1, hour=23, minute=59, second=0, year=2023, month=1)])
        plt.legend(handles=self.color_patch, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()


    def pie_plot(self):
        for name, day in self.__dict__.items():
            print(name, day.day_name)
            colors = [self.cmap[plan.name] for plan in day.plans]
            day.pie_plot(colors=colors)


    def update_routine(self, routine, except_day=[]):
        for name, day in self.__dict__.items():
            if name in except_day:
                continue
            day.plans += routine


    def update_plans(self, newplans):
        for keys, vals in newplans.items():
            self.__dict__[keys].plans += vals