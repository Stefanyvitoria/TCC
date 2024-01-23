import RPi.GPIO as GPIO


class Pin_Button:
    def __init__(self, number: int, ativo: bool = False) -> None:
        self.number = number
        self.ativo = ativo

    def ligar(self)-> None:
        print(f"Ligando pin {self.number}")
        self.ativo = True
        GPIO.output(self.number, self.ativo)

    def desligar(self)-> None:
        print(f"Desligando pin {self.number}")
        self.ativo = False
        GPIO.output(self.number, self.ativo)
