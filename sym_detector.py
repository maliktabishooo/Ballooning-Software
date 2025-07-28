from ultralytics import YOLOWorld
from app.utils import load_config

class YOLOGDTSymbolDetector:
    def __init__(self, model_path):
        self.model = YOLOWorld(model_path)
        self.config = load_config()
        self.classes = ['parallelism', 'concentricity', 'flatness', 'runout', 'perpendicularity', 'position', 'profile', 'cylindricity', 'straightness']

    def detect(self, image):
        results = self.model.predict(image, classes=self.classes, conf=0.5)
        symbols = []
        for box in results[0].boxes:
            symbols.append({
                'label': self.classes[int(box.cls)],
                'bbox': box.xyxy.tolist()[0],
                'angle': box.angle if hasattr(box, 'angle') else 0,
                'confidence': float(box.conf)
            })
        return symbols
