from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import layoutparser as lp
from PIL import Image
from app.utils import preprocess_image, load_config
import torch

class AdvancedOCREngine:
    def __init__(self):
        self.config = load_config()
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        self.layout_model = lp.Detectron2LayoutModel(
            "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
        )

    def extract_text(self, image):
        # Detect text regions
        layout = self.layout_model.detect(preprocess_image(image))
        text_regions = [region for region in layout if region.type == "Text"]
        
        # Extract text from each region
        text_data = []
        for region in text_regions[:self.config['ocr']['max_text_regions']]:
            cropped = image.crop((region.bbox.x1, region.bbox.y1, region.bbox.x2, region.bbox.y2))
            pixel_values = self.processor(cropped, return_tensors="pt").pixel_values
            generated_ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            text_data.append((text, (region.bbox.x1, region.bbox.y1)))
        
        return text_data
