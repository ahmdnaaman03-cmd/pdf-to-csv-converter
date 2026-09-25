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
    # رفع الملف مباشرة لجيمناي ليقرأه بصرياً
    uploaded_file = genai.upload_file(path=pdf_path)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """
    استخرج البيانات التالية من هذا المستند المرفق بدقة:
    - "Invoice Number" (رقم الفاتورة أو البوليصة)
    - "Date" (التاريخ)
    - "Total" (إجمالي المبلغ أو صافي المبلغ المطلوب سداده)
    
    يجب أن يكون الرد عبارة عن كائن JSON صحيح فقط (Valid JSON). إذا لم تجد قيمة معينة، اكتب "غير متوفر".
    لا تكتب أي نصوص أخرى خارج الـ JSON.
    """
    
    try:
        response = model.generate_content([uploaded_file, prompt])
        res_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(res_text)
        invoice_no = data.get("Invoice Number", "غير متوفر")
        date_val = data.get("Date", "غير متوفر")
        total_val = data.get("Total", "غير متوفر")
    except Exception as e:
        invoice_no, date_val, total_val = "خطأ", "خطأ", "خطأ"
    finally:
        # حذف الملف من سيرفرات جوجل فوراً بعد المعالجة
        genai.delete_file(uploaded_file.name)

    df = pd.DataFrame([{
        "رقم الفاتورة": invoice_no,
        "التاريخ": date_val,
        "الإجمالي": total_val
    }])
    df.to_excel(excel_path, index=False)
