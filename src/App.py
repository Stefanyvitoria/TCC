import RPi.GPIO as GPIO
import time, subprocess, os
from src.classes.GPIO_PIN import Pin_Button
from src.classes.Detector import Detector
from src.classes.Display import Display
from src.classes.Semaforo import Semaforo
from src.classes.Registrador import Registrador
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env


class App:
    def __init__(self) -> None:
        self.image_original_path = os.getenv('IMAGEM_ORIGINAL_PATH')
        self.detector = Detector()
        self.display = Display()
        self.semaforo = Semaforo()
        self.regitrador = Registrador()
        self.__pins = {
            'button_main': Pin_Button(int(os.getenv('PIN_NUMBER_BUTTON_MAIN'))),
            'led_button_main':Pin_Button(int(os.getenv('PIN_NUMBER_LED_BUTTON_MAIN')))
        }
        self.placas_permitidas = []

        self.get_placas_permitidas()
        self.__configuracoes_pins()
        self.run()


    def run(self) -> None:

        print("APP inicializado!")
        self.display.clean()
        desligar = False

        while True:
            gatilho = False
            
            self.__pins['led_button_main'].ligar() # acende o led que indica processamento

            start_time = time.time()
            while GPIO.input(self.__pins['button_main'].number) == GPIO.LOW:
                gatilho = True
                time.sleep(0.1)
                if time.time() - start_time >= 3.0:
                    desligar = True
                    print("Botão pressionado por 3 segundos ou mais! Desligando...")
                    break
            
            if gatilho and (not desligar):
                self.__pins['led_button_main'].desligar() #Desliga o led

                # self.__tirar_foto() # Captura a foto

                # Realiza a detecção da placa
                classe, resultado_placa = self.detector.get_text(self.image_original_path) 

                if classe != -1: # Se há detecção
                    self.regitrador.gravar_deteccao(resultado_placa) # Registra a placa

                    if resultado_placa in self.placas_permitidas:
                        self.semaforo.ligar_verde()
                    else:
                        self.semaforo.ligar_vermelho()

                    self.display.set_text(resultado_placa) # Exibe a placa no display
                    
                    # Aguardar o led ser pressionado novamente
                    GPIO.wait_for_edge(self.__pins['button_main'].number, GPIO.RISING)

                    self.display.clean() # Limpa o display

                    self.semaforo.desligar_semaforo() # Desliga o semáforo

                else:
                    self.display.set_text(resultado_placa) # Exibe a placa no display

                    while True:

                        # Faz o semáforo piscar
                        self.semaforo.ligar_verde()
                        time.sleep(0.1)
                        self.semaforo.ligar_vermelho()
                        time.sleep(0.1)

                        if GPIO.input(self.__pins['button_main'].number) == False:
                            self.display.clean()
                            self.semaforo.desligar_semaforo()
                            break

            elif desligar:
                print("\nResetando canais da GPIO...")
                GPIO.cleanup() # Desativa possíveis canais ativos
                print("GPIO Resetada.")
                break

            time.sleep(0.1)


    def get_placas_permitidas(self) -> None:
        file_placas_permitidas = open(os.getenv('PLACAS_PERMITIDAS_FILE'))

        self.placas_permitidas = [x.strip() for x in file_placas_permitidas.readlines()]

        file_placas_permitidas.close()

    def __tirar_foto(self) -> None:
        print("Capturando imagem.")
        subprocess.run(f"libcamera-still -o {self.image_original_path} -t 0.1", shell=True)
        print(f'imagem: {self.image_original_path}')


    def __configuracoes_pins(self) -> None:

        print("Configurando GPIO.")

        # Configura o modo de numeração dos pinos
        GPIO.setmode(GPIO.BCM)

        # Configura o pino como entrada
        GPIO.setup(self.__pins['button_main'].number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #configura o pino como saída
        GPIO.setup(self.__pins['led_button_main'].number, GPIO.OUT)

        print("GPIO configurada.")

