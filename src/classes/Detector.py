from ultralytics import YOLO
from PIL import Image, ImageDraw
import os


class Detector:
    def __init__(self) -> None:
        self.detector_LP = YOLO(os.getenv('MODEL_FILE'))
        self.img_drawer = f"{os.getenv('MIDIAS_PATH')}/imagem-desenhada.png"
    
    def get_text(self, img_path : str):
        print("Iniciando Detecção")

        # Carrega a imagem
        img = Image.open(img_path)

        # Detecta as placas na imagem
        results = self.detector_LP(img)[0]
        results_data = results.boxes.data.tolist()[0]
        cordenadas = results_data[0:4]
        classe_id = results_data[5]

        self.draw_bounding_box(img_path, cordenadas)

        return (cordenadas, classe_id)
        
    def draw_bounding_box(self, image_path: str, cordenadas: list):
        # Open image
        image = Image.open(image_path)

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Draw bounding box
        draw.rectangle(cordenadas, outline='red')

        # Save the image
        image.save(self.img_drawer)
