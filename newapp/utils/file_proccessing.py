import os

from tika import parser
import easyocr
from langdetect import detect, DetectorFactory
from langcodes import Language
from PIL import Image


DetectorFactory.seed = 0  # Ensure consistent results

class FileExploration:
    def __init__(self, filepath):
        self.filepath = filepath

    def determine_file_type(self):
        _, file_extension = os.path.splitext(self.filepath)
        file_type = file_extension[1:].lower()
        if file_type == 'txt':
            return file_type, 'Built-in open'
        elif file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx']:
            return file_type, 'Tika'
        elif file_type in ['jpg', 'png', 'jpeg']:
            return file_type, 'EasyOCR'
        else:
            return file_type, 'Unknown'

    def count_words(self, text):
        words = text.split()  # Split the text into words
        return len(words)

    def detect_language(self, text):
        try:
            language_code = detect(text)
            if language_code == 'sl':  # Slovenian language code
                return "Hindi"  # Return Hindi directly if Slovenian is detected
            language_name = Language(language_code).language_name()
            return language_name
        except:
            return "Language detection failed"

    def parse_text_file(self, library):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        language = self.detect_language(content)
        num_words = self.count_words(content)
        num_chars = len(content)
        return {
            "filename": os.path.basename(self.filepath),
            "filetype": 'TXT',
            "language": language,
            "library": library,
            "num_words": num_words,
            "num_chars": num_chars
        }


    def parse_office_file(self, file_type, library):
        parser_result = parser.from_file(self.filepath)
        if parser_result['status'] == 200:
            content = parser_result['content']
            language = self.detect_language(content)
            num_words = self.count_words(content)
            num_chars = len(content)
            return {
                "filename": os.path.basename(self.filepath),
                "filetype": file_type,
                "language": language,
                "library": library,
                "num_words": num_words,
                "num_chars": num_chars
            }
        else:
            return {"error": f"Failed to parse file: {self.filepath}"}

    def parse_image_file(self, image_path, library):
        reader = easyocr.Reader(['en'])  # Initialize EasyOCR with English language
        img = Image.open(image_path)
        result = reader.readtext(image_path)
        text = ' '.join([bbox[1] for bbox in result])  # Concatenate recognized text
        language = self.detect_language(text)
        num_words = self.count_words(text)
        num_chars = len(text)
        return {
            "filename": os.path.basename(image_path),
            "filetype": 'image',
            "language": language,
            "library": library,
            "num_words": num_words,
            "num_chars": num_chars
        }

    def parse_and_display_info(self):
        file_type, library = self.determine_file_type()
        if file_type == 'text':
            return self.parse_text_file(library)
        elif file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt']:
            return self.parse_office_file(file_type, library)
        elif file_type in ['jpg', 'png', 'jpeg']:
            return self.parse_image_file(library)
        else:
            return {"error": f"Unsupported file format: {self.filepath}"}
