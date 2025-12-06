import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory


def GetStyleRecords():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetStyleRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows


def GetStyleRecordsStmt():
    return '''
        SELECT styleNum,
               styleName
        FROM styles;
    '''