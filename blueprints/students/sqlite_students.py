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
               s.memberSinceDate,
               s.gender,
               s.ethnicity,
               s.middleName,
               s.currentRankNum,
               s.currentRankName,
               s.currentStripeId,
               s.currentStripeName,
               b.beltTitle,
               s.createDateTime,
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
               s.ethnicity,
               s.middleName,
               s.currentRankNum,
               s.currentRankName,
               s.currentStripeId,
               s.currentStripeName,
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
            on s.currentRankNum = b.beltId
        where  s.badgeNumber    = :badgeNumber    
    '''

# ------------------------------------------------------------------
def InsStudentRecord(studentRecord):
    try:
        db_path = getDbPath()
        dbObj = sqlite3.connect(db_path)
        dbObj.row_factory = DictFactory
        cursor = dbObj.cursor()
        cursor.execute(InsStudentRecordStmt(), studentRecord)
        dbObj.commit()
        rows = cursor.fetchall()
        dbObj.close()
        return rows
    except Exception as ex:
        print(f'Error: {ex.__str__()}')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def InsStudentRecordStmt():
    return '''
        insert into students (
          badgeNumber,
          firstName,
          lastName,
          address,
          address2,
          city,
          state,
          zip,
          birthDate,
          phoneHome,
          email
        )
        values (
          :badgeNumber,
          :frmFirstName,
          :frmLastName,
          :frmAddress,
          :frmAddress2,
          :frmCity,
          :frmState,
          :frmZip,
          :frmBirthDate,
          :frmPhoneHome,
          :frmEmail
        )  
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

def UpdatePromotionsRankStmt():
    return '''
        INSERT INTO promotions (
           badgeNumber,
           beltId,
           beltTitle,
           stripeId,
           stripeTitle,
           studentFirstName,
           studentLastName,
           promotionDate,
           comments
        )
        VALUES (
           :badgeNumber,
           :beltId,
           :beltTitle,
           :stripeId,
           :stripeTitle,
           :studentFirstName,
           :studentLastName,
           :promotionDate,
           :comments
        );
    '''

def UpdateStudentRankStmt():
    return '''
        update students  
        set    currentRankNum    = :currentRankNum,
               currentRankName   = :currentRankName,
               currentStripeId   = :currentStripeId,
               currentStripeName = :currentStripeName
        where  badgeNumber       = :badgeNumber
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

def GetDefaultImageStmt():
    return f'''
        select imageId,
               imageName,
               imageBase64,
               imageBytes,
               imageType,
               createDateTime,
               updateDateTime
        from   assets
        where  imageName = :imageName
    '''

def GetDefaultStudentDataStmt():
    return f'''
        with cte_default_image as (
          select a.imageId,
                 a.imageName,
                 a.imageType,
                 a.imageBase64
          from  assets a
          where a.imageId = 428
        )   
        select max(badgeNumber) + 10 as badgeNumber,
          ''  as firstName,
          ''  as lastName,
          ''  as namePrefix,
          ''  as email,
          ''  as address,
          ''  as address2,
          ''  as city,
          ''  as country,
          ''  as state,
          ''  as zip,
          ''  as birthDate,
          ''  as phoneHome,
          ''  as phoneMobile,
          ''  as status,
          ''  as memberSince,
          ''  as gender,
          ''  as ethnicity,
          null as studentImageBytes,
          ''  as studentImagePath,
          (select imageBase64 from cte_default_image)  as studentImageBase64,
          ''  as middleName,
          (select imageName from cte_default_image)  as studentImageName,
          (select imageType from cte_default_image)  as studentImageType,
          0   as currentRankNum,
          ''  as currentRankName,
          0   as currentStripeId,
          ''  as currentStripeName,
          ''  as createDateTime
        from  students     
    '''

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

def GetDefatulStudentRecord():
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
               s.currentStripeId,
               s.currentStripeName,
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
        where s.badgeNumber  = :badgeNumber
    '''

def GetStripeNamesByRank():
    return '''
        select s.rankNum, 
               r.beltTitle,
               s.stripeId,
               s.stripeName
        from   stripes  s
        join   belts    r
          on   s.rankNum = r.beltId
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

def GetStudentAttendanceRecords():
    return '''
        select a.attendance_id,
               a.checkinDateTime,
               a.checkinDate,
               a.checkinTime,
               a.classNum,
               a.className,
               a.studentRankNum,
               a.studentRankName,
               a.appliesPromotion,
               c.classDayOfWeek
        from   attendance  a
        left   join   classes     c
          on   a.classNum    = c.classNum        
        where  a.badgeNumber = :badgeNumber
        order  by a.checkinDateTime desc
    '''