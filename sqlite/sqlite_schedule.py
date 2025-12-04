import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory
from datetime import datetime
# ------------------------------------------------------------------
def GetClassRecordsSorted():
    classRecords = GetClassRecords()
    for classRecord in classRecords:
        date_string = "01-Jan-1980 " + classRecord['classStartTime']
        format_string = "%d-%b-%Y %I:%M %p"
        datetimeObject = datetime.strptime(date_string, format_string)
        try:
            classRecord['sortKey'] = datetimeObject.timestamp()
        except Exception as ex:
            print(f'ex: {ex.__str__()}')

    try:
        sorted_data = sorted(classRecords, key=lambda x: (x['classDayOfWeek'], x['sortKey']))
    except Exception as ex:
        print(f'ex: {ex.__str__()}')

    return sorted_data

# ------------------------------------------------------------------
def GetClassRecords():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetClassRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows


def GetClassRecordsStmt():
    return '''
        SELECT c.classNum,
               c.className,
               c.styleNum,
               c.styleName,
               c.classDayOfWeek,
               c.classStartTime,
               c.classFinisTime,
               c.classDuration,
               c.allowedRanks,
               c.classDisplayTitle,
               c.allowedAges,
               c.classCheckinStart,
               c.classCheckInFinis,
               v.dayName
          FROM classes c
          join vw_days_of_week v
            on c.classDayOfWeek = v.dayOfWeek
          order by c.classDayOfWeek; 
    '''