import RPi.GPIO as GPIO
import time, subprocess, os
from src.classes.GPIO_PIN import Pin_Button
from src.classes.Detector import Detector
from src.classes.Display import Display
from src.classes.Semaforo import Semaforo
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env


class App:
    def __init__(self) -> None:
        self.image_original_path = os.getenv('IMAGEM_ORIGINAL_PATH')
        self.detector = Detector()
        self.display = Display()
        self.semaforo = Semaforo()
        self.__pins = {
            'button_main': Pin_Button(int(os.getenv('PIN_NUMBER_BUTTON_MAIN'))),
            'led_button_main':Pin_Button(int(os.getenv('PIN_NUMBER_LED_BUTTON_MAIN')))
        }

        self.__configuracoes_pins()
        self.run()


    def run(self) -> None:

        entrada = '' # TODO: Remover
        print("APP inicializado!")
        while True:
            self.__pins['led_button_main'].ligar() # acende o led led de processamento
    
            # Se houver evento e for uma acionada no botão
            if GPIO.wait_for_edge(self.__pins['button_main'].number, GPIO.RISING):
                
                print('\ngatilho disparado!')
                self.__pins['led_button_main'].desligar() #Desliga o led
                self.__tirar_foto() # Captura a foto

                classe, resultado_placa = self.detector.get_text(self.image_original_path)
                print(resultado_placa)

                self.display.set_text(resultado_placa)

                entrada = input("aperte qualquer tecla para continuar?")
                self.display.clean()

            time.sleep(0.1)

            if entrada == 'fim': # TODO: Remover
                break

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