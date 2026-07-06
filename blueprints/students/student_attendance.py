def GetAttendanceByBadgeStmt(badge_number):
    return '''
        select date(a.checkinDateTime), 
               date('2025-07-06 15:30:22'),
               d.dayName,
               a.* 
        from   attendance a
        left   join   vw_days_of_week d
          on   a.checkinDayOfWeek = d.dayOfWeek
        where  a.badgeNumber = :badge_number
        and    date(a.checkinDateTime) > date('2026-03-06 15:30:22')
        order  by date(a.checkinDateTime) desc
    '''