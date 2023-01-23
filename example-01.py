from timetable import Week
import pandas as pd

fname = 'Plans.csv'
plans_all = pd.read_csv(fname, dtype=str)

week = Week()
week.update_plans(plans_all)


week.plot_timetable()
week.pie_plot()
week.weekly_pie_plot()
