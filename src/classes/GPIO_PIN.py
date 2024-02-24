import RPi.GPIO as GPIO


class Pin_Button:
    def __init__(self, number: int, ativo: bool = False, pin_type='in') -> None:
        self.number = number
        self.ativo = ativo
        self.pin_type = pin_type

    def ligar(self)-> None:
        self.ativo = True
        if self.pin_type == 'in':
            GPIO.output(self.number, self.ativo)
        else: 
            GPIO.output(self.number, not self.ativo)



    def desligar(self)-> None:
        self.ativo = False
        if self.pin_type == 'in':
            GPIO.output(self.number, self.ativo)
        else: 
            GPIO.output(self.number, not self.ativo)
