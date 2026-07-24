import sys

from sqlalchemy import text

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
            select *
            from   requirements r2
            where  r2.promotionSeqNum > (select promotionSeqNum from cte_current_requirement_id)
            order  by r2.promotionSeqNum asc
            limit  1
        '''
