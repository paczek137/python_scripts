# author: paczek

import datetime
import os
import sys
import PyPDF2
from PIL import Image

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
print(s)

# if (len(sys.argv) != 2):
#     print("\nUsage: python {} input_file\n".format(sys.argv[0]))
#     sys.exit(1)

input_pdf = "C:\git\python\python_scripts\quiz.pdf"

pdf = PyPDF2.PdfFileReader(open(input_pdf, "rb"))
page0 = pdf.getPage(6)

if '/XObject' in page0['/Resources']:
    xObject = page0['/Resources']['/XObject'].getObject()

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj].getData()
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if '/Filter' in xObject[obj]:
                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    img.save(obj[1:] + ".png")
                    print("Found png")
                elif xObject[obj]['/Filter'] == '/DCTDecode':
                    img = open(obj[1:] + ".jpg", "wb")
                    img.write(data)
                    img.close()
                    print("Found jpg")
                elif xObject[obj]['/Filter'] == '/JPXDecode':
                    img = open(obj[1:] + ".jp2", "wb")
                    img.write(data)
                    img.close()
                    print("Found jp2")
                elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                    img = open(obj[1:] + ".tiff", "wb")
                    img.write(data)
                    img.close()
                    print("Found jp2")
            else:
                img = Image.frombytes(mode, size, data)
                img.save(obj[1:] + ".png")
                print("Found png2")
else:
    print("No image found.")