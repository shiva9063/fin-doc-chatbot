from PyPDF2 import PdfReader
import os
def pdf_read(uploaded_file,PDF_DIR):
    # save file
    save_path = os.path.join(PDF_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # read file and extract the text
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text