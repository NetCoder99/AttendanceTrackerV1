from models.data_models import Archive
from sqlite.sqlite_alchemy import getDbSession

# set PYTHONPATH=C:\Users\jdugger01\source\Python\AttendanceTrackerV1\models
# $env:PYTHONPATH="C:\Users\jdugger01\source\Python\AttendanceTrackerV1\models"
# PYTHONPATH="models.data_models" python table_delete.py

db_session = getDbSession()
def DeleteArchiveTable():
    Archive.__table__.delete(bind=db_session.get_bind(), checkfirst=True)
