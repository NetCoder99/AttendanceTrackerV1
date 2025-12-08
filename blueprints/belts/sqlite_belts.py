import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory
from datetime import datetime

# ------------------------------------------------------------------
def GetRanksRecords():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetRanksRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows
def GetRanksRecordsStmt():
    return '''
        select r.rankNum,
               r.rankName,
               r.styleNum,
               r.styleName,
               r.imageSource,
               s.styleName
        from ranks  r
        left join styles s
          on r.styleNum = s.styleNum
        order by r.rankNum
    '''
# ------------------------------------------------------------------
def GetBeltsRecords():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetBeltsRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows
def GetBeltsRecordsStmt():
    return '''
        SELECT beltId,
               beltTitle,
               stripeTitle,
               classCount,
               imageSource
        FROM belts;
    '''
