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

def GetStudentRecordsStmt():
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
               s.ethnicity,
               s.middleName,
               s.currentRankNum,
               s.currentRankName,
               s.crntStripeId,
               s.crntStripeName,
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
            on s.currentRankNum = b.beltId
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

def GetUpdateStudentRankStmt():
    return '''
        INSERT INTO promotions (
           badgeNumber,
           beltId,
           beltTitle,
           stripeId,
           stripeTitle,
           studentName,
           promotionDate
        )
        VALUES (
           :badgeNumber,
           :beltId,
           :beltTitle,
           :stripeId,
           :stripeTitle,
           :studentName,
           :promotionDate
        );
    '''

def GetPromotionHistoryStmt():
    return '''
        select p.promotionId,
           p.badgeNumber,
           p.beltId,
           p.beltTitle,
           p.stripeId,
           p.stripeTitle,
           p.studentName,
           p.promotionDate
        from   promotions  p
        where  p.badgeNumber = :badgeNumber
        order  by p.promotionId desc;
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
def UpdStudentPicture(pictureDetails, updateDict):
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(UpdStudentPictureStmt() ,updateDict)
    dbObj.commit()
    dbObj.close()

def UpdStudentPictureStmt():
    return f'''
        update students
        set    studentImageName    = :studentImageName,
               studentImageType    = :studentImageType,
               studentImageBase64  = :studentImageBase64
        where  badgeNumber = :badgeNumber
    '''

def GetStudentRecordsStmtByBadge():
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
        from students  s
        left join belts b
            on s.currentRank = b.beltId
        where s.badgeNumber  = :badgeNumber
    '''

def GetStripeNamesByRank():
    return '''
        select s.rankNum, 
               r.rankName,
               s.stripeId,
               s.stripeName
        from   stripes  s
        join   ranks    r
          on   s.rankNum = r.rankNum
        where  s.rankNum = :rankNum
        order  by s.rankNum, s.seqNum
    '''

def GetMinRankClassCounts():
    return '''
        select s.rankNum, 
               r.rankName,
               sum(s.classCount) as minClassCount
        from   stripes  s
        where  r.rankNum = :rankNum
        join   ranks    r
          on   s.rankNum = r.rankNum
        group  by s.rankNum
        order  by s.rankNum
    '''