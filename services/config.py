import os
import platform

def getDbPath():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Attendance', 'AttendanceV2.db')
    else:
        raise "This os is not supported!"

