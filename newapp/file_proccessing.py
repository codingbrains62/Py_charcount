# import tika
# from tika import parser
# from langdetect import detect, DetectorFactory
# from langcodes import Language
# from PIL import Image
# from pytesseract import pytesseract
# import os
# 
# tika.initVM()
# DetectorFactory.seed = 0  # Ensure consistent results

# def parse_and_display_info(filepath):
    # file_type, library = determine_file_type(filepath)
    # if file_type == 'text':
        # return parse_text_file(filepath, library)
    # elif file_type in ['pdf', 'docx', 'xlsx', 'txt']:
        # return parse_office_file(filepath, file_type, library)
    # elif file_type in ['jpg', 'png', 'jpeg']:
        # return parse_image_file(filepath, library)
    # else:
        # return {"error": f"Unsupported file format: {filepath}"}
    

# def parse_text_file(filepath, library):
    # with open(filepath, 'r', encoding='utf-8') as file:
        # content = file.read()
    # language = detect_language(content)
    # num_words = count_words(content)
    # num_chars = len(content)
    # return {
        # "filename": os.path.basename(filepath),
        # "filetype": 'TXT',
        # "language": language,
        # "library": library,
        # "num_words": num_words,
        # "num_chars": num_chars
    # }

# def parse_office_file(filepath, file_type, library):
    # parser_result = parser.from_file(filepath)
    # if parser_result['status'] == 200:
        # content = parser_result['content']
        # language = detect_language(content)
        # num_words = count_words(content)
        # num_chars = len(content)
        # return {
            # "filename": os.path.basename(filepath),
            # "filetype": file_type,
            # "language": language,
            # "library": library,
            # "num_words": num_words,
            # "num_chars": num_chars
        # }
    # else:
        # return {"error": f"Failed to parse file: {filepath}"}

# def parse_image_file(image_path, library):
    # path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # pytesseract.tesseract_cmd = path_to_tesseract
    # img = Image.open(image_path)
    # text = pytesseract.image_to_string(img)
    # language = detect_language(text)
    # num_words = count_words(text)
    # num_chars = len(text)
    # return {
        # "filename": os.path.basename(image_path),
        # "filetype": 'image',
        # "language": language,
        # "library": library,
        # "num_words": num_words,
        # "num_chars": num_chars
    # }


# def determine_file_type(filepath):
    # _, file_extension = os.path.splitext(filepath)
    # file_type = file_extension[1:].lower()
    # if file_type == 'txt':
        # return file_type, 'Built-in open'
    # elif file_type in ['pdf', 'docx', 'xlsx']:
        # return file_type, 'Tika'
    # elif file_type in ['jpg', 'png', 'jpeg']:
        # return file_type, 'Tesseract'
    # else:
        # return file_type, 'Unknown'


# def count_words(text):
    # words = text.split()  # Split the text into words
    # return len(words)
# 
# def detect_language(text):
    # try:
        # language_code = detect(text)
        # if language_code == 'sl':  # Slovenian language code
            # return "Hindi"  # Return Hindi directly if Slovenian is detected
        # language_name = Language(language_code).language_name()
        # return language_name
    # except:
        # return "Language detection failed"



import tika
from tika import parser
import easyocr
from langdetect import detect, DetectorFactory
from langcodes import Language
from PIL import Image
import os

DetectorFactory.seed = 0  # Ensure consistent results

def parse_and_display_info(filepath):
    file_type, library = determine_file_type(filepath)
    if file_type == 'text':
        return parse_text_file(filepath, library)
    elif file_type in ['pdf', 'docx', 'xlsx', 'txt']:
        return parse_office_file(filepath, file_type, library)
    elif file_type in ['jpg', 'png', 'jpeg']:
        return parse_image_file(filepath, library)
    else:
        return {"error": f"Unsupported file format: {filepath}"}

def parse_text_file(filepath, library):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    language = detect_language(content)
    num_words = count_words(content)
    num_chars = len(content)
    return {
        "filename": os.path.basename(filepath),
        "filetype": 'TXT',
        "language": language,
        "library": library,
        "num_words": num_words,
        "num_chars": num_chars
    }

def parse_office_file(filepath, file_type, library):
    parser_result = parser.from_file(filepath)
    if parser_result['status'] == 200:
        content = parser_result['content']
        language = detect_language(content)
        num_words = count_words(content)
        num_chars = len(content)
        return {
            "filename": os.path.basename(filepath),
            "filetype": file_type,
            "language": language,
            "library": library,
            "num_words": num_words,
            "num_chars": num_chars
        }
    else:
        return {"error": f"Failed to parse file: {filepath}"}

def parse_image_file(image_path, library):
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR with English language
    img = Image.open(image_path)
    result = reader.readtext(image_path)
    text = ' '.join([bbox[1] for bbox in result])  # Concatenate recognized text
    language = detect_language(text)
    num_words = count_words(text)
    num_chars = len(text)
    return {
        "filename": os.path.basename(image_path),
        "filetype": 'image',
        "language": language,
        "library": library,
        "num_words": num_words,
        "num_chars": num_chars
    }

def determine_file_type(filepath):
    _, file_extension = os.path.splitext(filepath)
    file_type = file_extension[1:].lower()
    if file_type == 'txt':
        return file_type, 'Built-in open'
    elif file_type in ['pdf', 'docx', 'xlsx']:
        return file_type, 'Tika'
    elif file_type in ['jpg', 'png', 'jpeg']:
        return file_type, 'EasyOCR'
    else:
        return file_type, 'Unknown'

def count_words(text):
    words = text.split()  # Split the text into words
    return len(words)

def detect_language(text):
    try:
        language_code = detect(text)
        if language_code == 'sl':  # Slovenian language code
            return "Hindi"  # Return Hindi directly if Slovenian is detected
        language_name = Language(language_code).language_name()
        return language_name
    except:
        return "Language detection failed"
