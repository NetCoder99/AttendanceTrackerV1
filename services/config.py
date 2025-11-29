import os
import platform

def getDbPath():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Attendance', 'AttendanceV2.db')
    else:
        return os.path.join('/', 'Attendance', 'AttendanceV2.db')

