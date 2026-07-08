import pypdf, csv, os, re

def extract_pdf_data(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    raw_rows = []
    max_cols = 0
    with open(input_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if not text: continue
            for line in text.split('\n'):
                clean_line = re.sub(r'[^a-zA-Z0-9\s.,;:_\-+\-*/=%&@#$()\[\]]', '', line).strip()
                if not clean_line: continue
                row_data = clean_line.split()
                if row_data:
                    raw_rows.append(row_data)
                    if len(row_data) > max_cols: max_cols = len(row_data)
    if not raw_rows:
        raise ValueError("No valid English or numeric data found.")
    standardized_rows = [r + [''] * (max_cols - len(r)) for r in raw_rows]
    headers = [f"Column_{i}" for i in range(1, max_cols + 1)]
    with open(output_path, mode='w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        writer.writerows(standardized_rows)
    return f"Success! Standardized to {max_cols} columns."

