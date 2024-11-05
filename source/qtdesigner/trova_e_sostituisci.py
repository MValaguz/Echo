import sys

def trova_e_sostituisci(nome_file, cerca, sostituisci):
    try:
        with open(nome_file, 'r') as file:
            contenuto = file.read()

        contenuto_modificato = contenuto.replace(cerca, sostituisci)

        with open(nome_file, 'w') as file:
            file.write(contenuto_modificato)

        print(f"Sostituzione completata con successo nel file {nome_file}.")

    except FileNotFoundError:
        print(f"Il file {nome_file} non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Uso: python script.py <nome_file> <stringa_da_trovare> <stringa_di_sostituzione>")
    else:
        trova_e_sostituisci(sys.argv[1], sys.argv[2], sys.argv[3])
