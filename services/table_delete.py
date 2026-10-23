from models.data_models import Archive
from sqlite.sqlite_alchemy import getDbSession

# ------ powershell -------------------------------------------------------------
# $env:PYTHONPATH="C:\Users\jdugger01\source\Python\AttendanceTrackerV1"
# python -c 'from table_delete import DeleteArchiveTable; DeleteArchiveTable()'

# ------ bash  -------------------------------------------------------------
# PYTHONPATH="/home/johnd/AttendanceTracker/AttendanceTrackerV1" python -c "from table_delete import DeleteArchiveTable; DeleteArchiveTable()"

db_session = getDbSession()
def DeleteArchiveTable():
    engine = db_session.get_bind()
    print(f'DeleteArchiveTable - started - {str(engine.url)}')
    Archive.__table__.drop(bind=db_session.get_bind(), checkfirst=True)
    print('DeleteArchiveTable - completed')
