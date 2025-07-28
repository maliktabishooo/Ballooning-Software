from ultralytics import YOLOWorld
from app.utils import load_config

class YOLOGDTSymbolDetector:
    def __init__(self, model_path):
        self.model = YOLOWorld(model_path)
        self.config = load_config()
        self.classes = ['parallelism', 'concentricity', 'flatness', 'runout', 'perpendicularity', 'position', 'profile', 'cylindricity', 'straightness']

    def detect(self, image):
        # Return hardcoded dummy detection
        return [{
            'label': 'parallelism',
            'bbox': [100, 100, 150, 150],
            'angle': 0,
            'confidence': 0.9
        }]
