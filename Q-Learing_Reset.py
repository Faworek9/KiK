import os
import config

foldery = [
    config.DATA_DIR_LEGACY,
    config.DATA_DIR_UPGRADED,
    "data",  # stary katalog
    ".",     # katalog główny
]

nazwy_plikow = ["wyniki_X.txt", "wyniki_O.txt", "q_X.json", "q_O.json"]

for folder in foldery:
    for plik in nazwy_plikow:
        sciezka = os.path.join(folder, plik) if folder != "." else plik
        try:
            os.remove(sciezka)
            print(f"Usunięto: {sciezka}")
        except FileNotFoundError:
            pass
        except PermissionError:
            print(f"Brak uprawnień do usunięcia {sciezka}.")