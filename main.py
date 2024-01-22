"""
Autor: @Stefanyvitoria
Data: 12/2023
Descrição: Script principal da aplicação. 
"""

from PIL import Image
from ultralytics import YOLO
from src.utils.utils import *

# Constantes
ROOT_PATH = '/mnt/sda1/stefany/tcc/tcc-rep'


# Carregando Modelo
model_detector_placas = YOLO(f'{ROOT_PATH}/detect/train-100/weights/best.pt') # Placas

# Caminho para a imagem que você deseja analisar
# img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/img_000001.jpg"
img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/img_010002.jpg"
# img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/teste01.png"
# img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/carro.jpeg"

# Carrega a imagem
img = Image.open(img_path)

# Detecta as placas na imagem
results = model_detector_placas(img)[0]

cordenadas = results.boxes.data.tolist()[0][0:4]
confianca_placa = results.boxes.conf[0]

# Desenha uma caixa em torno da placa detectada
draw_bounding_box(img_path, cordenadas)

img_cut_path = image_cut(img_path=img_path, cordenadas=cordenadas)

print(f'easyocr= {get_txt(img_cut_path)}')
print(f'pytesseract= {get_txt_tessereact(img_cut_path)}')
print(f'ocropus= {get_txt_pyocr(img_cut_path)}')
print(f'tessereact_plus= {get_txt_tessereact_plus(img_cut_path)}')

