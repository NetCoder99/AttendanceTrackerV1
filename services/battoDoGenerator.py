import datetime
import os
import webbrowser

from PIL import Image
from fpdf import FPDF, Align
from services.imageSearch import searchForStudentImage

def createBattoDoBadgePdf(badgeNumber, studentData):
    try:
        imageName     = str(studentData['studentImageName'])
        if imageName is not None:
            student_image_path = searchForStudentImage(imageName)

        else:
            student_image_path = os.path.join('static', 'images', 'misc_images', 'RSM_Logo2.jpg')

        rsmImagePath  = os.path.join('static', 'images', 'misc_images', 'RSM_Logo2.jpg')

        pdf = FPDF(unit="in", format=(3.5, 2))
        pdf.add_page()
        pdf.set_margin(0)
        pdf.rect(x=0, y=0, w=3.5, h=2, style='')

        pdf.image(rsmImagePath, x=2.75, y=0.06, w=0.7)

        pdf.set_font("Times", style="B", size=12)
        pdf.text(x=1.05, y=0.25, txt="Rising Sun Martial Arts")

        # pdf.set_line_width(.005)
        # pdf.line(.1, .45, 1.9, .45)
        #
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_xy(x=1.0, y=0.29)
        pdf.cell(2, 0.3, txt="Batto-Do", align=Align.C)


        pdf.set_font("Times", style="B", size=7)
        pdf.set_xy(0.9, 0.49)
        pdf.cell(2, 0.3, txt="Building tomorrows leaders,", align=Align.C)
        pdf.set_xy(0.9, 0.59)
        pdf.cell(2, 0.3, txt="one black belt at a time!", align=Align.C)
        #
        # pdf.set_line_width(.005)
        # pdf.line(.1, .71, 1.9, .71)
        #
        newImagePath = correctImageOrientation(str(student_image_path))
        # newImagePath = os.path.join('static', 'images', 'students', 'studentImage.jpg')
        #showImageProperties(oldImagePath)
        pdf.image(newImagePath, x=.05, y=.05, w=0.95)
        #
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_fill_color(255, 0, 0)
        pdf.set_xy(x=1.05, y=0.8)
        pdf.cell(w=2.4, h=0.27, txt=f'{studentData['firstName']} {studentData['lastName']} ', border=0, align=Align.C, fill=True)

        col_width = pdf.epw / 2
        pdf.set_font("Times", style="B", size=10)
        pdf.set_xy(x=1.07, y=1.1)
        pdf.cell(col_width, 0.2, txt=f'Student # {studentData['badgeNumber']}', border=0, align=Align.L)

        pdf.set_xy(x=2.07, y=1.1)
        pdf.cell(col_width, 0.2, txt=f'Birthday:' , border=0, align=Align.L)
        pdf.set_xy(x=2.67, y=1.1)
        pdf.cell(col_width, 0.2, txt=f'{studentData['birthDate']}', border=0, align=Align.L)

        pdf.set_xy(x=2.07, y=1.25)
        pdf.cell(col_width, 0.2, txt=f'Since:' , border=0, align=Align.L)
        pdf.set_xy(x=2.67, y=1.25)
        pdf.cell(col_width, 0.2, txt=f'{studentData['memberSince']}', border=0, align=Align.L)

        barcodeFilePath = os.path.join('static', 'images', 'badges', f'{badgeNumber}_barcode.png')
        pdf.image(barcodeFilePath, x=.6, y=1.55, h=.4,  w=2.3)

        line_x = 1.5
        pdf.set_line_width(.009)
        pdf.line(.1, line_x, 3.4, line_x)

        current_timestamp = datetime.datetime.now().timestamp()
        badgeFilePath = os.path.join('static', 'images', 'badges', f'{badgeNumber}_batto_do_{current_timestamp}.pdf')
        pdf.output(badgeFilePath)

        abs_file_path = os.path.abspath(badgeFilePath)
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