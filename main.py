# Importações
from ultralytics import YOLO
import cv2

# Constantes
ROOT_PATH = '/home/stefany/Documentos/tcc/tcc-rep'


# Carregando Modelo
model_detector_carros = YOLO('yolov8n.pt') # Detectar Carros (Modelo Pre-treinado)
model_detector_placas = YOLO(f'{ROOT_PATH}/models/best_detector_placas.pt') # Placas

#Carregando vídeo/imagem
cap = cv2.VideoCapture(f'{ROOT_PATH}/midias/videoplayback.mp4')

print("lendo frames")
# Lendo frames
ret = True
frame_num = -1

while ret:
    #Ler frames do vídeo
    ret, frame = cap.read()

    if ret and frame_num < 10:
        # Detectando vartices
        deteccao = model_detector_carros(frame)[0]
        print(deteccao)
    