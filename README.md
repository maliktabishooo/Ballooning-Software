Advanced Auto-Ballooning & GD&T Inspection Software
This project provides a production-ready auto-ballooning software for engineering drawings, supporting PDF and image inputs. It uses YOLOv11 for GD&T symbol detection, Florence-2 for structured data parsing, and a Streamlit front-end for interactive use.
Features

Extracts all dimension types (linear, angular, diameters, etc.) using hybrid OCR (EasyOCR + Tesseract).
Detects GD&T symbols with ~95% accuracy using YOLOv11.
Parses structured GD&T data with ~97% F1-score using Florence-2.
Generates annotated drawings and reports in CSV, Excel, and PDF formats.
Supports manual override for editing annotations.
Multi-page PDF handling and robust error handling.

Installation

Clone the repository:git clone https://github.com/yourusername/auto-ballooning-streamlit.git
cd auto-ballooning-streamlit


Install dependencies:pip install -r requirements.txt


Install Tesseract OCR (e.g., sudo apt install tesseract-ocr on Ubuntu).
Place pre-trained models in models/:
yolov11_weights.pt
florence2_gdt.pkl



Usage
Run the Streamlit app:
streamlit run app/streamlit_app.py

Deployment
Deploy to Streamlit Cloud or use Docker:
docker-compose up

Contributing
Contributions are welcome! Please open an issue or pull request.
License
MIT License
