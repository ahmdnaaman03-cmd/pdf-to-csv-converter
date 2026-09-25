import pypdf
import pandas as pd
import re
import os

def extract_invoice_data(pdf_path, output_excel_path):
    if not os.path.exists(pdf_path):
        return f"Error: File {pdf_path} not found."

    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # التعبيرات النمطية لصيد البيانات الأساسية
    invoice_no = re.search(r"(?:Invoice\s*No|Invoice\s*Number|رقم\s*الفاتورة)[\s:\-]*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    total = re.search(r"(?:Total|الإجمالي|المبلغ)[\s:\-]*([0-9.,]+)", text, re.IGNORECASE)
    date = re.search(r"(?:Date|التاريخ)[\s:\-]*([0-9/.\-]+)", text, re.IGNORECASE)

    data = {
        "رقم الفاتورة": [invoice_no.group(1) if invoice_no else "غير متوفر"],
        "التاريخ": [date.group(1) if date else "غير متوفر"],
        "الإجمالي": [total.group(1) if total else "غير متوفر"]
    }

    # حفظ البيانات في ملف إكسيل
    df = pd.DataFrame(data)
    df.to_excel(output_excel_path, index=False)
    return f"Success: Saved to {output_excel_path}"
