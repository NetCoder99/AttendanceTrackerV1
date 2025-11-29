import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory


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