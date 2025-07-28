import re
from app.ocr_engine import AdvancedOCREngine
from app.utils import load_config

class PDFDimensionExtractor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.config = load_config()
        self.ocr = AdvancedOCREngine()
        self.dimensions = []

    def extract_text(self, image):
        return self.ocr.extract_text(image)

    def filter_dimensions(self, text_data):
        dim_pattern = self.config['regex_patterns']['dimensions']
        for text, coords in text_data:
            if re.match(dim_pattern, text, re.IGNORECASE):
                self.dimensions.append({'text': text, 'coords': coords, 'type': 'dimension'})
            elif re.match(self.config['regex_patterns']['tolerances'], text):
                self.dimensions.append({'text': text, 'coords': coords, 'type': 'tolerance'})
        return self.dimensions
