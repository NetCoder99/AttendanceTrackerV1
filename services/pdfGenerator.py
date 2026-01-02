import base64
import os
import webbrowser
from io import BytesIO

import img2pdf
from PIL import Image
from fpdf import FPDF, Align


def createBadgePdf(badgeNumber, studentData):
    try:
        imageName     = str(studentData['studentImageName'])
        if imageName is not None:
            oldImagePath = os.path.join('static', 'images', 'students', imageName)
            data_uri = f"data:image/{studentData['studentImageType']};base64,{studentData['studentImageBase64']}"
        else:
            oldImagePath = os.path.join('static', 'images', 'misc_images', 'RISING_SUN_FOOTER.webp')
            data_uri = os.path.join('static', 'images', 'misc_images', 'RISING_SUN_FOOTER.webp')

        rsmImagePath  = os.path.join('static', 'images', 'misc_images', 'RSM_Logo2.jpg')

        pdf = FPDF(unit="in", format=(2, 3.5))
        pdf.add_page()
        pdf.set_margin(0)

        pdf.image(rsmImagePath, x=0.04, y=0.01, w=.4)

        pdf.set_font("Times", style="B", size=10)
        pdf.text(0.5, 0.29, txt="Rising Sun Martial Arts")

        pdf.set_line_width(.005)
        pdf.line(.1, .45, 1.9, .45)

        pdf.set_font("Times", style="B", size=7)
        pdf.set_xy(0.1, 0.39)
        pdf.cell(2, 0.3, txt="Building tomorrows leaders,", align=Align.C)
        pdf.set_xy(0.1, 0.49)
        pdf.cell(2, 0.3, txt="one black belt at a time!", align=Align.C)

        pdf.set_line_width(.005)
        pdf.line(.1, .71, 1.9, .71)

        newImageBase64 = correctImageOrientationBase64(data_uri, studentData['studentImageType'])
        newDataUri     = f"data:image/{studentData['studentImageType']};base64,{newImageBase64}"
        # newImagePath = os.path.join('static', 'images', 'students', 'studentImage.jpg')
        # showImageProperties(oldImagePath)
        pdf.image(newDataUri, x=.4, y=.75, h=1.5)

        pdf.set_font("Arial", style="B", size=12)
        pdf.set_xy(0, 2.3)
        pdf.cell(0, 0.2, txt=f'{studentData['firstName']} {studentData['lastName']} ', border=0, align=Align.C)

        col_width = pdf.epw / 2
        pdf.set_font("Times", style="B", size=7)
        pdf.set_xy(0, 2.5)
        pdf.cell(col_width, 0.2, txt=f'Since: {studentData['memberSince']}', border=0, align=Align.C)
        pdf.set_xy(col_width, 2.5)
        pdf.cell(col_width, 0.2, txt=f'Birthday: {studentData['birthDate']}', border=0, align=Align.C)


        line_x = 2.8
        pdf.set_line_width(.009)
        pdf.line(.1, line_x, 1.9, line_x)

        barcodeFilePath = os.path.join('static', 'images', 'badges', f'{badgeNumber}_barcode.png')
        pdf.image(barcodeFilePath, x=.3, y=2.86, h=.5,  w=1.5)

        line_x = 3.4
        pdf.set_line_width(.009)
        pdf.line(.1, line_x, 1.9, line_x)

        badgeFilePath = os.path.join('static', 'images', 'badges', f'{badgeNumber}.pdf')
        pdf.output(badgeFilePath)


        abs_file_path = os.path.abspath(badgeFilePath)
        webbrowser.open_new_tab(f'file://{abs_file_path}')
    except Exception as e:
        print(f"Error generating badge pdf : {e}")


def correctImageOrientationBase64(inpImageBase64, imageFormat):
    if "," in inpImageBase64:
        tmpImageBase64 = inpImageBase64.split(",")[1]
    else:
        tmpImageBase64 = inpImageBase64
    tmpImageBytes = BytesIO(base64.b64decode(tmpImageBase64))

    # oldFilePath = os.path.split(imagePath)[0]
    # newFilePath = os.path.join(oldFilePath, "studentImage.jpg")
    try:
        with Image.open(tmpImageBytes) as img:
            exif = img.getexif()
            if imageFormat is None:
                imageFormat = img.format
            orientation = exif.get(0x0112, 1)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
            # img.save(newFilePath)
            max_size = (300, 300)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            buffered = BytesIO()
            img.save(buffered, format=imageFormat)
            img.close()
            img = None

            newImageDecode = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return newImageDecode
    except Exception as e:
        print(f"Error processing image : {e}")

def correctImageOrientation(imagePath):
    oldFilePath = os.path.split(imagePath)[0]
    newFilePath = os.path.join(oldFilePath, "studentImage.jpg")
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
            img.save(newFilePath)
            max_size = (300, 300)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.close()
    except Exception as e:
        print(f"Error processing image {imagePath}: {e}")
    return newFilePath

# def saveImageAsPdf(imagePath):
#     # pdfPath = os.path.split(imagePath)
#     pdfFileName   = os.path.split(imagePath)[1].replace('JPG', 'PDF')
#     pdfImagePath  = os.path.join('static', 'images', 'pdfTemp', pdfFileName)
#     with open(pdfImagePath, "wb") as f:
#         f.write(img2pdf.convert(imagePath, rotation=img2pdf.Rotation.ifvalid))
#     return pdfImagePath
#

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