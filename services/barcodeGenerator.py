import io
import os

import barcode
from PIL import Image
from barcode import Code39
#from barcode import Code39
from barcode.writer import ImageWriter

def createBarcodeFile(badgeNumber):
    barcodeFilePath   = os.path.join('static', 'images', 'badges', f'{badgeNumber}_barcode.png')
    code39Generator   = Code39(badgeNumber, writer=ImageWriter(), add_checksum=False)
    options = {
        'quiet_zone': 1,
        'module_width': 0.5,
        'module_height': 17,
        'write_text': False,
        'text' : f'Student# {badgeNumber}',
        'dpi': 2400,
        'add_checksum': False
    }
    with open(barcodeFilePath, 'wb') as f:
        img = code39Generator.render(options)
        resized_img = img.resize((404, 122), Image.Resampling.NEAREST)
        resized_img.save(f, text='My Custom Text')

# def createBarcodeFile3(badgeNumber):
#     barCodeFilePath = os.path.join('static', 'images', 'badges', f'{badgeNumber}_barcode.png')
#     options = {
#         'quiet_zone': 2,
#         'module_width': 0.5,
#         'module_height': 17,
#         'write_text': False,
#         'text': f'Student# {badgeNumber}',
#         'dpi': 300,
#         'add_checksum' : False
#     }
#     fp = io.BytesIO()
#     code = barcode.get('code39', badgeNumber, writer=ImageWriter())
#     code.write(fp, options)
#     fp.seek(0)
#     img = Image.open(fp)
#     img.save(barCodeFilePath)

# def create_badge_api(badgeNumber):
#     print(f'Current route: create_badge_api')
#     badgeCode   = barcode.Code39(badgeNumber, writer=ImageWriter(), add_checksum=False)
#     badgeOptions   = {
#         "module_width":4,
#         "module_height":80,
#         "font_size": 40,
#         'write_text': True,
#         'text': 'My Product Name',
#         "text_distance": 20,
#         "quiet_zone": 3
#     }
#     options = {
#         'text': 'My Product Name',  # Or use default data
#         'font_size': 10,
#         'text_distance': 8,  # mm from barcode
#         'foreground': 'black',
#         'background': 'white'
#     }
#     file_path   = os.path.join('static', 'images', 'badges', f'{badgeNumber}_barcode')
#     filename    = badgeCode.save(file_path, options)
#     print(f'filename: {filename}')
#     return {"status" : 'ok'}
