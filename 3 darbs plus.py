import os

folder="invoices"

for count, filename in enumerate(os.listdir(folder)):        /// to rename files in a folder
    dst=f"invoice_{str(count)}.pdf"
    src = f"{folder}/{filename}"
    dst=f"{folder}/{dst}"
    os.rename(src,dst)

import PyPDF2
import pathlib
from tabulate import tabulate                              // read from pdf. find specifiskus datus un put them in  a tabula
data=[]                                                    // first print text then from that find pos of things and to pritn specifik atrast no pos(priekša) un pos (aizmugurē)
adrese = pathlib.Path("invoices")
visi_faili=list(adrese.glob("*.pdf"))
for f in range(len(visi_faili)):
    row=[]
    pdf_file=PyPDF2.PdfReader(open(visi_faili[f],"rb"))
    number_of_pages=len(pdf_file.pages)
    page1=pdf_file.pages[0]
    page2=pdf_file.pages[1]

    text1=page1.extract_text()
    text2=page2.extract_text()

    pos1 = text1.find("Apmaksai:")
    pos2 = text1.find("Elektroenerģijas patēriņš kopā")

    summa = text1[pos1+10:pos2].rstrip()
    row.append(summa)
    pos1 = text2.find("Apjoms Mērv. Cena,")
    per = text2[pos1-23:pos1]
    row.append(per)
    data.append(row)
print(tabulate(data,headers=["Summa", "Periods"], tablefmt="github"))



from PyPDF2 import PdfReader, PdfWriter                                // merge pdf files in one file if need be
def merge_pdf(input_file, output_file):
    result=PdfWriter()
    for file in input_file:
        reader=PdfReader(file)
        for page in reader.pages:
            result.add_page(page)
          
    with open(output_file, "wb") as f:
        result.write(f)
input_file=['invoices/invoice_0.pdf','invoices/invoice_1.pdf', 'invoices/invoice_2.pdf']
output_file='result.pdf'
merge_pdf(input_file,output_file)


from PyPDF2 import PdfReader, PdfWriter                      /// split files if need be
def split_pdf(file_name, prefix):
    pdf_read=PdfReader(file_name)
    for page in range(len(pdf_read.pages)):
        output=prefix+"_"+str(page)+".pdf"
        pdf_write=PdfWriter()
        pdf_write.add_page(pdf_read.pages[page])
      
        with (open(output, "wb")) as f:
            pdf_write.write(f)
split_pdf("result.pdf","datne")
