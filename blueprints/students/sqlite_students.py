import re
import sqlite3

from services.config import getDbPath
from sqlite.sqlite_procs import DictFactory


# ------------------------------------------------------------------
def GetSqliteStudents():
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(GetStudentRecordsStmt())
        rows = cursor.fetchall()
        dbObj.close()
        return rows
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

def GetStudentRecordsStmt(badgeNumber = None):
    return '''
        with cte_default_image as (
          select a.imageId,
                 a.imageName,
                 a.imageType,
                 a.imageBase64
          from  assets a
          where a.imageId = 428
        )    
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
               s.middleName,
               s.currentRankName,
               b.beltTitle,
               case when s.studentImageBase64 is not null
                    then s.studentImageBase64 
                    else (select imageBase64 from cte_default_image)
               end as studentImageBase64,   
               case when s.studentImageBase64 is not null
                    then s.studentImageName 
                    else (select imageName from cte_default_image)
               end as studentImageName,   
               case when s.studentImageBase64 is not null
                    then s.studentImageType 
                    else (select imageType from cte_default_image)
               end as studentImageType   
        FROM students  s
        left join belts b
            on s.currentRank = b.beltId
    '''

# ------------------------------------------------------------------
def UpdStudentRecord(studentRecord):
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(UpdStudentRecordStmt(), studentRecord)
        dbObj.commit()
        rows = cursor.fetchall()
        dbObj.close()
        return rows
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

def UpdStudentRecordStmt():
    return '''
        UPDATE students
        SET    firstName   = :frmFirstName,
               lastName    = :frmLastName,
               address     = :frmAddress,
               address2    = :frmAddress2,
               city        = :frmCity,
               state       = :frmState,
               zip         = :frmZip,
               birthDate   = :frmBirthDate,
               phoneHome   = :frmPhoneHome,
               email       = :frmEmail
        WHERE  badgeNumber = :badgeNumber
    '''


# '''
# 'frmFirstName' = {str} 'Daffy'
# 'frmLastName' = {str} 'Duck'
# 'frmAddress' = {str} '100 Looney Lane'
# 'frmAddress2' = {str} ''
# 'frmCity' = {str} 'Cartoon Town'
# 'frmState' = {str} ''
# 'frmZip' = {str} ''
# 'frmBirthDate' = {str} '06/02/2025'
# 'frmPhoneHome' = {str} ''
# 'frmEmail' = {str} ''
# 'badgeNumber' = {str} '100'
# __len__ = {int} 11
#        firstName = 'firstName',
#        lastName = 'lastName',
#        namePrefix = 'namePrefix',
#        email = 'email',
#        address = 'address',
#        address2 = 'address2',
#        city = 'city',
#        country = 'country',
#        state = 'state',
#        zip = 'zip',
#        birthDate = 'birthDate',
#        phoneHome = 'phoneHome',
#        phoneMobile = 'phoneMobile',
#        status = 'status',
#        memberSince = 'memberSince',
#        gender = 'gender',
#        currentRank = 'currentRank',
#        ethnicity = 'ethnicity',
#        studentImageBytes = 'studentImageBytes',
#        studentImagePath = 'studentImagePath',
#        studentImageBase64 = 'studentImageBase64',
#        middleName = 'middleName',
#        studentImageName = 'studentImageName',
#        studentImageType = 'studentImageType',
#        currentRankName = 'currentRankName'
#        '''
# ------------------------------------------------------------------
def UpdStudentPicture(pictureDetails):
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(UpdStudentPictureStmt(pictureDetails))
    dbObj.commit()
    rows = cursor.fetchall()
    dbObj.close()
    return rows

def UpdStudentPictureStmt(pictureDetails):
    pattern = r"(data:image/)(.+)(;)"
    match = re.search(pattern, pictureDetails['fileBase64'])
    studentImageType = match.groups()[1]
    studentImageParts = pictureDetails['fileBase64'].split(',')
    return f'''
        update students
        set    studentImageName    = '{pictureDetails['file_name']}',
               studentImageType    = '{studentImageType}',
               studentImageBase64  = '{studentImageParts[1]}'
        WHERE badgeNumber = '{pictureDetails['badgeNumber']}'
    '''
