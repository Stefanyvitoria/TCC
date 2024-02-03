import RPi.GPIO as GPIO


class Pin_Button:
    def __init__(self, number: int, ativo: bool = False, pin_type='in') -> None:
        self.number = number
        self.ativo = ativo
        self.pin_type = pin_type

    def ligar(self)-> None:
        print(f"Ligando pin {self.number}")
        self.ativo = True
        if self.pin_type == 'in':
            GPIO.output(self.number, self.ativo)
        else: 
            GPIO.output(self.number, not self.ativo)

    def desligar(self)-> None:
        print(f"Desligando pin {self.number}")
        self.ativo = False
        if self.pin_type == 'in':
            GPIO.output(self.number, self.ativo)
        else: 
            GPIO.output(self.number, not self.ativo)
