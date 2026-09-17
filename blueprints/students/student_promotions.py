import sys
from datetime import datetime

from sqlalchemy import text, select, func

import constants
from models.data_models import Students, Attendance, Requirements, Promotions
from models.output_models import StudentRankFields
from sqlite.sqlite_alchemy import getDbSession

db_session = getDbSession()

def rows_as_dicts(cursor):
    """convert tuple result to dict with cursor"""
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]

def GetNextPromotion(badge_number):
    try:
        query  = text(GetNextPromotionStmt())
        result = db_session.execute(query, {'badgeNumber' : badge_number})
        for row in result.mappings():
            return row
        raise Exception('No rows found!')
    except Exception as ex:
        print(f'{str(ex)}', file=sys.stderr)

def GetNextPromotionStmt():
    return '''
            with cte_current_requirement_id as
            (
                select r1.promotionSeqNum
                from   students s1
                join   requirements r1
                  on   s1.currentRankNum  = r1.beltId
                  and  s1.currentStripeId = r1.stripeId
                where  s1.badgeNumber = :badgeNumber
            )
            select requirementId,
                beltId,
                beltTitle,
                stripeId,
                stripeTitle,
                stripeSeqNum,
                classesCount,
                requiredClasses,
                promotionSeqNum,
                createDateTime,
                updateDateTime
            from   requirements r2
            where  r2.promotionSeqNum > (select promotionSeqNum from cte_current_requirement_id)
            order  by r2.promotionSeqNum asc
            limit  1
        '''

def GetNextStudentRank(student_record: Students) -> StudentRankFields:
    try:
        # if rank and stripe are set on the student record then find the next
        # promotion / requirement type
        if student_record.currentRankNum and student_record.currentStripeId:
            next_student_rank = GetNextFromCurrent(student_record)
            return next_student_rank

        # if both rank and stripe are 'None' then check for a promotion record, use that if found
        last_promotion_record = GetLastPromotionRecord(student_record.badgeNumber)
        if last_promotion_record:
            next_student_rank = GetNextFromLastPromotion(last_promotion_record)
            return next_student_rank

        # not set on student record and no promotion history, use total classes attended
        next_student_rank = GetBasedOnAttendanceTotalCount(student_record)
        return next_student_rank

    except Exception as ex:
        print(f'Error: {str(ex)}')
        raise ex

# ---------------------------------------------------------------------------------------
def GetNextFromCurrent(student_record: Students) -> StudentRankFields:
    try:
        next_student_rank = StudentRankFields.construct()
        crnt_requirement_stmt = (select(Requirements)
                                 .where(Requirements.beltId == student_record.currentRankNum)
                                 .where(Requirements.stripeId == student_record.currentStripeId)
                                 .order_by(Requirements.promotionSeqNum))
        crnt_requirement_id = db_session.scalars(crnt_requirement_stmt).first().requirementId
        next_requirement_stmt = ((select(Requirements)
                                  .where(Requirements.requirementId > crnt_requirement_id))
                                 .order_by(Requirements.promotionSeqNum))
        next_requirement_record = db_session.scalars(next_requirement_stmt).first()

        next_student_rank.currentRankNum = next_requirement_record.beltId
        next_student_rank.currentRankName = next_requirement_record.beltTitle
        next_student_rank.currentStripeId = next_requirement_record.stripeId
        next_student_rank.currentStripeName = next_requirement_record.stripeTitle
        next_student_rank.studentPromotionDate = datetime.now().strftime(constants.fmtDateTime)
        next_student_rank.rankMessage = "From current rank"
        return next_student_rank
    except Exception as ex:
        print(f'Error: {str(ex)}')
        raise ex

def GetNextFromLastPromotion(last_promotion_record: Promotions) -> StudentRankFields:
    try:
        next_student_rank = StudentRankFields.construct()
        crnt_requirement_stmt = (select(Requirements)
                                 .where(Requirements.beltId == last_promotion_record.beltId)
                                 .where(Requirements.stripeId == last_promotion_record.stripeId)
                                 .order_by(Requirements.promotionSeqNum))
        crnt_requirement_id = db_session.scalars(crnt_requirement_stmt).first().requirementId

        next_requirement_stmt = ((select(Requirements)
                                  .where(Requirements.requirementId > crnt_requirement_id))
                                 .order_by(Requirements.promotionSeqNum))
        next_requirement_record = db_session.scalars(next_requirement_stmt).first()

        next_student_rank.currentRankNum = next_requirement_record.beltId
        next_student_rank.currentRankName = next_requirement_record.beltTitle
        next_student_rank.currentStripeId = next_requirement_record.stripeId
        next_student_rank.currentStripeName = next_requirement_record.stripeTitle
        next_student_rank.studentPromotionDate = next_requirement_record.promotionDate
        next_student_rank.rankMessage = "From last promotion"
        return next_student_rank
    except Exception as ex:
        print(f'Error: {str(ex)}')
        raise ex

def GetBasedOnAttendanceTotalCount(student_record: Students) -> StudentRankFields:
    try:
        next_student_rank = StudentRankFields.construct()
        attendance_total_stmt = (select(func.count())
                                 .select_from(Attendance)
                                 .where(Attendance.badgeNumber == student_record.badgeNumber))
        attendance_count_total = db_session.scalar(attendance_total_stmt)
        requirement_record = (
            db_session.scalars(select(Requirements)
                               .where(Requirements.requiredClasses <= attendance_count_total)
                               .order_by(Requirements.beltId.desc(), Requirements.promotionSeqNum.desc()))
            .first()
        )
        next_student_rank.currentRankNum = requirement_record.beltId
        next_student_rank.currentRankName = requirement_record.beltTitle
        next_student_rank.currentStripeId = requirement_record.stripeId
        next_student_rank.currentStripeName = requirement_record.stripeTitle
        next_student_rank.rankMessage = "From total attendance"
        return next_student_rank
    except Exception as ex:
        print(f'Error: {str(ex)}')
        raise ex

# ---------------------------------------------------------------------------------------
def GetPromotionRecords(badge_number: int) -> list[Promotions]:
    promotion_query_stmt = (select(Promotions)
                            .where(Promotions.badgeNumber == badge_number)
                            .order_by(Promotions.promotionDate.desc())
                            )
    return db_session.scalars(promotion_query_stmt).all()

def GetLastPromotionRecord(badge_number) -> Promotions:
    promotion_record_stmt = (select(Promotions)
                             .where(Promotions.badgeNumber == badge_number)
                             .order_by(Promotions.promotionDate.desc()))
    return db_session.scalars(promotion_record_stmt).first()
