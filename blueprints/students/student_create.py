import re
import logging.config

import constants
from datetime import datetime
from models.data_models import Students, Promotions
from models.input_models import NewPromotionRecord
from sqlite.sqlite_alchemy import getDbSession

logger = logging.getLogger(__name__)
db_session = getDbSession()

def CreateNewStudentRecord(form_dict: dict):
    try:
        student_record = Students()
        student_record.badgeNumber = None

        #student_record.badgeNumber  = form_dict['badgeNumber'] if form_dict['badgeNumber'] else form_dict['hdnBadgeNumber']
        student_record.firstName    = form_dict['frmField1']
        student_record.lastName     = form_dict['frmField3']
        #student_record.namePrefix   = form_dict['namePrefix']
        student_record.email        = form_dict['frmEmail']
        student_record.address      = form_dict['frmField4']
        student_record.address2     = form_dict['frmField42']
        student_record.city         = form_dict['frmField9']
        student_record.country      = 'USA'
        student_record.state        = form_dict['frmField10']
        student_record.zip          = form_dict['frmField11']
        student_record.birthDate    = form_dict['frmBirthDate']
        student_record.phoneHome    = form_dict['frmPhoneHome']
        #student_record.phoneMobile  = form_dict['phoneMobile']
        student_record.status       = 'Active'

        pattern = re.compile(r"^(data):(image)/(.*);(base64),(.+)")
        matches = pattern.search(form_dict['imageSrc'])
        student_record.studentImageName   = form_dict['imageName']
        student_record.studentImageType   = matches.group(3)
        student_record.studentImageBase64 = matches.group(5)

        student_record.currentRankNum       = 1
        student_record.currentRankName      = 'White Belt'
        student_record.currentStripeId      = 181
        student_record.currentStripeName    = 'No stripe earned'
        student_record.studentPromotionDate = datetime.now().strftime(constants.fmtDateTime)

        db_session.add(student_record)
        db_session.commit()

        promotion_params = NewPromotionRecord.construct()
        promotion_params.badge_number   = student_record.badgeNumber
        promotion_params.belt_id        = student_record.currentRankNum
        promotion_params.belt_name      = student_record.currentRankName
        promotion_params.stripe_id      = student_record.currentStripeId
        promotion_params.stripe_name    = student_record.currentStripeName
        promotion_params.promotion_date = student_record.studentPromotionDate
        promotion_params.comments       = 'New student creation'
        InsNewPromotionRecord(student_record, promotion_params)
        return student_record
    except Exception as ex:
        logger.error(ex)
        raise ex

def InsNewPromotionRecord(student_record: Students,  promotion_params: NewPromotionRecord) -> Promotions:
    try:
        #ValidatePromotionParams(promotion_params)
        new_promotion_record = Promotions()
        new_promotion_record.studentName      = f'{student_record.firstName} {student_record.lastName}'
        new_promotion_record.studentFirstName = student_record.firstName
        new_promotion_record.studentLastName  = student_record.lastName
        new_promotion_record.badgeNumber      = student_record.badgeNumber
        new_promotion_record.beltId      = promotion_params.belt_id
        new_promotion_record.beltTitle   = promotion_params.belt_name
        new_promotion_record.stripeId    = promotion_params.stripe_id
        new_promotion_record.stripeTitle = promotion_params.stripe_name
        if promotion_params.belt_id != student_record.currentRankNum:
            new_promotion_record.promotionType = 'Belt'
        else:
            new_promotion_record.promotionType = 'Stripe'
        if promotion_params.comments.strip() == '':
            new_promotion_record.comments = "Promotion from api"
        else:
            new_promotion_record.comments = promotion_params.comments

        if isinstance(promotion_params.promotion_date, str):
            new_promotion_record.promotionDate = promotion_params.promotion_date
        elif isinstance(promotion_params.promotion_date, datetime):
            new_promotion_record.promotionDate  = promotion_params.promotion_date.strftime(constants.fmtDateTime)
        else:
            raise Exception("Unknown promotion date type!")
        new_promotion_record.createDateTime = datetime.now().strftime(constants.fmtDateTime)
        new_promotion_record.createDateTime = datetime.now().strftime(constants.fmtDateTime)
        db_session.add(new_promotion_record)
        db_session.commit()
        return new_promotion_record
    except Exception as ex:
        logger.error(ex)
        raise ex
