import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from decimal import Decimal


csv_json = {}
pdfFile = wi(filename="export (1).pdf", resolution=260)

image = pdfFile.convert('jpeg')

imageBlobs = []

for img in image.sequence:
    imgPage = wi(image=img)
    imageBlobs.append(imgPage.make_blob('jpeg'))

extract = []

for imgBlob in imageBlobs:
    image = Image.open(io.BytesIO(imgBlob))
    text = pytesseract.image_to_string(image, lang='eng')
    extract.append(text)

result = extract[0]
lists = result.split("\n")
for faxs in lists:
    fax_list = faxs.split(" ")
    if len(fax_list) == 5:
        if fax_list[0].isnumeric() and int(fax_list[0]) > 1900 and int(fax_list[0]) < 2021:
            j_key = "DUE AMOUNT FOR " + fax_list[0]
            csv_json[j_key] = fax_list[4]
    # elif faxs.find("TOTAL") > -1 and faxs.find("AMOUNT") > -1:
    #     total_fax = faxs.replace(" ", "").replace("-", ".")
    #     res = re.findall("\d+,\d+\.\d+", total_fax)
    #     res1 = re.findall("\d+\.\d+", total_fax)
    #     if len(res) > 0:
    #         csv_json["GRAND TOTAL TAXS 1900-2020"] = str(res[0])[1:]
    #     elif len(res1) > 0:
    #         csv_json["GRAND TOTAL TAXS 1900-2020"] = str(res1[0])[1:]
    #     else:
    #         csv_json["GRAND TOTAL TAXS 1900-2020"] = "0.00"
sum = 0
for key, each_year in csv_json.items():
    k = each_year
    sum = sum + Decimal(each_year.replace(",", ""))
csv_json["GRAND TOTAL TAXS 1900-2020"] = f"{sum:,}"
print(csv_json)

