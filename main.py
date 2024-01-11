"""
Autor: @Stefanyvitoria
Data: 12/2023
Descrição: Script principal da aplicação. 
"""

from PIL import Image, ImageDraw
from ultralytics import YOLO

# Constantes
ROOT_PATH = '/mnt/sda1/stefany/tcc/tcc-rep'

def draw_bounding_box(image_path, coordinates):
    # Open image
    image = Image.open(image_path)

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Draw bounding box
    draw.rectangle(coordinates, outline='red')

    # Save the image
    image.save('/mnt/sda1/stefany/tcc/tcc-rep/midias/output.jpg')

# Carregando Modelo
model_detector_placas = YOLO(f'{ROOT_PATH}/detect/train-100/weights/best.pt') # Placas

# Caminho para a imagem que você deseja analisar
# img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/img_000001.jpg"
img_path = "/mnt/sda1/stefany/tcc/tcc-rep/midias/carro.jpeg"

# Carrega a imagem
img = Image.open(img_path)

# Detecta as placas na imagem
results = model_detector_placas(img)[0]

# Desenha uma caixa em torno da placa detectada
cordenadas = results.boxes.data.tolist()[0][0:4]

draw_bounding_box(img_path, cordenadas)
