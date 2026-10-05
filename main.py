def es_lliure(crossword, fila, columna):
    """Retorna True si la casella és dins del tauler i no és un '#'."""
    return (0 <= fila < len(crossword)
            and 0 <= columna < len(crossword[0])
            and crossword[fila][columna] != "#")


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
            if not es_lliure(crossword, fila, columna):
                continue

            # Paraula horitzontal: la casella de l'esquerra és # o fora del tauler
            if not es_lliure(crossword, fila, columna - 1):
                longitud = 0
                while es_lliure(crossword, fila, columna + longitud):
                    longitud += 1

                if longitud >= 2:
                    variables.append({
                        "id": numero_variable,
                        "fila": fila,
                        "columna": columna,
                        "direccio": "H",
                        "longitud": longitud,
                        "caselles": [(fila, columna + k) for k in range(longitud)],
                    })
                    numero_variable += 1

            # Paraula vertical: la casella de dalt és # o fora del tauler
            if not es_lliure(crossword, fila - 1, columna):
                longitud = 0
                while es_lliure(crossword, fila + longitud, columna):
                    longitud += 1

                if longitud >= 2:
                    variables.append({
                        "id": numero_variable,
                        "fila": fila,
                        "columna": columna,
                        "direccio": "V",
                        "longitud": longitud,
                        "caselles": [(fila + k, columna) for k in range(longitud)],
                    })
                    numero_variable += 1

    return variables


def main():
    crossword = llegir_crossword("MaterialsPractica/crossword_CB_v3.txt")
    diccionari = llegir_diccionari("MaterialsPractica/diccionari_CB_v3.txt")

    print("Crossword:")
    for fila in crossword:
        print(fila)

    print("\nDiccionari:")
    print(len(diccionari), "paraules")
    print(diccionari)

    variables = trobar_variables(crossword)
    print("\nVariables trobades:", len(variables))
    for v in variables:
        print(v["id"], v["direccio"], (v["fila"], v["columna"]), "longitud", v["longitud"])


if __name__ == "__main__":
    main()


