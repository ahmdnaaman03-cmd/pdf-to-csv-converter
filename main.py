from core.engine import extract_pdf_data
import os
import glob

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

print("--- Starting Bulk PDF Data Extraction System ---")

# البحث عن جميع ملفات PDF داخل مجلد الـ input
pdf_files = glob.glob(os.path.join(INPUT_DIR, "*.pdf"))

if not pdf_files:
    print(f"No PDF files found in '{INPUT_DIR}'. Please add PDF files and try again.")
else:
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        # إنشاء اسم ملف الـ CSV بناءً على اسم البي دي إف الأصلي
        csv_name = pdf_name.rsplit('.', 1)[0] + ".csv"
        output_file_path = os.path.join(OUTPUT_DIR, csv_name)
        
        print(f"\nProcessing: {pdf_name}...")
        try:
            result = extract_pdf_data(pdf_path, output_file_path)
            print(result)
            if os.path.exists(output_file_path):
                print(f"Saved successfully at: {output_file_path}")
        except Exception as e:
            print(f"Error processing {pdf_name}: {e}")

print("\n--- Process Finished ---")
