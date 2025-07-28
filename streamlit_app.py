
import sys
sys.path.append(r"C:\Users\user\Documents\Ballooning-Software")
from app.extractor import PDFDimensionExtractor
import streamlit as st
from app.extractor import PDFDimensionExtractor
from app.sym_detector import YOLOGDTSymbolDetector
from app.vl_parser import GDTParser
from app.drawer import BalloonDrawer
from app.report import ReportGenerator
from app.utils import pdf_to_images, load_config

st.title("✅ Advanced Auto-Ballooning & GD&T Inspection App")
config = load_config()
uploaded = st.file_uploader("Upload your drawing (PDF/image)", type=["pdf", "jpg", "png"])

if uploaded:
    path = f"temp.{uploaded.type.split('/')[-1]}"
    with open(path, "wb") as f:
        f.write(uploaded.read())
    
    images = pdf_to_images(path) if path.endswith('.pdf') else [Image.open(path)]
    all_dims, all_syms, all_gdt = [], [], []
    
    for page_num, img in enumerate(images):
        # Extract dimensions
        extractor = PDFDimensionExtractor(path)
        text_data = extractor.extract_text(img)
        dims = extractor.filter_dimensions(text_data)
        all_dims.extend([{'page': page_num+1, **dim} for dim in dims])
        
        # Detect GD&T symbols
        detector = YOLOGDTSymbolDetector(config['model_paths']['yolo'])
        sym_regions = detector.detect(img)
        all_syms.extend([{'page': page_num+1, **sym} for sym in sym_regions])
        
        # Parse GD&T data
        parser = GDTParser(config['model_paths']['florence'])
        gdt_records = [parser.parse(img.crop(sym['bbox'][0])) for sym in sym_regions]
        all_gdt.extend([{'page': page_num+1, **rec} for rec in gdt_records])
        
        # Draw balloons
        drawer = BalloonDrawer(img)
        annotated_img = drawer.draw(dims, sym_regions, gdt_records)
        st.image(annotated_img, caption=f"Page {page_num+1}: Annotated Drawing", use_column_width=True)
    
    # Generate reports
    report = ReportGenerator(all_dims, all_gdt)
    csv_path = report.generate_csv()
    pdf_path = report.generate_pdf()
    
    with open(csv_path, "rb") as f:
        st.download_button("Download CSV Report", f, file_name="inspection_report.csv")
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF Report", f, file_name="inspection_report.pdf")
    
    # Manual override
    st.subheader("Manual Override")
    balloon_num = st.number_input("Balloon Number to Edit", min_value=1, max_value=len(all_dims)+len(all_gdt))
    new_value = st.text_input("New Value")
    if st.button("Update"):
        if balloon_num <= len(all_dims):
            all_dims[balloon_num-1]['text'] = new_value
        else:
            all_gdt[balloon_num-len(all_dims)-1]['tolerance'] = new_value
        st.success("Updated successfully!")
