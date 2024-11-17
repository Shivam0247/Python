import csv
import os
from fpdf import FPDF
from PyPDF2 import PdfMerger
from datetime import datetime

os.makedirs("invoices", exist_ok=True)

class InvoicePDF(FPDF):
    
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Invoice", ln=True, align="C")
        self.ln(10)

    def add_invoice_details(self, order_id, date, customer, product, quantity, unit_price, total):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Invoice Number: {order_id}", ln=True)
        self.cell(0, 10, f"Date of Purchase: {date}", ln=True)
        self.cell(0, 10, f"Customer Name: {customer}", ln=True)
        self.cell(0, 10, f"Product: {product}", ln=True)
        self.cell(0, 10, f"Quantity: {quantity}", ln=True)
        self.cell(0, 10, f"Unit Price: {unit_price} INR", ln=True)
        self.cell(0, 10, f"Total Amount: {total} INR", ln=True)

def generate_invoice(order):
    order_id, customer, product, quantity, unit_price = order
    quantity = int(quantity)
    unit_price = float(unit_price)
    total = quantity * unit_price

    pdf = InvoicePDF()
    pdf.add_page()
    pdf.add_invoice_details(
        order_id=order_id,
        date=datetime.today().strftime('%Y-%m-%d'),
        customer=customer,
        product=product,
        quantity=quantity,
        unit_price=unit_price,
        total=total,
    )

    pdf_filename = f"invoices/{order_id}.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def merge_pdfs(pdf_files, output_file):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_file)
    merger.close()

def main():
    orders = []
    with open("/Users/patelshivam/Documents/PythonLab/Practical 12/Syllabus.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  
        orders = list(reader)

    pdf_files = [generate_invoice(order) for order in orders]

    merge_pdfs(pdf_files, "Subject.pdf")
    print("All invoices merged into 'Subject.pdf' successfully.")

if __name__ == "__main__":
    main()
