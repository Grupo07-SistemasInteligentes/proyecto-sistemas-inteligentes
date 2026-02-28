from fpdf import FPDF
import os

# Crear carpeta temp si no existe
os.makedirs("temp", exist_ok=True)

# PDF 1: Normal
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Un algoritmo es una secuencia ordenada de pasos para resolver un problema.", ln=True)
pdf.cell(200, 10, txt="Por ejemplo, para calcular el promedio de una lista: sum(lista)/len(lista)", ln=True)
pdf.output("temp/entrega_normal.pdf")

# PDF 2: Copia (similar al 1)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Un algoritmo consiste en pasos ordenados que resuelven un problema.", ln=True)
pdf.cell(200, 10, txt="Ejemplo: promedio = sum(lista)/len(lista)", ln=True)
pdf.output("temp/entrega_copia.pdf")

# PDF 3: Off-topic
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="HTML es un lenguaje de marcado para crear páginas web.", ln=True)
pdf.cell(200, 10, txt="Las etiquetas como <div> y <p> definen la estructura.", ln=True)
pdf.output("temp/entrega_offtopic.pdf")

print("✅ PDFs de prueba creados en carpeta 'temp/'")