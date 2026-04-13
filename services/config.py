import os
import platform



def getDbPath(db_name: str = 'AttendanceV3.db'):
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Attendance', db_name)
    else:
        return os.path.join('/', 'Attendance', db_name)

