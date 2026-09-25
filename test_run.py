from core.engine import extract_invoice_data
import os

# تجهيز مجلد للمخرجات
os.makedirs("output", exist_ok=True)

# استبدل 'sample.pdf' باسم أي فاتورة موجودة لديك في نفس المجلد
pdf_file = "sample.pdf" 
excel_file = "output/result.xlsx"

if os.path.exists(pdf_file):
    print("Processing...")
    result = extract_invoice_data(pdf_file, excel_file)
    print(result)
else:
    print(f"Please put a PDF invoice named '{pdf_file}' in the folder first.")
