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
def obtenir_dominis(variables, diccionari):
    """Filtra les paraules del diccionari segons la longitud de cada variable."""
    dominis = {}
    for v in variables:
        longitud = v["longitud"]
        dominis[v["id"]] = [p for p in diccionari if len(p) == longitud]
    return dominis


def trobar_encreuaments(variables):
    """Trobem quines variables es creuen i quines posicions comparteixen."""
    encreuaments = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            v1 = variables[i]
            v2 = variables[j]

            for pos1, casella1 in enumerate(v1["caselles"]):
                for pos2, casella2 in enumerate(v2["caselles"]):
                    if casella1 == casella2:
                        encreuaments.append({
                            "var1": v1["id"],
                            "pos1": pos1,
                            "var2": v2["id"],
                            "pos2": pos2
                        })
    return encreuaments


def compleix_restriccions(id_variable, paraula, assignacio, encreuaments):
    """Comprova si una paraula compleix els encreuaments amb les variables assignades."""

    for encreuament in encreuaments:
        var1 = encreuament["var1"]
        var2 = encreuament["var2"]
        pos1 = encreuament["pos1"]
        pos2 = encreuament["pos2"]

        # Si la variable actual és var1 i var2 ja està assignada
        if id_variable == var1 and var2 in assignacio:
            if paraula[pos1] != assignacio[var2][pos2]:
                return False

        # Si la variable actual és var2 i var1 ja està assignada
        elif id_variable == var2 and var1 in assignacio:
            if paraula[pos2] != assignacio[var1][pos1]:
                return False

    return True


def backtracking(variables, dominis, encreuaments, assignacio):
    """Resol el mots encreuats mitjançant backtracking."""

    # Cas base: totes les variables tenen una paraula assignada
    if len(assignacio) == len(variables):
        return True

    # Seleccionem la primera variable que encara no està assignada
    variable = None

    for v in variables:
        if v["id"] not in assignacio:
            variable = v
            break

    # Provem totes les paraules del domini de la variable
    id_variable = variable["id"]

    for paraula in dominis[id_variable]:

        # Comprovem si la paraula compleix els encreuaments
        if compleix_restriccions(
            id_variable, paraula, assignacio, encreuaments
        ):
            # Assignem la paraula a la variable
            assignacio[id_variable] = paraula

            # Intentem resoldre les variables restants
            if backtracking(
                variables, dominis, encreuaments, assignacio
            ):
                return True

            # Si no trobem solució, desfem l'assignació
            del assignacio[id_variable]

    # Cap paraula del domini ha permès trobar una solució
    return False

    
def imprimir_solucio(tauler, variables, assignacio):
    """Imprimeix el tauler amb les paraules de la solució."""

    # Fem una còpia del tauler per no modificar l'original
    tauler_resolt = [fila.copy() for fila in tauler]

    for variable in variables:
        id_variable = variable["id"]
        paraula = assignacio[id_variable]

        for i, (fila, columna) in enumerate(variable["caselles"]):
            tauler_resolt[fila][columna] = paraula[i]

    # Mostrem el tauler resolt
    for fila in tauler_resolt:
        print(" ".join(str(casella) for casella in fila))






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

    dominis = obtenir_dominis(variables, diccionari)
    encreuaments = trobar_encreuaments(variables)
    print("\nEncreuaments trobats:", len(encreuaments))
            
    # Test de la funció compleix_restriccions
    print("\n--- Test compleix_restriccions ---")

    if encreuaments:
        encreuament = encreuaments[0]
        id_variable = encreuament["var1"]

        # Agafem una paraula del domini de la variable
        paraula = dominis[id_variable][0]

        # Sense cap altra variable assignada, ha de ser compatible
        assignacio = {}

        resultat = compleix_restriccions(
            id_variable, paraula, assignacio, encreuaments
        )

        print("Variable:", id_variable)
        print("Paraula provada:", paraula)
        print("Resultat sense conflictes:", resultat)

        # Ara assignem una paraula a l'altra variable de l'encreuament
        id_altra = encreuament["var2"]
        pos1 = encreuament["pos1"]
        pos2 = encreuament["pos2"]

        assignacio = {id_altra: dominis[id_altra][0]}

        resultat = compleix_restriccions(
            id_variable, paraula, assignacio, encreuaments
        )

        print("Paraula de l'altra variable:", assignacio[id_altra])
        print("Resultat amb l'encreuament:", resultat)
        print("Lletra de la primera paraula:", paraula[pos1])
        print("Lletra de l'altra paraula:", assignacio[id_altra][pos2])
        
    else:
        print("No s'han trobat encreuaments per provar.")

        # Busquem una paraula incompatible al domini de l'altra variable
    paraula_incompatible = None

    for candidata in dominis[id_altra]:
        if candidata[pos2] != paraula[pos1]:
            paraula_incompatible = candidata
            break

    if paraula_incompatible is not None:
        assignacio = {id_altra: paraula_incompatible}

        resultat = compleix_restriccions(
            id_variable, paraula, assignacio, encreuaments
        )

        print("\n--- Test de conflicte ---")
        print("Paraula actual:", paraula)
        print("Paraula incompatible:", paraula_incompatible)
        print("Resultat esperat: False")
        print("Resultat obtingut:", resultat)
    else:
        print("No s'ha trobat cap paraula incompatible al domini.")
    

    assignacio = {}

    if backtracking(variables, dominis, encreuaments, assignacio):
        print("Solució trobada:")
        print(assignacio)
    else:
        print("No s'ha trobat cap solució.")

    
    # Resolem el mots encreuats amb backtracking
    assignacio = {}

    if backtracking(variables, dominis, encreuaments, assignacio):
        print("\nSolució trobada:")
        print(assignacio)

        print("\nTauler resolt:")
        imprimir_solucio(crossword, variables, assignacio)
    else:
        print("No s'ha trobat cap solució.")


if __name__ == "__main__":
    main()


