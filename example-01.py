from timetable import ToDo, Week

routine = [ToDo('Sleep', (0, 0, 0), (6, 45, 0)),
           ToDo('Weakup', (6, 43, 0), (7, 00, 0)),
           ToDo('Breakfast 1', (7, 00, 0), (7, 30, 0)),
           ToDo('Go out', (7, 30, 0), (9, 00, 0)),
           ToDo('breakfast 2', (9, 00, 0), (9, 15, 0)),
           ToDo('launch', (12, 45, 0), (13, 45, 0)),
           ToDo('go back', (18, 00, 0), (19, 30, 0)),
           ToDo('rest', (19, 30, 0), (20, 00, 0))
           ]

week = Week()
week.update_routine(routine, except_day=['Thursday', 'Friday'])

plans = {'Saturday': [],
         'Sunday': [],
         'Monday': [
             ToDo('4 Friends meeting', (20, 30, 0), (22, 15, 0)),
             ToDo('Go back home', (22, 15, 0), (23, 00, 0)),
             ],
         'Tuesday': [],
         'Wednesday': [
            ToDo('DL meeting', (14, 00, 0), (17, 30, 0)),
             ],
         'Thursday': [],
         'Friday': []
         }
week.update_plans(newplans=plans)

week.plot_timetable()
# week.pie_plot()
