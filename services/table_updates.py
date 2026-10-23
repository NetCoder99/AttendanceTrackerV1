import csv
import logging.config

from sqlalchemy import inspect, MetaData, Table
from sqlalchemy.orm import declarative_base

from models.column_definition import NewColumnDefinition
from models.data_models import Schools, Archive
from sqlite.sqlite_alchemy import getDbSession


logger = logging.getLogger(__name__)
db_session = getDbSession()

def CheckForTableUpdates():
    try:
        engine = db_session.get_bind()
        inspector = inspect(engine)
        CheckForSchoolUpdates(inspector, engine)
        CheckForArchiveUpdates(inspector, engine)
    except Exception as ex:
        logger.exception(ex)
        raise ex

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

        #CompareTableColumns(inspector, engine, Archive)

    except Exception as ex:
        logger.exception(ex)
        raise ex

def CheckForSchoolUpdates(inspector, engine):
    try:
        if inspector.has_table("schools"):
            logger.info("The schools table exists!")
        else:
            logger.info("The schools table does not exist, creating ...")
            # Schools.__table__.delete(bind=engine, checkfirst=True)
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
        raise ex

# def CompareTableColumns(inspector, engine, model: declarative_base):
#     try:
#         logger.info(f"Comparing table columns for: {model.__table__}")
#         db_metadata = MetaData()
#         db_table    = Table(model.__table__, db_metadata, autoload_with=engine)
#
#         model_cols  = set(model.__table__.columns.keys())
#         db_cols     = set(db_table.columns.keys())
#
#         missing_in_db = model_cols - db_cols
#         extra_in_db   = db_cols    - model_cols
#
#         if missing_in_db:
#             for column_name in missing_in_db:
#                 logger.info(f"❌ Missing in Live DB: {column_name}")
#                 column_def = model.__table__.columns[column_name]
#                 CreateTableColumn(engine, column_def)
#         if extra_in_db:
#             logger.info(f"⚠️ Present in DB but missing from Model: {extra_in_db}")
#
#         # Compare data types and attributes for columns that exist in both
#         for col_name in model_cols & db_cols:
#             model_col = model.__table__.columns[col_name]
#             db_col    = db_table.columns[col_name]
#             if str(model_col.type) != str(db_col.type):
#                 print(f"❌ Type mismatch on '{col_name}': Model={model_col.type} | DB={db_col.type}")
#             if model_col.nullable != db_col.nullable:
#                 print(f"❌ Nullability mismatch on '{col_name}': Model={model_col.nullable} | DB={db_col.nullable}")
#
#         logger.info(f"DB Table is: {model.__table__}")
#     except Exception as ex:
#         logger.exception(ex)
#         raise ex
#
# def CreateTableColumn(engine, column_def):
#     try:
#         new_column_def = NewColumnDefinition.fromSqlAlchemy(column_def)
#         logger.info(f"Comparing table columns for: {new_column_def}")
#     except Exception as ex:
#         logger.exception(ex)
#         raise ex
