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
        SELECT classNum,
               className,
               styleNum,
               styleName,
               classDayOfWeek,
               classStartTime,
               classFinisTime,
               classDuration,
               allowedRanks,
               classDisplayTitle,
               allowedAges,
               classCheckinStart,
               classCheckInFinis
        FROM classes
    '''