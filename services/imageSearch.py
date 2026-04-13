import os
from pathlib import Path



def searchForStudentImage(image_name):
    pics_dir    = os.path.join(os.getenv('APPDATA'), "Attendance", "Pictures")
    pics_files  = list(Path(pics_dir).rglob(image_name))
    if len(pics_files) > 0:
        return pics_files[0]
    else:
        return None
