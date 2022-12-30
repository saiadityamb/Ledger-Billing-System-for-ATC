# from fpdf import FPDF,HTMLMixin
# class MyFPDF(FPDF, HTMLMixin):
#     pass
# with open("WholeSellerBijak.html",'r') as f:
#     data = f.read()
# pdf  = MyFPDF()
# # pdf.set_font("Arial",'B',24)
# pdf.add_page()
# pdf.write_html(data)
# pdf.output("mbsa.pdf",'F')



# Importing required module
import os
# Using system() method to
# execute shell commands
link = "http://127.0.0.1:5500/-MtTA1tivomDJ-JhjZl9/bijak/-Mv9ckVFgXWliAAMt4jl"
filename = 'mbsambsa.pdf'
cmd = f'wkhtmltopdf {link} {filename}'
print(cmd)
os.system(f"start /B start cmd.exe @cmd /k {cmd}")