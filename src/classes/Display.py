from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
from time import sleep
import os


class Display:
    def __init__(self) -> None:
        self.fonte = ImageFont.truetype(os.getenv('FONTE'),int(os.getenv('FONT_SIZE')))
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)

    def set_text(self, text:str):
        # Box and text rendered in portrait mode - sudo i2cdetect -y 1
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((5, 13), text, font=self.fonte, fill="white")
      
    
    def clean(self):
        self.device.cleanup()
        

if __name__ == '__main__':

    from dotenv import load_dotenv
    load_dotenv() 
    
    disp = Display()
    disp.set_text("Sem Placas")