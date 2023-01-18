from timetable import ToDo, Week

routine = {'sleep':  ToDo((0, 0, 0),
                          (6, 45, 0)),
           
            'weakup': ToDo((6, 45, 0),
                           (7, 00, 0)),
                      
            'breakfast 1':  ToDo((7, 00, 0),
                                 (7, 30, 0)),
            
           'go out':  ToDo((7, 30, 0),
                           (9, 00, 0)),
           
           'breakfast 2':  ToDo((9, 00, 0),
                                (9, 15, 0)),
           
           'launch': ToDo((12, 45, 0),
                          (13, 45, 0)),
           
           'go back':  ToDo((18, 00, 0),
                            (19, 30, 0)),
           
           'rest':  ToDo((19, 30, 0),
                         (20, 00, 0))
           }

week = Week()
week.update_routine(routine, except_day=['Thursday', 'Friday'])

plans = {'Saturday': {
             },
         'Sunday': {
             },
         'Monday':{
             '4 Friends meeting':  ToDo((20, 30, 0),
                                        (22, 15, 0)),
             },
         'Tuesday':{
             },
         'Wednesday':{
             'breakfast 1':  ToDo((9, 00, 0),
                                  (9, 15, 0)),
             'DL meeting':  ToDo((14, 00, 0),
                                 (17, 30, 0)),
             },
         'Thursday':{
             },
         'Friday':{
             }
         }
week.update_plans(plans=plans)

week.plot()
week.pie()
