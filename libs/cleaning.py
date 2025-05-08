import re
from libs.extraction import ExtractionEngine

def clean_text(text: str, extraction_engine: str) -> str:
    if extraction_engine not in [ExtractionEngine.GOOGLE_CLOUD_VISION.value, ExtractionEngine.TESSERACT_OCR.value, ExtractionEngine.EASY_OCR.value]:
        raise Exception('Unhandled text extraction engine.')
    
    if extraction_engine == ExtractionEngine.TESSERACT_OCR.value:
        return __clean_text_tesseract_ocr(text=text)

    if extraction_engine == ExtractionEngine.EASY_OCR.value:
        return __clean_text_easy_ocr(text=text)

    return __clean_text_google_cloud_vision(text=text)

def __clean_text_tesseract_ocr(text: str) -> str:
    text = re.search(r'de métal(.*)', text, re.DOTALL).group(1).strip()
    
    # isolate elements
    text = text.replace('\n\n', '\n')
    entries = text.split('\n')
    
    new_entries = []

    for entry in entries:
        if re.match(r'^\d+\s*\(\d+\)', entry.strip()):
            new_entries.append(f'{entry}')
        else:
            new_entries[-1] = f'{new_entries[-1]} {entry}'

    # remove polluting keywords and characters
    substrings_to_remove = ['VO', 'VAN', 'VA', 'TUTT', 'TITT', '✓', 'דוח']

    final_entries = []

    for entry in new_entries:
        for substring_to_remove in substrings_to_remove:
            entry = entry.replace(substring_to_remove, '')
        final_entries.append(entry)
    
    # fixes
    final_entries = [entry.replace('\n', ' ').replace('- ', '-').strip() for entry in final_entries]
    
    return '\n'.join(final_entries)

def __clean_text_easy_ocr(text: str) -> str:
    text = re.search(r'de métal(.*)', text, re.DOTALL).group(1).strip()
    
    # fixes
    text = text.replace('(B)', '(8)')
    text = text.replace('Cæur', 'Cœur')
    
    # isolate elements
    entries = text.split('\n')

    new_entries = []

    for entry in entries:
        if re.match(r'^\d+\s*\(\d+\)', entry.strip()):
            new_entries.append(f'{entry}')
        else:
            new_entries[-1] = f'{new_entries[-1]} {entry}'

    # remove polluting keywords and characters
    substrings_to_remove = [' 44 ', '@66']

    tmp_entries = []

    for entry in new_entries:
        for substring_to_remove in substrings_to_remove:
            entry = entry.replace(substring_to_remove, ' ')
        tmp_entries.append(entry)
    
    final_entries = []

    # fixes
    for entry in tmp_entries:
        entry = entry.replace('\n', ' ').replace('- ', '-').replace(' -', '-').replace('gel gel', 'gel').replace('feu gel', 'feu').strip()
        entry = re.sub(r'\s{2,}', ' ', entry).strip()

        if entry.endswith("Griffes de"):
            entry = entry.replace('Griffes de', 'Griffes de gel')

        entry = entry.replace("Griffes de suprême", "Griffes de gel suprême")
        entry = entry.replace("Gueule-d'orage gel", "Gueule-d'orage")
        entry = entry.replace("Oiseau-tempête gel", "Oiseau-tempête")

        final_entries.append(entry)
    
    return '\n'.join(final_entries)

def __clean_text_google_cloud_vision(text: str) -> str:
    text = re.search(r'de métal(.*)', text, re.DOTALL).group(1).strip()
    
    # fixes
    text = text.replace('Coeur', 'Cœur')
    
    # isolate elements
    entries = text.split('\n')

    new_entries = []

    for entry in entries:
        if re.match(r'^\d+\s*\(\d+\)', entry.strip()):
            new_entries.append(f'{entry}')
        else:
            new_entries[-1] = f'{new_entries[-1]} {entry}'

    # remove polluting keywords and characters
    substrings_to_remove = ['VO', 'VAN', 'VA', 'TUTT', 'TITT', '✓', '☑', 'דוח', ' E ', ' U ']

    final_entries = []

    for entry in new_entries:
        for substring_to_remove in substrings_to_remove:
            entry = entry.replace(substring_to_remove, ' ')
        final_entries.append(entry)
    
    # fixes
    final_entries = [entry.replace('\n', ' ').replace('- ', '-').strip() for entry in final_entries]
    final_entries = [entry.replace('ACœur', 'Cœur').replace('FCœur', 'Cœur').replace('VCœur', 'Cœur').strip() for entry in final_entries]
    final_entries = [re.sub(r'\s{2,}', ' ', entry).strip() for entry in final_entries]
    
    return '\n'.join(final_entries)