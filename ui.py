import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys

try:
    from core.engine import extract_invoice_data
except ImportError as e:
    print(f"Error loading engine: {e}")
    sys.exit(1)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF to Excel Extractor")
        self.geometry("450x250")
        
        self.label = ctk.CTkLabel(self, text="Smart Invoice Extractor", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)
        
        self.btn_upload = ctk.CTkButton(self, text="Upload PDF", command=self.upload_file, width=200, height=40)
        self.btn_upload.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self, text="Ready to process...", text_color="gray")
        self.status_label.pack(pady=10)

    def upload_file(self):
        input_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if input_path:
            output_dir = "data/output"
            os.makedirs(output_dir, exist_ok=True)
            file_name = os.path.basename(input_path).replace(".pdf", ".xlsx")
            output_path = os.path.join(output_dir, file_name)
            
            self.status_label.configure(text=f"Processing: {os.path.basename(input_path)}...", text_color="orange")
            self.update()
            
            try:
                extract_invoice_data(input_path, output_path)
                self.status_label.configure(text="Extraction Successful!", text_color="green")
                messagebox.showinfo("Success", f"File created at:\n{output_path}")
            except Exception as e:
                self.status_label.configure(text="Error occurred", text_color="red")
                messagebox.showerror("Error", f"Failed to extract:\n{str(e)}")

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()
