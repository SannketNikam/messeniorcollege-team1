import pytesseract 
import sys

# print(sys.argv[0],sys.argv[1])
image = sys.argv[1]
pytesseract.pytesseract.tesseract_cmd = r'F:\\Installations\\Tesseract-OCR\\tesseract.exe'
with open('text','w') as f:
    f.write(pytesseract.image_to_string(image=image))
    