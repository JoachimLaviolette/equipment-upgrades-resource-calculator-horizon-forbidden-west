import base64
from PIL import Image
import pytesseract
import requests
from dotenv import load_dotenv
import os
from enum import Enum
import easyocr

class ExtractionEngine(Enum):
    GOOGLE_CLOUD_VISION = 'google_cloud_vision'
    TESSERACT_OCR = 'tesseract_ocr'
    EASY_OCR = 'easy_ocr'

def extract_text_from_image(image_path: str, extraction_engine: str) -> str:
    if extraction_engine not in [ExtractionEngine.GOOGLE_CLOUD_VISION.value, ExtractionEngine.TESSERACT_OCR.value, ExtractionEngine.EASY_OCR.value]:
        raise Exception('Unhandled text extraction origin.')
    
    print(f"Extracting text from image '{image_path}'...")

    if extraction_engine == ExtractionEngine.TESSERACT_OCR.value:
        return __extract_text_from_image_tesseract_ocr(image_path=image_path)
    
    if extraction_engine == ExtractionEngine.EASY_OCR.value:
        return __extract_text_from_image_easy_ocr(image_path=image_path)
        
    return __extract_text_from_image_google_cloud_vision(image_path=image_path)


def __extract_text_from_image_tesseract_ocr(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--psm 11', lang='fra')

    return text

def __extract_text_from_image_easy_ocr(image_path: str) -> str:
    reader = easyocr.Reader(['fr'], gpu=False)
    results = reader.readtext(image_path)
    
    return '\n'.join([text for (_, text, _) in results])

def __extract_text_from_image_google_cloud_vision(image_path: str) -> str:
    load_dotenv(dotenv_path='.env', override=True)
    
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = requests.post(
        url=f'https://vision.googleapis.com/v1/images:annotate?key={os.getenv('GOOGLE_CLOUD_VISION_API_KEY')}',
        headers={'Content-Type': 'application/json'},
        json={
            'requests': [
                {
                    'image': {'content': encoded_image},
                    'features': [{'type': 'TEXT_DETECTION'}]
                }
            ]
        }
    )

    data = response.json()

    try:
        text = data['responses'][0]['fullTextAnnotation']['text']
        
        return text
    except KeyError:
        print('No text returned from Google Cloud Vision API.')

        return ''