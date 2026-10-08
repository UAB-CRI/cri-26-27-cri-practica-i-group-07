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


def backtracking(variables, dominis, encreuaments, assignacio, comptador):
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
        comptador[0] += 1

        # Comprovem si la paraula compleix els encreuaments
        if compleix_restriccions(
            id_variable, paraula, assignacio, encreuaments
        ):
            # Assignem la paraula a la variable
            assignacio[id_variable] = paraula

            # Intentem resoldre les variables restants
            if backtracking(
                variables, dominis, encreuaments, assignacio, comptador
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


def reduir_dominis(id_variable, paraula, dominis, encreuaments, assignacio):
    """Retorna uns dominis nous on s'han tret les paraules incompatibles
    amb 'paraula' de les variables no assignades que es creuen amb id_variable.
    Retorna None si algun domini queda buit."""
    nous = dict(dominis)  # còpia: així no cal desfer res en tornar enrere

    for e in encreuaments:
        if e["var1"] == id_variable:
            altra, pos_meva, pos_altra = e["var2"], e["pos1"], e["pos2"]
        elif e["var2"] == id_variable:
            altra, pos_meva, pos_altra = e["var1"], e["pos2"], e["pos1"]
        else:
            continue

        if altra in assignacio:
            continue

        # Ens quedem només amb les paraules que tenen la lletra que cal
        nous[altra] = [p for p in nous[altra] if p[pos_altra] == paraula[pos_meva]]

        if not nous[altra]:
            return None  # domini buit: aquesta paraula no pot ser

    return nous

def forward_checking(variables, dominis, encreuaments, assignacio, comptador):
    """Backtracking amb forward checking."""
    if len(assignacio) == len(variables):
        return True

    id_variable = next(v["id"] for v in variables if v["id"] not in assignacio)

    for paraula in dominis[id_variable]:
        comptador[0] += 1

        # No repetir paraules
        if paraula in assignacio.values():
            continue

        nous_dominis = reduir_dominis(id_variable, paraula, dominis,
                                      encreuaments, assignacio)
        if nous_dominis is None:
            continue

        assignacio[id_variable] = paraula

        if forward_checking(variables, nous_dominis, encreuaments,
                            assignacio, comptador):
            return True

        del assignacio[id_variable]

    return False

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
    comptador = [0]
    
    if backtracking(variables, dominis, encreuaments, assignacio, comptador):
        print("Solució trobada:")
        print(assignacio)
    else:
        print("No s'ha trobat cap solució.")

    
    # Resolem el mots encreuats amb backtracking
    assignacio = {}
    comptador = [0]
    if backtracking(variables, dominis, encreuaments, assignacio, comptador):
        print("\nSolució trobada:")
        print(assignacio)

        print("\nTauler resolt:")
        imprimir_solucio(crossword, variables, assignacio)
    else:
        print("No s'ha trobat cap solució.")

        
    # Test de reduir_dominis()
    print("\n--- Test reduir_dominis ---")

    if encreuaments:
        e = encreuaments[0]
        id_variable = e["var1"]
        id_altra = e["var2"]

        # Triem una paraula candidata de la primera variable
        paraula = dominis[id_variable][0]

        assignacio_test = {}

        nous_dominis = reduir_dominis(
            id_variable,
            paraula,
            dominis,
            encreuaments,
            assignacio_test
        )

        print("Variable provada:", id_variable)
        print("Paraula provada:", paraula)
        print("Domini original de la variable veïna:",
              dominis[id_altra])
        
        if nous_dominis is None:
            print("Resultat: algun domini ha quedat buit.")
        else:
            print("Domini reduït de la variable veïna:",
                  nous_dominis[id_altra])

            pos_meva = e["pos1"]
            pos_altra = e["pos2"]

            print("Lletra exigida:", paraula[pos_meva])
            print(
                "Totes les paraules són compatibles:",
                all(
                    p[pos_altra] == paraula[pos_meva]
                    for p in nous_dominis[id_altra]
                )
            )
    else:
        print("No hi ha encreuaments per provar.")

    assignacio_fc = {}
    comptador = [0]

    resultat_fc = forward_checking(
        variables,
        dominis,
        encreuaments,
        assignacio_fc,
        comptador
    )

    if resultat_fc:
        print("Solució trobada:")
        print(assignacio_fc)
    else:
        print("No s'ha trobat cap solució.")

    print("Nombre de paraules provades:", comptador[0])

    
    # Comparació dels dos algorismes
    print("\n--- Comparació d'algorismes ---")

    # 1. Backtracking normal
    assignacio_bt = {}
    comptador_bt = [0]

    resultat_bt = backtracking(
        variables,
        dominis,
        encreuaments,
        assignacio_bt,
        comptador_bt
    )

    print("\nBacktracking normal:")
    print("Solució trobada:", resultat_bt)
    print("Paraules candidates provades:", comptador_bt[0])

    # 2. Forward Checking
    assignacio_fc = {}
    comptador_fc = [0]

    resultat_fc = forward_checking(
        variables,
        dominis,
        encreuaments,
        assignacio_fc,
        comptador_fc
    )

    print("\nForward Checking:")
    print("Solució trobada:", resultat_fc)
    print("Paraules candidates provades:", comptador_fc[0])

    # 3. Comparació
    if resultat_bt and resultat_fc:
        diferencia = comptador_bt[0] - comptador_fc[0]

        print("\nDiferència de candidates provades:", diferencia)

        if comptador_bt[0] > 0:
            millora = diferencia / comptador_bt[0] * 100
            print(f"Reducció de candidates: {millora:.2f}%")



if __name__ == "__main__":
    main()


