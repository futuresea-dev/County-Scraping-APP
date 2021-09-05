from pdf2image import convert_from_path
import pytesseract
import cv2
from PIL import Image
import re



pdfs = r"export (1).pdf"
pages = convert_from_path(pdfs, 300)

i = 1
image_name = "Page_" + str(i) + ".jpg"


pages[0].save(image_name, "JPEG")
image = cv2.imread(image_name)



# get co-ordinates to crop the image
# c = line_items_coordinates[1]
#
# # cropping image img = image[y0:y1, x0:x1]
# img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]
#
# plt.figure(figsize=(10,10))
# plt.imshow(img)

# convert the image to black and white for better OCR
ret,thresh1 = cv2.threshold(image,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
print(text)
csv_json = {}
lists = text.split("\n")
for faxs in lists:
    fax_list = faxs.split(" ")
    if len(fax_list) == 5:
        if fax_list[0].isnumeric() and int(fax_list[0]) > 1900 and int(fax_list[0]) < 2021:
            j_key = "DUE AMOUNT FOR " + fax_list[0]
            csv_json[j_key] = fax_list[4]
    elif faxs.find("TOTAL") > -1 and faxs.find("AMOUNT") > -1:
        total_fax = faxs.replace(" ", "").replace("-", ".").replace(":", "").replace("O", "0")
        res = re.findall("\d+,\d+\.\d+", total_fax)
        res1 = re.findall("\d+\.\d+", total_fax)
        if len(res) > 0:
            csv_json["GRAND TOTAL TAXS 1900-2020"] = str(res[0])[1:]
        elif len(res1) > 0:
            csv_json["GRAND TOTAL TAXS 1900-2020"] = str(res1[0])[1:]
        else:
            csv_json["GRAND TOTAL TAXS 1900-2020"] = "0.00"

