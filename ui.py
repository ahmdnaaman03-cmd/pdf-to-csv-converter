import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from core.engine import extract_invoice_data

ctk.set_appearance_mode("dark")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x250")
        self.btn = ctk.CTkButton(self, text="Upload Invoice", command=self.upload)
        self.btn.place(relx=0.5, rely=0.5, anchor="center")

    def upload(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            os.makedirs("data/output", exist_ok=True)
            out = "data/output/result.xlsx"
            try:
                extract_invoice_data(path, out)
                messagebox.showinfo("Success", "Excel created successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    App().mainloop()
