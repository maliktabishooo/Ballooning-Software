from PIL import Image, ImageDraw
from app.utils import load_config

class BalloonDrawer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.config = load_config()

    def draw(self, dimensions, symbols, gdt_records):
        img = Image.open(self.input_path)
        draw = ImageDraw.Draw(img)
        
        # Draw dimension balloons
        for i, dim in enumerate(dimensions):
            x, y = dim['coords']
            r = self.config['drawing']['balloon_radius']
            draw.ellipse([x-r, y-r, x+r, y+r], outline=self.config['drawing']['balloon_color'], width=2)
            draw.text((x+r+5, y-r), str(i+1), fill=self.config['drawing']['balloon_color'])
        
        # Draw GD&T frames
        for sym, rec in zip(symbols, gdt_records):
            x1, y1, x2, y2 = sym['bbox'][0]
            draw.rectangle([x1, y1, x2, y2], outline='blue', width=2)
            draw.text((x1, y1-15), f"{rec['symbol']} {rec['tolerance']}", fill='blue')
        
        return img
