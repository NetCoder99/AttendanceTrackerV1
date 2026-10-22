import datetime
import os
import webbrowser

from PIL import Image
from fpdf import FPDF, Align

from models.data_models import Schools, Classes
from services.datetimeFormats import GetDayName


def PrintClassSchedule(schoolData: Schools, classData: list[Classes], footer_text: list[str]):
    try:
        # rsmSunburstPath  = os.path.join('static', 'images', 'misc_images', 'RSM_Sunburst.png')
        rsmBadgePath     = os.path.join('static', 'images', 'misc_images', 'RSM_Patch.png')

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Prepare the header section
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pdf = FPDF(unit="in", format=(8.5, 11))
        pdf.add_page()
        pdf.set_margin(0)
        pdf.rect(x=0, y=0, w=8.5, h=11, style='')

        pdf.image(rsmBadgePath, x=0.50, y=0.15, w=1.5)
        pdf.image(rsmBadgePath, x=6.30, y=0.15, w=1.5)

        pdf.set_font("Helvetica", style="B", size=24)
        pdf.text(x=2.35, y=0.65, txt=f"{schoolData.schoolName}")
        pdf.set_font("Times", style="B", size=12)
        pdf.text(x=2.70, y=0.90, txt=f"{schoolData.schoolAddr1} {schoolData.schoolAddr2} ")
        pdf.text(x=2.70, y=1.10, txt=f"{schoolData.schoolCity}, {schoolData.schoolState} {schoolData.schoolZip}")
        pdf.text(x=2.70, y=1.30, txt=f"{schoolData.schoolPhone}")
        pdf.text(x=2.70, y=1.50, txt=f"{schoolData.schoolUrl}")

        pdf.set_font("Times", style="", size=10)
        pdf.text(x=6.40, y=1.75, txt=f"Effective: 10/06/2026")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Print the class schedule details
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pdf.set_font("Times", style="B", size=12)
        col1_x = 0.30
        col2_x = 1.20
        start_y = 1.50

        previous_day = -1
        for class_record in classData:
            if class_record.classDayOfWeek != previous_day:
                start_y += .20
                pdf.set_font("Times", style="BU", size=12)
                pdf.set_xy(x=col1_x, y=start_y)
                pdf.cell(w=1, h=1,  txt=GetDayName(class_record.classDayOfWeek), align=Align.L)

            pdf.set_font("Times", style="B", size=12)
            pdf.set_xy(x=col2_x, y=start_y)
            pdf.cell(w=1, h=1,txt=class_record.classStartTime, align=Align.R)

            pdf.set_xy(x=col2_x + 0.65, y=start_y)
            pdf.cell(w=1, h=1,txt=' TO ', align=Align.C)

            pdf.set_xy(x=col2_x + 1.10, y=start_y)
            pdf.cell(w=1, h=1,txt=class_record.classFinisTime, align=Align.R)

            pdf.set_xy(x=col2_x + 2.25, y=start_y)
            pdf.cell(w=1, h=1,txt=class_record.className, align=Align.L)

            previous_day = class_record.classDayOfWeek
            start_y += .20

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Print the footer
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        start_y = 9
        pdf.set_font("Helvetica", style="BI", size=12)
        for footer_line in footer_text:
            pdf.set_xy(x=col1_x, y=start_y)
            pdf.cell(w=0, h=1,txt=footer_line, align=Align.C)
            start_y += .20
            pdf.set_font("Helvetica", style="B", size=12)

        current_timestamp = datetime.datetime.now().timestamp()
        scheduleFilePath = os.path.join('static', 'images', 'output', f'rsm_class_schedule_{current_timestamp}.pdf')
        pdf.output(scheduleFilePath)

        abs_file_path = os.path.abspath(scheduleFilePath)
        webbrowser.open_new_tab(f'file://{abs_file_path}')
    except Exception as ex:
        print(str(ex))
        raise ex

def correctImageOrientation(imagePath):
    #oldFilePath = os.path.split(imagePath)[0]
    newFilePath = os.path.join('static/images/students', "studentImage.jpg")
    try:
        with Image.open(imagePath) as img:
            exif = img.getexif()
            orientation = exif.get(0x0112, 1)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

            if img.mode in ("RGBA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                max_size = (300, 300)
                background.thumbnail(max_size, Image.Resampling.LANCZOS)
                background.save(newFilePath)
                background.close()
            else:
                max_size = (300, 300)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(newFilePath)
                img.close()
            return newFilePath
    except Exception as ex:
        print(f"Error processing image {imagePath}: {ex}")
        raise ex

def showImageProperties(imagePath):
    img = Image.open(imagePath)

    # Access properties
    print(f"-------------------------------------")
    print(f"Filename: {img.filename}")
    print(f"Format:   {img.format}")  # e.g., JPEG, PNG, GIF
    print(f"Size:     {img.size}")  # (width, height) tuple in pixels
    print(f"Width:    {img.width}")  # Width in pixels
    print(f"Height:   {img.height}")  # Height in pixels
    print(f"Mode:     {img.mode}")