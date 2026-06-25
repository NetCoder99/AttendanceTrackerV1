import base64
import os
import webbrowser
from io import BytesIO

import img2pdf
from PIL import Image
from fpdf import FPDF, Align

def createBeltsPdf():
    try:
        pdf = FPDF(unit="in", format=(2, 3.5))
        pdf.add_page()
        pdf.set_margin(0)


        pdf.set_font("Times", style="B", size=10)
        pdf.text(0.5, 0.29, txt="Rising Sun Martial Arts")

        pdf.set_line_width(.005)
        pdf.line(.1, .45, 1.9, .45)

        pdf.set_font("Times", style="B", size=7)
        pdf.set_xy(0.1, 0.39)
        pdf.cell(2, 0.3, txt="Building tomorrows leaders,", align=Align.C)
        pdf.set_xy(0.1, 0.49)
        pdf.cell(2, 0.3, txt="one black belt at a time!", align=Align.C)

        badgeFilePath = os.path.join('static', 'images', f'belts.pdf')
        pdf.output(badgeFilePath)

        abs_file_path = os.path.abspath(badgeFilePath)
        webbrowser.open_new_tab(f'file://{abs_file_path}')
    except Exception as e:
        print(f"Error generating badge pdf : {e}")