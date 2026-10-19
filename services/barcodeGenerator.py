import io
import logging
import os

from PIL import Image
from barcode import Code39
from barcode.writer import ImageWriter
from flask import current_app

logger = logging.getLogger(__name__)

def createBarcodeFile(badgeNumber):
    try:
        barcodeFilePath   = os.path.join(current_app.root_path,  'static', 'images', 'badges', f'{badgeNumber}_barcode.png')
        logger.info(f'absolute barcode path: {os.path.abspath(barcodeFilePath)}')
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
    except Exception as ex:
        logger.exception(ex)
        raise ex
