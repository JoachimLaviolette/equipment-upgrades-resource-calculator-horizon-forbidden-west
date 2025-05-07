import re
from libs.extraction import ExtractionEngine

def clean_text(text: str, extraction_engine: str) -> str:
    if extraction_engine not in [ExtractionEngine.GOOGLE_CLOUD_VISION.value, ExtractionEngine.TESSERACT.value]:
        raise Exception('Unhandled text extraction origin.')
    
    if extraction_engine == ExtractionEngine.GOOGLE_CLOUD_VISION.value:
        return __clean_text_google_cloud_vision(text=text)

    return __clean_text_tesseract(text=text)

def __clean_text_tesseract(text: str) -> str:
    text = re.search(r'de métal(.*)', text, re.DOTALL).group(1).strip()
    # isolate elements
    entries = text.split('\n\n')
    # remove extra white spaces between '-' and text
    entries = [entry.replace('\n', ' ').replace('- ', '-').strip() for entry in entries]
    # remove element that aint start with number (number)
    entries = [entry for entry in entries if re.match(r'^\d+\s*\(\d+\)', entry.strip())]
    
    # print(entries)
    
    return '\n'.join(entries)

def __clean_text_google_cloud_vision(text: str) -> str:
    text = re.search(r'de métal(.*)', text, re.DOTALL).group(1).strip()
    # isolate elements
    entries = text.split('\n')

    new_entries = []

    for entry in entries:
        if re.match(r'^\d+\s*\(\d+\)', entry.strip()):
            new_entries.append(f'{entry}')
        else:
            new_entries[-1] = f'{new_entries[-1]} {entry}'

    # remove new lines and extra white spaces between '-' and text
    new_entries = [entry.replace('\n', ' ').replace('- ', '-').strip() for entry in new_entries]
    # fix wrong traductions
    new_entries = [re.sub(r'^[AV]Cœur', 'Cœur', entry).strip() for entry in new_entries]
    # remove unwanted polluting keywords and characters
    substrings_to_remove = ['VO', 'VAN', 'VA', 'TUTT', 'TITT', '✓', 'דוח']

    final_entries = []

    for entry in new_entries:
        for substring_to_remove in substrings_to_remove:
            entry = entry.replace(substring_to_remove, '')
        final_entries.append(entry)

    final_entries = [entry.replace('  ', ' ').strip() for entry in final_entries]
    
    return '\n'.join(final_entries)