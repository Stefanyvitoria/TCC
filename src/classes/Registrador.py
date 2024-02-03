from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

class Registrador:
    def __init__(self) -> None:
        self.filename  = ""

        self.check_file()

    def check_file(self):
        data_atual = date.today()
        self.filename = f"{os.getenv('REGISTROS_PATH')}/Registro-Placas-{data_atual}.xlsx"

        if Path(self.filename).exists():
            print(f"O arquivo {self.filename} já existe.")
        else:
            Path(self.filename).touch()
            print(f"Arquivo {self.filename} criado com sucesso!")


if __name__ == "__main__":
    registrador = Registrador()