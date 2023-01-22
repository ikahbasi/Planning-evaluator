from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
import pandas as pd

def Time(time, date='2023-01-01'):
    datetime_str = f'{date} {time}'
    return dt.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


class ToDo:
    def __init__(self, name, stime, etime):
        self.name = name
        self.stime = Time(stime)
        self.etime = Time(etime)
        self.offset = 0

def formattxt_pie(pct):
    hr = pct / 100 * 24
    return f'{pct:.1f}% ({hr:.1f} hr)'

def formattxt_pie_week(pct):
    hr = pct / 100 * 24 * 7
    return f'{pct:.1f}% ({hr:.1f} hr)'

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
                    # print(plan.name, plan.offset, plan.stime, plan.etime)
                    plan.offset = self.plans[indx-1].offset + 0.05
                # if (self.lst_stimes[ii] < self.lst_etimes[ii-1]) or (self.lst_etimes[ii] > self.lst_stimes[ii+1]):
                #     self.plan[self.lst_works[ii]].offset = offset
            except IndexError as error:
                print(error)
            
            
    def pie_plot(self, colors=None):
        dic = {plan.name: (plan.etime-plan.stime).seconds / (24*3600) for plan in self.plans}
        free_time = 1 - sum(dic.values())
        dic.update({'Free Time': free_time})
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.title(self.day_name)
        patches, labels, pct_texts = ax.pie(
            dic.values(), labels=dic.keys(),
            autopct=lambda pct: formattxt_pie(pct),#'%1.1f%%',
            startangle=90, normalize=False, colors=colors+[(0.8, 1, 1)], rotatelabels=True,
            pctdistance=0.7)
        for label, pct_text in zip(labels, pct_texts):
            rotation = label.get_rotation()
            pct_text.set_rotation(rotation)
        plt.show()

    def makedf(self):
        #
        dictionary = {'name': [plan.name for plan in self.plans],
                      'Start Time': [plan.stime.strftime("%H:%M:%S") for plan in self.plans],
                      'End Time': [plan.etime.strftime("%H:%M:%S") for plan in self.plans]}
        df = pd.DataFrame(dictionary)
        return df
    def __str__(self):
        txt = self.day_name + '\n'
        txt += self.makedf().to_string()
        return txt
    
    def _sort_plans(self):
        self.plans = sorted(self.plans, key=lambda plan: plan.stime)
        
    def add_action(self, name, stime, etime):
        action = ToDo(name, stime, etime)
        self.plans.append(action)

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
            # print(day)
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
            plt.plot_date((Time('00:00:00'), Time('23:59:59')),
                          (y, y),
                          linewidth=1, c='k',
                          fmt=':')
            day.handel_interference()
            for plan in day.plans:
                # print('plot', plan.name, plan.offset)
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
        plt.xlim([Time('00:00:00'), Time('23:59:59')])
        plt.legend(handles=self.color_patch, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()


    def pie_plot(self):
        for name, day in self.__dict__.items():
            if isinstance(day, Day):
                colors = [self.cmap[plan.name] for plan in day.plans]
                day.pie_plot(colors=colors)
    
    
    def weekly_pie_plot(self):
        works = {}
        for name, day in self.__dict__.items():
            if isinstance(day, Day):
                for plan in day.plans:
                    if plan.name not in works.keys():
                        works[plan.name] = (plan.etime-plan.stime).seconds / (7*24*3600)
                    else:
                        works[plan.name] += (plan.etime-plan.stime).seconds / (7*24*3600)
        # cmap = plt.cm.get_cmap('Spectral')
        names = works.keys()
        times = works.values()
        colors = [self.cmap[name] for name in names]
        free_time = 1 - sum(times)
        works.update({'Free Time': free_time})
        #
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.title('All Week')
        patches, labels, pct_texts = ax.pie(
            times, labels=names,
            autopct=lambda pct: formattxt_pie_week(pct),#'%1.1f%%',
            startangle=90, normalize=False, colors=colors+[(0.8, 1, 1)], rotatelabels=True,
            pctdistance=0.7)
        for label, pct_text in zip(labels, pct_texts):
            rotation = label.get_rotation()
            pct_text.set_rotation(rotation)
        plt.show()
        
        


    def update_routine(self, routines, except_day=[]):
        for name, day in self.__dict__.items():
            if name in except_day:
                continue
            for action in routines:
                day.add_action(*action)
        self._sort_plans()


    def update_plans(self, plans):
        for plan in plans:
            day = plan[0]
            action = plan[1:]
            exec(f"self.{day}.add_action(*{action})")
        self._sort_plans()

    
    def _sort_plans(self):
        for name, day in self.__dict__.items():
            day._sort_plans()
