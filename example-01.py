from timetable import Week
import pandas as pd

fname = 'Plans.csv'
plans_all = pd.read_csv(fname)

routines = plans_all[plans_all['day']=='Routine']
routines = [tuple(action[1:]) for action in routines.values.tolist()]


plans = plans_all[plans_all['day']!='Routine']
plans = [tuple(action) for action in plans.values.tolist()]

week = Week()
week.update_routine(routines)#, except_day=['Thursday', 'Friday'])
week.update_plans(plans)


# routines = pd.read_csv('/home/iman/Dropbox/plan-project/Planning-evaluator/Plans/routines.csv')

# daily_routine1 = [('Sleep', '00:00:00', '06:45:00'),
#                   ('Weakup', '06:45:00', '07:00:00'),
#                   ('Breakfast 1', '07:00:00', '07:30:00'),
#                   ('Breakfast 2', '09:00:00', '09:15:00'),
#                   ('Launch', '12:45:00', '13:45:00'),
#                   ('Tea time', '15:30:00', '16:30:00'),
#                   ('Dinner', '20:30:00', '21:00:00'),
#                   ('BUSUU', '21:00:00', '22:00:00'),
#                   ]

# daily_routine2 = [('Go out', '07:30:00', '09:00:00'),
#                  ('Go back', '18:00:00', '19:30:00'),
#                  ('Rest', '19:30:00', '20:30:00')
#                  ]


# study_routine = [('Learning DL', (9, 30, 0), (10, 30, 0)),
#                 ]

# python_class = [('Python Class', (10, 0, 0), (12, 00, 0)),
#                 ('Python Class', (20, 0, 0), (22, 00, 0)),
#                 ('Python Class', (16, 0, 0), (18, 00, 0)),]


# entertainment = [('go out', (10, 0, 0), (12, 00, 0)),
#                  ('Python Class', (20, 0, 0), (22, 00, 0)),
#                  ('Python Class', (16, 0, 0), (18, 00, 0)),]


# week = Week()
# week.update_routine(daily_routine1, except_day=[])
# week.update_routine(daily_routine2, except_day=['Thursday', 'Friday'])
# week.update_plans(python_class, target_day=['Friday'])
# week.Monday.add_plan('4 Friends', ())
# week.update_routine(study_routine)
week.plot_timetable()
week.pie_plot()
week.weekly_pie_plot()
