import os
import argparse
from dotenv import load_dotenv
from libs.extraction import extract_text_from_image
from libs.file import get_files_from_folder, read_file, write_file
from libs.cleaning import ExtractionEngine, clean_text

def get_extraction_engine() -> ExtractionEngine:
    load_dotenv(dotenv_path='.env', override=True)

    if os.getenv('EXTRACTION_ENGINE') == ExtractionEngine.TESSERACT.value:
        print(f"Extraction engine '{ExtractionEngine.TESSERACT.value}' found in .env file. This engine will be used.")

        return ExtractionEngine.TESSERACT.value
    
    if os.getenv('EXTRACTION_ENGINE') == ExtractionEngine.GOOGLE_CLOUD_VISION.value:
        print(f"Extraction engine '{ExtractionEngine.GOOGLE_CLOUD_VISION.value}' found in .env file. This engine will be used.")

        if os.getenv('GOOGLE_CLOUD_VISION_API_KEY') is not None and os.getenv('GOOGLE_CLOUD_VISION_API_KEY').strip() != '':
            print(f"Google Cloud Vision API key found in .env file. The key will be used.")

            return ExtractionEngine.GOOGLE_CLOUD_VISION.value
        
        while response is None:
            response = input('Provide an API key:\n')

            if response.strip() == '':
                print('Please provide a valid API key.\n')
                response = None

        with open(file='.env', mode='w') as f:
            f.write(f'GOOGLE_CLOUD_VISION_API_KEY={response}')

        return ExtractionEngine.GOOGLE_CLOUD_VISION.value
    
    response = None
    
    while response is None:
        response = input('Which text extraction API do you want to use?\n- [1] google_cloud_vision (API key required)\n- [2] tesseract\n')

        if response != '1' and response != '2':
            print('Please select one of the two given options.\n')
            response = None

    if response == '1':
        print(f"Extraction engine '{ExtractionEngine.GOOGLE_CLOUD_VISION.value}' will be used.")

        response = None

        if os.getenv('GOOGLE_CLOUD_VISION_API_KEY') is not None and os.getenv('GOOGLE_CLOUD_VISION_API_KEY').strip() != '':
            print(f"Google Cloud Vision API key found in .env file. The key will be used.")

            return ExtractionEngine.GOOGLE_CLOUD_VISION.value

        while response is None:
            response = input('Provide an API key:\n')

            if response.strip() == '':
                print('Please provide a valid API key.\n')
                response = None

        with open(file='.env', mode='w') as f:
            f.write(f'GOOGLE_CLOUD_VISION_API_KEY={response}')

        return ExtractionEngine.GOOGLE_CLOUD_VISION.value
    else:
        print(f"Extraction engine '{ExtractionEngine.TESSERACT.value}' will be used.")

        return ExtractionEngine.TESSERACT.value

def main():
    extraction_engine: str = get_extraction_engine()

    image_paths = get_files_from_folder(folder_path='dataset')

    for image_path in image_paths:
        # extracted_text = extract_text_from_image(image_path=image_path, extraction_engine=extraction_engine)
        extracted_text = read_file(file_path=f'output/{os.path.splitext(os.path.basename(image_path))[0]}_{extraction_engine}_extracted_text.txt')
        cleaned_text = clean_text(text=extracted_text, extraction_engine=extraction_engine)

        write_file(file_path=f'output/{os.path.splitext(os.path.basename(image_path))[0]}_{extraction_engine}_extracted_text.txt', content=extracted_text)
        write_file(file_path=f'output/{os.path.splitext(os.path.basename(image_path))[0]}_{extraction_engine}_cleaned_text.txt', content=cleaned_text)

    total_per_resource: dict = {}

    for image_path in image_paths:
        content = read_file(file_path=f'output/{os.path.splitext(os.path.basename(image_path))[0]}_{extraction_engine}_cleaned_text.txt')
        lines = content.split('\n')

        for line in lines:
            chunks = line.split(' ', maxsplit=2)
            total = int(chunks[0])
            resource = chunks[2]

            if resource not in total_per_resource.keys():
                total_per_resource[resource] = total
            else:
                total_per_resource[resource] = total_per_resource[resource] + total

    total_per_resource = dict(sorted(total_per_resource.items()))

    with open(file='output/results.md', mode='w', encoding='utf8') as f:
        f.write('| Ressource         | Total       |\n')
        f.write('|-------------------|-------------|\n')
        
        for key, value in total_per_resource.items():
            f.write(f'| {key}      | {value}     |\n')

if __name__ == '__main__':
    main()