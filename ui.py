import customtkinter as ctk
from tkinter import filedialog

# إعدادات المظهر
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class InvoiceConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # إعدادات النافذة
        self.title("PDF to Excel - MVP")
        self.geometry("400x250")
        
        # زر الرفع الوحيد
        self.upload_btn = ctk.CTkButton(
            self, 
            text="Upload File", 
            command=self.upload_file,
            width=200, 
            height=50,
            font=("Arial", 16, "bold")
        )
        self.upload_btn.place(relx=0.5, rely=0.5, anchor="center")
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF Invoice",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            print(f"File selected: {file_path}")

if __name__ == "__main__":
    app = InvoiceConverterApp()
    app.mainloop()
