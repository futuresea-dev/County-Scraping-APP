from PIL import Image as Pimage, ImageDraw
from wand.image import Image as Wimage
import sys
import numpy as np
from io import BytesIO

import pyocr
import pyocr.builders


def _convert_pdf2jpg(in_file_path: str, resolution: int = 200) -> Pimage:
    """
    Convert PDF file to JPG

    :param in_file_path: path of pdf file to convert
    :param resolution: resolution with which to read the PDF file
    :return: PIL Image
    """
    with Wimage(filename=in_file_path, resolution=resolution).convert("jpg") as all_pages:
        for page in all_pages.sequence:
            with Wimage(page) as single_page_image:
                # transform wand image to bytes in order to transform it into PIL image
                yield Pimage.open(BytesIO(bytearray(single_page_image.make_blob(format="jpeg"))))


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.
for img in _convert_pdf2jpg("export (1).pdf"):
    txt = tool.image_to_string(img,
                               lang=lang,
                               builder=pyocr.builders.TextBuilder())
