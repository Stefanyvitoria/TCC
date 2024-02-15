from ultralytics import YOLO
from PIL import Image, ImageDraw
import os, cv2, easyocr
from matplotlib import pyplot as plt
from google.cloud import vision


class Detector:
    def __init__(self) -> None:
        self.detector_LP = YOLO(os.getenv('MODEL_FILE'))
        self.img_drawer = f"{os.getenv('MIDIAS_PATH')}/imagem-desenhada.png"
        self.img_cut = f"{os.getenv('MIDIAS_PATH')}/imagem-cortada.png"
    
    def get_text(self, img_path : str):
        print("Iniciando Detecção")

        # Carrega a imagem
        img = Image.open(img_path)

        # Detecta as placas na imagem
        results = self.detector_LP(img)[0]
        # print(results)
        
        if len(results.boxes.data.tolist()) > 0:
            results_data = results.boxes.data.tolist()[0]
            cordenadas = results_data[0:4]
            classe_id = results_data[5]

            self.draw_bounding_box(img_path, cordenadas)
            self.cut_image(img_path, cordenadas)
            text = self.OCR()

            # TODO: Verifica se o texto detectado está na máscara
            
            return (classe_id, text)
        
        return (-1, "Sem deteccoes")

    def OCR(self):
        client = vision.ImageAnnotatorClient()

        with open(self.img_cut, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)


        txt = response.full_text_annotation.text

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        return txt

    def cut_image(self,image_path: str ,cordenadas: list):
        # Le a imagem
        imagem = cv2.imread(image_path)

        # Define as coordenadas da área desejada
        x, y, w, h = cordenadas

        # Corta a imagem para incluir apenas a área desejada -
        # as somas e subtrações são pra permitir uma margem de distorção da placa
        area_aumentada_w=5
        area_aumentada_h=10
        area_desejada = imagem[int(y+area_aumentada_h):int(h), int(x+area_aumentada_w):int(w-area_aumentada_w)]

        # Salva a área desejada como uma nova imagem
        cv2.imwrite(self.img_cut, area_desejada)

    def draw_bounding_box(self, image_path: str, cordenadas: list):
        # Open image
        image = Image.open(image_path)

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Draw bounding box
        draw.rectangle(cordenadas, outline='red')

        # Save the image
        image.save(self.img_drawer)
