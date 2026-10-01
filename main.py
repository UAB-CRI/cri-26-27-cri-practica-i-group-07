def llegir_crossword(nom_fitxer):
    with open(nom_fitxer, "r") as f:
        crossword = []

        for linia in f:
            linia = linia.strip()

            if linia:
                crossword.append(linia.split())

    return crossword


crossword = llegir_crossword("MaterialsPractica/crossword_CB_v3.txt")

print("Crossword:")

for fila in crossword:
    print(fila)