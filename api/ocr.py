import os
from io import BytesIO
from PIL import Image
from tesserocr import PyTessBaseAPI


TRAINEDDATA = os.path.dirname(os.path.abspath(__file__))

def ocr(image: bytes) -> str:
    try:
        with PyTessBaseAPI(TRAINEDDATA) as api:
            api.SetImage(Image.open(BytesIO(image)))
            return api.GetUTF8Text()
            #print(api.AllWordConfidences())
        # api is automatically finalized when used in a with-statement (context manager)
        # otherwise api.End() should be explicitly called when it's no longer needed
    except Exception as error:
        print('[ERROR/OCR]', error)

# Other usages:
#print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages())  # prints tessdata path and list of available languages
#print(tesserocr.image_to_text(image)) # print ocr text from image
