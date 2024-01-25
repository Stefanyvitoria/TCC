import RPi.GPIO as GPIO
import time, subprocess, os
from src.classes.GPIO_PIN import Pin_Button
from src.classes.Detector import Detector
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env


class App:
    def __init__(self) -> None:
        self.image_original_path = os.getenv('IMAGEM_ORIGINAL_PATH')
        self.detector = Detector()
        self.__pins = {
            'button_main': Pin_Button(int(os.getenv('PIN_NUMBER_BUTTON_MAIN'))),
            'led_button_main':Pin_Button(int(os.getenv('PIN_NUMBER_LED_BUTTON_MAIN')))
        }

        self.__configuracoes_pins()
        self.run()


    def run(self) -> None:

        print("APP inicializado!")
        while True:
            self.__pins['led_button_main'].ligar() # acende o led led de processamento
    
            # Se houver evento e for uma acionada no botão
            if GPIO.event_detected(self.__pins['button_main'].number) and (GPIO.input(self.__pins['button_main'].number) == False):
                
                print('gatilho disparado!')
                self.__pins['led_button_main'].desligar() #Desliga o led
                self.__tirar_foto() # Captura a foto

                print(self.detector.get_text(self.image_original_path))

                input()


            time.sleep(0.1)

        GPIO.cleanup()
        print("APP Finalizado!")


    def __tirar_foto(self) -> None:
        print("Capturando imagem.")
        subprocess.run(f"libcamera-still -o {self.image_original_path} -t 0.1", shell=True)
        print(f'imagem: {self.image_original_path}')


    def __configuracoes_pins(self) -> None:

        print("Configurando GPIO.")

        # Configura o modo de numeração dos pinos
        GPIO.setmode(GPIO.BCM)

        # Configura o pino como entrada
        GPIO.setup(self.__pins['button_main'].number, GPIO.IN, pull_up_down=GPIO.PUD_UP) #PUD_UP PUD_DOWN
        GPIO.add_event_detect(self.__pins['button_main'].number, GPIO.RISING)

        #configura o pino como saída
        GPIO.setup(self.__pins['led_button_main'].number, GPIO.OUT)

        print("GPIO configurada.")