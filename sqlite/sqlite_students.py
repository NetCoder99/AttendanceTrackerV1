import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory


# ------------------------------------------------------------------
def GetSqliteStudents():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetStudentRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows


def GetStudentRecordsStmt(badgeNumber = None):
    return '''
        SELECT s.badgeNumber,
               s.firstName,
               s.lastName,
               s.namePrefix,
               s.email,
               s.address,
               s.address2,
               s.city,
               s.country,
               s.state,
               s.zip,
               s.birthDate,
               s.phoneHome,
               s.phoneMobile,
               s.status,
               s.memberSince,
               s.gender,
               s.currentRank,
               s.ethnicity,
               --s.studentImageBytes,
               s.studentImagePath,
               s.studentImageBase64,
               s.middleName,
               s.studentImageName,
               s.studentImageType,
               s.currentRankName,
               b.beltTitle
        FROM students  s
        left join belts b
            on s.currentRank = b.beltId
    '''