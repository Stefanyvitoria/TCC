from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os, arrow

load_dotenv()

class Registrador:
    def __init__(self) -> None:
        self.filename  = ""

        self.delete_old_files()
        self.check_file()

    def check_file(self) -> None:
        data_atual = date.today()
        self.filename = f"{os.getenv('REGISTROS_PATH')}/Registro-Placas-{data_atual}.xlsx"

        if Path(self.filename).exists():
            print(f"O arquivo {self.filename} já existe.")
        else:
            Path(self.filename).touch()
            print(f"Arquivo {self.filename} criado com sucesso!")


    def delete_old_files(self) -> None:
        tempo_maximo = arrow.now().shift(days=-int(os.getenv('DIAS_MAX_PERMANENCIA')))

        for item in Path(os.getenv('REGISTROS_PATH')).glob('*'):
            if item.is_file() and arrow.get(item.stat().st_mtime) < tempo_maximo:
                item.unlink()


if __name__ == "__main__":
    registrador = Registrador()