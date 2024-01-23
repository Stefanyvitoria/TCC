import RPi.GPIO as GPIO
import time, subprocess

class Pin_Button:
    def __init__(self, number: int, pressed: bool = False) -> None:
        self.number = number
        self.pressed = pressed

    def ligar(self)-> None:
        GPIO.output(self.number, True)

    def desligar(self)-> None:
        GPIO.output(self.number, True)



class App:
    def __init__(self, detector) -> None:
        self.detector_placa = detector

        self.image_path = '/home/pi/Documents/TCC/midias/imagem-01.png'

        self.pins = {
            'button_main': Pin_Button(26),
            'led_button_main':Pin_Button(16)
        }

        self.configuracoes_pins()
        self.run()


    def run(self) -> None:
        while True:

            self.pins['led_button_main'].desligar() # desliga o led que indica processamento
            
            # Se houver evento e for uma acionada no botão
            if GPIO.event_detected(self.pins['button_main'].number) and (GPIO.input(self.pins['button_main'].number) == 0):
                self.pins['led_button_main'].ligar() # acende o led led de processamento
                self.tirar_foto()

            # self.tirar_foto()
            # break

            time.sleep(0.1)


    def tirar_foto(self) -> None:
        subprocess.run(f"libcamera-still -o {self.image_path} -t 0.1", shell=True)

    def configuracoes_pins(self) -> None:

        # Configura o modo de numeração dos pinos
        GPIO.setmode(GPIO.BCM)

        # Configura o pino como entrada
        GPIO.setup(self.pins['button_main'].number, GPIO.IN, pull_up_down=GPIO.PUD_UP) #PUD_UP PUD_DOWN
        GPIO.add_event_detect(self.pins['button_main'].number, GPIO.RISING)

        #configura o pino como saída
        GPIO.setup(self.pins['led_button_main'].number, GPIO.OUT)