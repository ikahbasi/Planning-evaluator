from timetable import ToDo, Week

daily_routine = [ToDo('Sleep', (0, 0, 0), (6, 45, 0)),
                 ToDo('Weakup', (6, 45, 0), (7, 00, 0)),
                 ToDo('Breakfast 1', (7, 00, 0), (7, 30, 0)),
                 ToDo('Go out', (7, 30, 0), (9, 00, 0)),
                 ToDo('breakfast 2', (9, 00, 0), (9, 15, 0)),
                 ToDo('launch', (12, 45, 0), (13, 45, 0)),
                 ToDo('Tea time', (15, 30, 0), (16, 30, 0)),
                 ToDo('go back', (18, 00, 0), (19, 30, 0)),
                 ToDo('rest', (19, 30, 0), (20, 30, 0)),
                 ToDo('Dinner', (20, 30, 0), (21, 00, 0)),
                 ToDo('BUSUU', (21, 00, 0), (23, 59, 0)),
                 ]

study_routine = [ToDo('Learning DL', (9, 30, 0), (10, 30, 0)),
                 ToDo('Busuu', (22, 0, 0), (22, 30, 0)),
                ]

week = Week()
week.update_routine(daily_routine, except_day=['Thursday', 'Friday'])
week.update_routine(study_routine)
week.plot_timetable()
week.pie_plot()
