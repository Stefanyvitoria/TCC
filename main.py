"""
Autor: @Stefanyvitoria
Data: 12/2023
Descrição: Script principal da aplicação. 
"""

import cv2, time

from sort.sort import *

# Constantes
ROOT_PATH = '/mnt/sda1/stefany/tcc/tcc-rep'

mot_tracker = Sort()

# Carregando Modelo
model_detector_carros = YOLO('yolov8n.pt') # Detectar Carros (Modelo Pre-treinado)
model_detector_placas = YOLO(f'{ROOT_PATH}/detect/train-100/weights/best.pt') # Placas


veiculos = [2,3,5,7]

# Lendo frames
frame_num = -1
ret = True

while ret:

    frame_num += 1

    #Ler frames do vídeo
    ret, frame = cap.read()

    if ret and frame_num < 10:
        # Detectando vartices
        deteccoes = model_detector_carros(frame)[0]
        # print(deteccao)
        deteccoes_ = []

        for deteccao in deteccoes.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = deteccao
            if int(class_id) in veiculos:
                deteccoes_.append([x1, y1, x2, y2, score])


        # rastreia os veiculos
        track_ids = mot_tracker.update(np.asarray(deteccoes_))

        print(track_ids)
