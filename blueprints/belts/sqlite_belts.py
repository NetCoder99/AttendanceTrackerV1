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
        select b.beltId     as rankNum,
               b.beltTitle  as rankName,
               s.styleNum,
               s.styleName,
               b.imageSource
        from   belts b
        left   join styles s
          on   b.styleNum = s.styleNum
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

# ------------------------------------------------------------------
def GetStripeRecords(searchData):
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetStripeRecordsStmt(), searchData)
    rows = cursor.fetchall()
    dbObj.close()
    return rows
def GetStripeRecordsStmt():
    return '''
        with cte_classCount as (
          select 5 as rankClassCount 
        )
        select s.stripeId,
               s.stripeName,
               s.rankNum,
               s.seqNum,
               c.rankClassCount,
               s.seqNum *  c.rankClassCount as stripeClassCount,
               r.beltTitle,
               (
                 select max(s1.seqNum)
                 from   stripes  s1
                 where  s1.rankNum = r.beltId
               ) as maxSeqNum,
               case when                (
                 select max(s1.seqNum)
                 from   stripes  s1
                 where  s1.rankNum = r.beltId
               ) = s.seqNum 
               then true else false end as lastStripeFlag
        from   stripes  s
        join   belts    r
          on   s.rankNum = r.beltId
        join   cte_classCount c  
        where  s.rankNum = :rankNum
        order  by s.seqNum;
    '''

# ------------------------------------------------------------------
def GetNextStripeName(searchData):
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(GetNextStripeNameStmt(), searchData)
    rows = cursor.fetchall()
    dbObj.close()
    return rows
def GetNextStripeNameStmt():
    return '''
        with cteCurrentMaxStripe as (
            select b1.beltId,
                   b1.beltTitle,
                   b1.stripeTitle,
                   b1.classCount,
                   (
                     select ifnull(max(seqNum), 0)
                     from   stripes s1
                     where  s1.rankNum = b1.beltId
                    ) as maxStripeId
            from   belts  b1
            where  b1.beltId = :rankNum
        )
        select cte.beltId                                as rankNum, 
               sp.stripePrefix || ' ' || cte.stripeTitle as stripeName,
               cte.classCount * sp.stripePrefixSeq       as stripeClassCount,
               sp.stripePrefixSeq                        as seqNum
        from   stripePrefixes       sp
        join   cteCurrentMaxStripe  cte
          on   sp.stripePrefixSeq = cte.maxStripeId + 1
    '''

# ------------------------------------------------------------------
def InsStripeRecord(insertData) -> int:
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    lastRowId = cursor.execute(InsStripeRecordStmt(), insertData)
    dbObj.commit()
    dbObj.close()
    return lastRowId.lastrowid
def InsStripeRecordStmt():
    return '''
        INSERT INTO stripes (
          stripeName,
          rankNum,
          classCount,
          seqNum
        ) 
        VALUES (
          :stripeName,
          :rankNum,
          :classCount,
          :seqNum
        )
    '''

# ------------------------------------------------------------------
def DelStripeRecord(deleteData):
    db_path = getDbPath()
    dbObj = sqlite3.connect(db_path)
    dbObj.row_factory = DictFactory
    cursor = dbObj.cursor()
    cursor.execute(DelStripeRecordStmt(), deleteData)
    dbObj.commit()
    dbObj.close()
def DelStripeRecordStmt():
    return '''
        delete from stripes
        where  stripeId = :stripeId
    '''

# select *
# from   stripes s
# where  s.stripeId = 22
