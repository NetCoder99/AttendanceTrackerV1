import json
import csv
import logging.config

from sqlalchemy import inspect

from models.data_models import Schools
from sqlite.sqlite_alchemy import getDbSession


logger = logging.getLogger(__name__)
db_session = getDbSession()

def CheckForTableUpdates():
    try:
        inspector = inspect(db_session.get_bind())
        CheckForSchoolUpdates(inspector, db_session.get_bind())
    except Exception as ex:
        logger.exception(ex)

def CheckForSchoolUpdates(inspector, engine):
    try:
        if inspector.has_table("schools"):
            logger.info("The schools table exists!")
        else:
            logger.info("The schools table does not exist, creating ...")
            Schools.__table__.create(bind=engine, checkfirst=True)
            with open("static/data/schools_20261022.csv", 'r', encoding='utf-8') as schools_csv_file:
                schools_data_reader = csv.DictReader(schools_csv_file, quoting=csv.QUOTE_STRINGS)
                for school_csv_row in schools_data_reader:
                    logger.info(school_csv_row)
                    schools_record = Schools(**school_csv_row)
                    schools_record.updateDateTime = None if schools_record.updateDateTime.strip() == '' else schools_record.updateDateTime
                    db_session.add(schools_record)
            commit_result = db_session.commit()
            logger.info("The schools was created ...")
    except Exception as ex:
        logger.exception(ex)

