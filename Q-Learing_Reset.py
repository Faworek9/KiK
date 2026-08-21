import os

pliki_do_usuniecia = ["wyniki_X.txt","wyniki_O.txt", "q_X.json", "q_O.json"]

for plik in pliki_do_usuniecia:
    try:
        os.remove(plik)
        print(f"Usunięto: {plik}")
    except FileNotFoundError:
        print(f"Plik {plik} nie istnieje.")
    except PermissionError:
        print(f"Brak uprawnień do usunięcia {plik}.")