from sqlalchemy import select

import constants
from blueprints.students.sqlite_students import GetStudentRecordsStmtByBadge
from models import Students, Classes, Attendance
from sqlite.sqlite_alchemy import getDbSession
from sqlite.sqlite_procs import GetDataWithArgs
from datetime import datetime

# ------------------------------------------------------------------------------------------
db_session = getDbSession()

def GetPromotionMessage(badge_number):
    studentData       = GetDataWithArgs(GetStudentRecordsStmtByBadge(), {'badgeNumber': badge_number})
    print(f'studentData: {studentData}')
    return ""


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

def UpdPromotionDateStmt():
    return '''
        update promotions
        set    promotionDate  = :promotionDate,
               updateDateTime = :promotionDate
        where  promotionId    = :promotionId
    '''

# --------------------------------------------------------------------
# Insert the attendance checkin record
# --------------------------------------------------------------------
def InsertAttendanceRecord(student_record: Students, class_record: Classes, checkin_datetime: datetime):
    try:
        day_of_week = checkin_datetime.weekday() + 1
        checkinDateTimeStr = checkin_datetime.strftime(constants.fmtDateTime)
        checkinDateStr     = checkin_datetime.strftime(constants.fmtDate)
        checkinTimeStr     = checkin_datetime.strftime(constants.fmtTime)

        attendance_record = Attendance()
        attendance_record.badgeNumber       = student_record.badgeNumber
        attendance_record.checkinDayOfWeek  = day_of_week
        attendance_record.checkinDateTime   = checkinDateTimeStr
        attendance_record.checkinDate       = checkinDateStr
        attendance_record.checkinTime       = checkinTimeStr

        attendance_record.studentFirstName  = student_record.firstName
        attendance_record.studentLastName   = student_record.lastName
        attendance_record.studentRankNum    = student_record.currentRankNum
        attendance_record.studentRankName   = student_record.currentRankName
        attendance_record.studentStripeId   = student_record.currentStripeId
        attendance_record.studentStripeName = student_record.currentStripeName
        if class_record:
            attendance_record.classNum         = class_record.classNum
            attendance_record.className        = class_record.className
            attendance_record.classStartTime   = class_record.classStartTime
            attendance_record.styleNum         = class_record.styleNum
            attendance_record.appliesPromotion = class_record.isPromotions
        db_session.add(attendance_record)
        db_session.commit()
    except Exception as ex:
        print(f'{str(ex)}')
        raise ex

def GetAttendanceRecord(badge_number: int, checkin_datetime: datetime):
    select_stmt = select(Attendance).where(
        Attendance.badgeNumber     == badge_number,
        Attendance.checkinDateTime == checkin_datetime.strftime(constants.fmtDateTime)
    )
    results = db_session.scalars(select_stmt).all()
    return results
