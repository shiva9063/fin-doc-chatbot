import pandas as pd
import os
def excel_read(uploaded_file,EXCEL_DIR):
    # save file 
    save_path = os.path.join(EXCEL_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


    # read file and extract the text
    df = pd.read_excel(uploaded_file, sheet_name=None)  # all sheets
    text = ""
    for sheet, data in df.items():
        text += f"--- Sheet: {sheet} ---\n"
        text += data.to_string(index=False) + "\n"
    return text