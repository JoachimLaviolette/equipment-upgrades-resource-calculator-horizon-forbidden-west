import os
from dotenv import load_dotenv
from libs.extraction import extract_text_from_image
from libs.file import get_files_from_folder, read_file, write_file, write_image
from libs.cleaning import ExtractionEngine, clean_text
from libs.cropping import crop_image

def get_extraction_engine() -> ExtractionEngine:
    load_dotenv(dotenv_path='.env', override=True)

    if os.getenv('EXTRACTION_ENGINE') == ExtractionEngine.TESSERACT_OCR.value:
        print(f"Extraction engine '{ExtractionEngine.TESSERACT_OCR.value}' found in .env file. This engine will be used.")

        return ExtractionEngine.TESSERACT_OCR.value

    if os.getenv('EXTRACTION_ENGINE') == ExtractionEngine.EASY_OCR.value:
        print(f"Extraction engine '{ExtractionEngine.EASY_OCR.value}' found in .env file. This engine will be used.")

        return ExtractionEngine.EASY_OCR.value
    
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
        print(f"Extraction engine '{ExtractionEngine.TESSERACT_OCR.value}' will be used.")

        return ExtractionEngine.TESSERACT_OCR.value

def crop_original_dataset():
    image_paths = get_files_from_folder(folder_path='dataset/original', extensions=['.png'])

    for image_path in image_paths:
        file_name, file_ext = os.path.splitext(os.path.basename(image_path))
        cropped_image = crop_image(image_path=image_path)
        write_image(file_path=f'dataset/cropped/{file_name}.{file_ext}', image=cropped_image)

def extract_text_from_cropped_dataset(extraction_engine: str):
    print('Extracting texts from cropped screenshots...')

    image_paths = get_files_from_folder(folder_path='dataset/cropped', extensions=['.png'])

    for image_path in image_paths:
        file_name, file_ext = os.path.splitext(os.path.basename(image_path))
        extracted_text = extract_text_from_image(image_path=image_path, extraction_engine=extraction_engine)
        # extracted_text = read_file(file_path=f'output/{extraction_engine/extracted/{file_name}.txt')
        write_file(file_path=f'output/{extraction_engine}/extracted/{file_name}.txt', content=extracted_text)

def clean_extracted_text(extraction_engine: str):
    print('Cleaning extracted texts...')

    extracted_text_file_paths = get_files_from_folder(folder_path=f'output/{extraction_engine}/extracted', extensions=['.txt'])

    for extracted_text_file_path in extracted_text_file_paths:
        file_name, _ = os.path.splitext(os.path.basename(extracted_text_file_path))
        extracted_text = read_file(file_path=extracted_text_file_path)
        cleaned_text = clean_text(text=extracted_text, extraction_engine=extraction_engine)
        write_file(file_path=f'output/{extraction_engine}/cleaned/{file_name}.txt', content=cleaned_text)

def compute_total_costs_per_resource(extraction_engine: str) -> dict:
    print('Computing total costs per resource...')
    
    total_costs_per_resource: dict = {}
    cleaned_text_file_paths = get_files_from_folder(folder_path=f'output/{extraction_engine}/cleaned', extensions=['.txt'])

    for cleaned_text_file_path in cleaned_text_file_paths:
        content = read_file(file_path=cleaned_text_file_path)
        lines = content.split('\n')

        for line in lines:
            chunks = line.split(' ', maxsplit=2)
            total_costs = int(chunks[0])
            resource = chunks[2]

            if resource not in total_costs_per_resource.keys():
                total_costs_per_resource[resource] = total_costs
            else:
                total_costs_per_resource[resource] = total_costs_per_resource[resource] + total_costs

    return dict(sorted(total_costs_per_resource.items()))

def save_total_costs_per_resource(total_costs_per_resource: dict, extraction_engine: str):
    print('Saving total costs per resource in markdown file...')

    content: list[str] = [
        '| Ressource         | Total       |',
        '|-------------------|-------------|'
    ]
    
    for key, value in total_costs_per_resource.items():
        content.append(f'| {key}      | {value}     |')

    file_path = f'output/{extraction_engine}/results/total_costs_per_resource.md'
    write_file(file_path=file_path, content='\n'.join(content))    
    print(f"Result saved in file '{file_path}'.")

def main():
    extraction_engine: str = get_extraction_engine()

    # crop_original_dataset()
    # extract_text_from_cropped_dataset(extraction_engine=extraction_engine)   
    clean_extracted_text(extraction_engine=extraction_engine)
    total_costs_per_resource = compute_total_costs_per_resource(extraction_engine=extraction_engine)
    save_total_costs_per_resource(total_costs_per_resource=total_costs_per_resource, extraction_engine=extraction_engine)

if __name__ == '__main__':
    main()