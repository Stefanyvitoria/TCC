"""
Autor: @Stefanyvitoria
Data: 01/2024
Descrição: Script principal da aplicação. 
"""

from PIL import Image, ImageDraw
import cv2, easyocr
import matplotlib.pyplot as plt
import pyocr 
import pyocr.builders

import pytesseract , cv2


def get_txt_tessereact_plus(img_path):
    pass


def get_txt_pyocr(img_path):
    image_cut=f'{img_path}/imagecut.png'
    image = Image.open(image_cut)

    tools = pyocr.get_available_tools() 
    if len(tools) == 0:
        return("No OCR tool found.") 

    ocr_tool = tools[1]
    text = ocr_tool.image_to_string( image, builder=pyocr.builders.TextBuilder() )

    return text




def get_txt_tessereact(img_path):
    # pytesseract.pytesseract.tesseract_cmd = r'/home/stefany/Documentos/pytesseract-0.3.10/pytesseract/pytesseract.py'
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    
    # print(img_path)
    image=f'{img_path}/imagecut.png'
    img = cv2.imread(image)

    custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
    # '--psm 7 --oem 1 tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = pytesseract.image_to_string(img,config =custom_config)

    return res

# def get_txt_keras(img_path):
#     pipeline = keras_ocr.pipeline.Pipeline()

#     images = [
#         keras_ocr.tools.read(url) for url in [
#             '/mnt/sda1/stefany/tcc/tcc-rep/midias/img_010002.jpg'
#         ]
#     ]

#     # Each list of predictions in prediction_groups is a list of
#     # (word, box) tuples.
#     prediction_groups = pipeline.recognize(images)

#     # Plot the predictions
#     fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
#     for ax, image, predictions in zip(axs, images, prediction_groups):
#         keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)



def get_txt(img_cut_path):

    list_permited = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Crie um objeto Reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Leia a imagem da área desejada
    resultados = reader.readtext(f'{img_cut_path}/imagecut.png', allowlist=list_permited)

    res = resultados[0][1]

    return res

    # for resultado in resultados:
    #     print(f'{resultado[1]}')



def image_cut(img_path,cordenadas: list, area_aumentada=0):
    # Leia a imagem
    imagem = cv2.imread(img_path)

    # Defina as coordenadas da área desejada
    x, y, w, h = cordenadas

    # Corte a imagem para incluir apenas a área desejada -
    # as somas e subtrações são pra permitir uma margem de distorção da placa
    area_desejada = imagem[int(y-area_aumentada):int(h+area_aumentada), int(x-area_aumentada):int(w+area_aumentada)]

    img_path_cut = "/".join(img_path.split("/")[:-1])
    # Salve a área desejada como uma nova imagem
    cv2.imwrite(f'{img_path_cut}/imagecut.png', area_desejada)

    return img_path_cut


def draw_bounding_box(image_path, coordinates):
    # Open image
    image = Image.open(image_path)

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Draw bounding box
    draw.rectangle(coordinates, outline='red')

    # Save the image
    image.save('/mnt/sda1/stefany/tcc/tcc-rep/midias/output.png')