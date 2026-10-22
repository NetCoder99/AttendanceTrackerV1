import json
import csv
import logging.config

from sqlalchemy import inspect

from models.data_models import Schools, Archive
from sqlite.sqlite_alchemy import getDbSession


logger = logging.getLogger(__name__)
db_session = getDbSession()

def CheckForTableUpdates():
    try:
        inspector = inspect(db_session.get_bind())
        CheckForSchoolUpdates(inspector, db_session.get_bind())
        CheckForArchiveUpdates(inspector, db_session.get_bind())
    except Exception as ex:
        logger.exception(ex)

def CheckForArchiveUpdates(inspector, engine):
    try:
        if inspector.has_table("archive"):
            logger.info("The archive table exists!")
        else:
            logger.info("The archive table does not exist, creating ...")
            Archive.__table__.create(bind=engine, checkfirst=True)
            # with open("static/data/archive_20261022.csv", 'r', encoding='utf-8') as archive_csv_file:
            #     archive_data_reader = csv.DictReader(archive_csv_file, quoting=csv.QUOTE_STRINGS)
            #     for archive_csv_row in archive_data_reader:
            #         logger.info(archive_csv_row)
            #         archive_record = Archive(**archive_csv_row)
            #         #archive_record.updateDateTime = None if archive_record.updateDateTime.strip() == '' else archive_record.updateDateTime
            #         db_session.add(archive_record)
            # commit_result = db_session.commit()
            logger.info("The archive was created ...")
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

