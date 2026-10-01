def llegir_crossword(nom_fitxer):
    with open(nom_fitxer, "r") as f:
        crossword = []

        for linia in f:
            linia = linia.strip()

            if linia:
                crossword.append(linia.split())

    return crossword


def llegir_diccionari(nom_fitxer):
    with open(nom_fitxer, "r", encoding="latin-1") as f:
        paraules = []

        for linia in f:
            paraula = linia.strip().upper()

            if paraula:
                paraules.append(paraula)

    return paraules

def trobar_variables(crossword):
    variables = []

    files = len(crossword)
    columnes = len(crossword[0])

    numero_variable = 1

    for fila in range(files):
        for columna in range(columnes):


def main():
    crossword = llegir_crossword("MaterialsPractica/crossword_CB_v3.txt")
    diccionari = llegir_diccionari("MaterialsPractica/diccionari_CB_v3.txt")

    print("Crossword:")
    for fila in crossword:
        print(fila)

    print("\nDiccionari:")
    print(len(diccionari), "paraules")
    print(diccionari)


if __name__ == "__main__":
    main()


