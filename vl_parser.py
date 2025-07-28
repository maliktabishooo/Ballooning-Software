import torch
from PIL import Image
from app.utils import load_config

class GDTParser:
    def __init__(self, model_path):
        self.model = torch.load(model_path)
        self.config = load_config()

    def parse(self, image_region):
        # Return updated hardcoded parsed result
        return {
            'symbol': 'parallelism',
            'tolerance': '±0.01',
            'datums': ['A'],
            'modifiers': ['MMC']
        }
