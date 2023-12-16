# Importações
from ultralytics import YOLO

def train_model():
    # Load a model
    model = YOLO("yolov8n.yaml")  # build a new model from scratch
    # model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Use the model
    model.train(data="./config.yaml", epochs=1)  # train the model



if __name__ == '__main__':
    train_model()