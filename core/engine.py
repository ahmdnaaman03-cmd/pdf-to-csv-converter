import pypdf
import pandas as pd
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key is missing. Please set GEMINI_API_KEY in .env file.")

genai.configure(api_key=api_key)

def extract_invoice_data(pdf_path, excel_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    اقرأ الفاتورة التالية واستخرج منها البيانات المطلوبة بدقة بغض النظر عن لغة الفاتورة أو التنسيق.
    يجب أن يكون الرد عبارة عن كائن JSON صحيح فقط (Valid JSON) يحتوي على المفاتيح التالية:
    - "Invoice Number"
    - "Date"
    - "Total"
    إذا لم تجد قيمة معينة، اكتب "غير متوفر".
    لا تكتب أي نصوص أخرى خارج الـ JSON.
    
    نص الفاتورة:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        res_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(res_text)
        invoice_no = data.get("Invoice Number", "غير متوفر")
        date_val = data.get("Date", "غير متوفر")
        total_val = data.get("Total", "غير متوفر")
    except Exception as e:
        invoice_no, date_val, total_val = "خطأ في القراءة", "خطأ في القراءة", "خطأ في القراءة"

    df = pd.DataFrame([{
        "رقم الفاتورة": invoice_no,
        "التاريخ": date_val,
        "الإجمالي": total_val
    }])
    df.to_excel(excel_path, index=False)
