import RPi.GPIO as GPIO
from src.classes.GPIO_PIN import Pin_Button
import os

class Semaforo:
    def __init__(self) -> None:
        self.__pins = {
            'rele_3': Pin_Button(int(os.getenv('PIN_NUMBER_RELE_3')),pin_type='out'),
            'rele_4': Pin_Button(int(os.getenv('PIN_NUMBER_RELE_4')),pin_type='out'),
        }

        self.__configurar_pinos()

    def __configurar_pinos(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pins['rele_3'].number, GPIO.OUT)
        GPIO.setup(self.__pins['rele_4'].number, GPIO.OUT)

        self.desligar_semaforo()

    def desligar_semaforo(self) -> None:
        self.__pins['rele_3'].desligar()
        self.__pins['rele_4'].desligar()

    def ligar_verde(self) -> None:
        self.__pins['rele_3'].ligar()
        self.__pins['rele_4'].ligar()

    def ligar_vermelho(self) -> None:
        self.__pins['rele_3'].ligar()
        self.__pins['rele_4'].desligar()