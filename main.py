"""
Autor: @Stefanyvitoria
Data: 12/2023
Descrição: Script principal da aplicação. 
"""

from src.App import App
import RPi.GPIO as GPIO

try:
    App()
    
except Exception as e:
    print(f'Exception capturada:\n{e}')
    
    print("\nResetando canais da GPIO...")
    GPIO.cleanup() # Desativa possíveis canais ativos
    print("GPIO Resetada.")

