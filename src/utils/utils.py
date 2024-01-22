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



def image_cut(img_path,cordenadas: list, area_aumentada_w=0, area_aumentada_h=0):
    # Leia a imagem
    imagem = cv2.imread(img_path)

    # Defina as coordenadas da área desejada
    x, y, w, h = cordenadas

    # Corte a imagem para incluir apenas a área desejada -
    # as somas e subtrações são pra permitir uma margem de distorção da placa
    area_desejada = imagem[int(y+10):int(h), int(x+5):int(w-5)]

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



def get_txt_tessereact_plus(img_path):
    # Carregando a imagem
    imagem_path = f'{img_path}/imagecut.png'  # Substitua pelo caminho da sua imagem
    imagem = cv2.imread(imagem_path)

    # Verificando se a imagem foi carregada corretamente
    if imagem is None:
        print("Erro ao carregar a imagem.")
    else:
        print("Imagem carregada com sucesso.")

    # PRE PROCESSAMENTO

    # Convertendo a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicando binarização (thresholding)
    _, imagem_binaria = cv2.threshold(imagem_cinza, 90, 255, cv2.THRESH_BINARY)

    # img = cv2.imread(imagem_path, cv2.IMREAD_GRAYSCALE)
    # # img = cv2.medianBlur(img,5)
    # imagem_processada = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # Aplicando um filtro para remover ruídos (opcional)
    imagem_sem_ruido = cv2.medianBlur(imagem_binaria, 1)

    imagem_processada = imagem_sem_ruido

    # # Ajustando o contraste (opcional)
    # alpha = 1.5  # Fator de contraste
    # beta = 50    # Fator de brilho
    # imagem_processada = cv2.convertScaleAbs(imagem_sem_ruido, alpha=alpha, beta=beta)

    # Exibindo a imagem original e a imagem processada
    cv2.imshow('Imagem Original', imagem)
    cv2.imshow('Imagem Processada', imagem_processada)
    cv2.waitKey(0)
    # input()
    cv2.destroyAllWindows()

    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
    res = pytesseract.image_to_string(imagem_processada,config =custom_config)

    return res

def teste():
    import cv2 as cv
    import numpy as np
    from matplotlib import pyplot as plt
    img = cv.imread('/mnt/sda1/stefany/tcc/tcc-rep/midias/imagecut.png', cv.IMREAD_GRAYSCALE)
    # assert img is not None, "file could not be read, check with os.path.exists()"
    img = cv.medianBlur(img,1)
    ret,th1 = cv.threshold(img,110,255,cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY,11,2)
    th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY,11,2)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
                'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]

    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    # custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
    
    list_permited = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Crie um objeto Reader
    reader = easyocr.Reader(['pt'], gpu=False)
    # Leia a imagem da área desejada

    for i in range(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        # res = pytesseract.image_to_string(images[i],config =custom_config)
        resultados = reader.readtext(images[i], allowlist=list_permited)
        res = resultados[0][1]
        plt.title(f'{titles[i]} = {res}')
        plt.xticks([]),plt.yticks([])

    plt.show()

if __name__ == "__main__":
    # print(get_txt_tessereact_plus('/mnt/sda1/stefany/tcc/tcc-rep/midias'))
    teste()
