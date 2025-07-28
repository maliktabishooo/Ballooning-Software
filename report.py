import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.utils import load_config

class ReportGenerator:
    def __init__(self, dimensions, gdt_records):
        self.dimensions = dimensions
        self.gdt_records = gdt_records
        self.config = load_config()

    def generate_csv(self):
        data = []
        for i, dim in enumerate(self.dimensions):
            data.append({
                'Balloon #': i+1,
                'Type': 'Dimension',
                'Value': dim['text'],
                'Coordinates': dim['coords']
            })
        for i, rec in enumerate(self.gdt_records):
            data.append({
                'Balloon #': i+len(self.dimensions)+1,
                'Type': 'GD&T',
                'Symbol': rec['symbol'],
                'Tolerance': rec['tolerance'],
                'Datums': ','.join(rec['datums']),
                'Modifiers': ','.join(rec['modifiers'])
            })
        df = pd.DataFrame(data)
        csv_path = f"{self.config['report']['output_dir']}/inspection_report.csv"
        df.to_csv(csv_path, index=False)
        return csv_path

    def generate_pdf(self):
        pdf_path = f"{self.config['report']['output_dir']}/inspection_report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, "Inspection Report")
        y = 700
        for i, dim in enumerate(self.dimensions):
            c.drawString(100, y, f"Balloon #{i+1}: {dim['text']} at {dim['coords']}")
            y -= 20
        for i, rec in enumerate(self.gdt_records):
            c.drawString(100, y, f"Balloon #{i+len(self.dimensions)+1}: {rec['symbol']} {rec['tolerance']}")
            y -= 20
        c.save()
        return pdf_path
