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
               c.isPromotions,
               v.dayName
          FROM classes c
          join vw_days_of_week v
            on c.classDayOfWeek = v.dayOfWeek
          order by c.classDayOfWeek, c.classCheckinStart; 
    '''


# ------------------------------------------------------------------
def CheckForClassOverlap():
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetClassRecordsStmt())
    rows = cursor.fetchall()
    dbObj.close()
    return rows
def CheckForClassOverlapStmt():
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
               c.isPromotions,
               v.dayName
          FROM classes c
          join vw_days_of_week v
            on c.classDayOfWeek = v.dayOfWeek
          order by c.classDayOfWeek; 
    '''

# ------------------------------------------------------------------
def InsertNewClass(classDict):
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(InsertNewClassStmt(), classDict)
        dbObj.commit()
        dbObj.close()
    except Exception as ex:
        print(f'Error in InsertNewClass: {ex.__str__()}')
        raise ex
def InsertNewClassStmt():
    return '''
        INSERT INTO classes (
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
          isPromotions
        )
        VALUES (
          :className, 
          :styleNum, 
          :styleName, 
          :classDayOfWeek, 
          :classStartTime, 
          :classFinisTime, 
          :classDuration, 
          :allowedRanks, 
          :classDisplayTitle, 
          :allowedAges,
          :isPromotions
        )
    '''

# ------------------------------------------------------------------
def UpdateExistingClass(classDict):
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(UpdateExistingClassStmt(), classDict)
        dbObj.commit()
        dbObj.close()
    except Exception as ex:
        print(f'Error in InsertNewClass: {ex.__str__()}')
        raise ex
def UpdateExistingClassStmt():
    return '''
        update classes 
        set className         = :className, 
            styleNum          = :styleNum, 
            styleName         = :styleName, 
            allowedRanks      = :allowedRanks, 
            classDisplayTitle = :classDisplayTitle, 
            allowedAges       = :allowedAges,
            isPromotions      = :isPromotions
       where classNum         = :classNum            
    '''

# ------------------------------------------------------------------
def DeleteClass(classDict):
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(DeleteClassStmt(), classDict)
        rowCount = cursor.rowcount
        dbObj.commit()
        dbObj.close()
        return rowCount
    except Exception as ex:
        print(f'Error in InsertNewClass: {ex.__str__()}')
        raise ex

def DeleteClassStmt():
    return '''
        delete from classes
        where  classNum = :classNum 
    '''