"""
Exercici 3 (PART A): mots encreuats amb diccionari gran.
Forward checking + MRV + índex (longitud, posició, lletra) + paraules úniques.

Reutilitza les funcions de main.py (lectura del tauler, variables,
encreuaments i impressió de la solució).
"""
import random
import sys
import time
from collections import defaultdict

from main import (llegir_crossword, trobar_variables,
                  trobar_encreuaments, imprimir_solucio)

BUIT = frozenset()


# ----------------------------------------------------------------------
# Diccionaris
# ----------------------------------------------------------------------
def llegir_diccionari(nom_fitxer):
    """Llegeix el diccionari, passa a majúscules i elimina duplicats."""
    paraules = set()
    with open(nom_fitxer, "r", encoding="latin-1") as f:
        for linia in f:
            p = linia.strip().upper()
            if p and p.isalpha():
                paraules.add(p)
    return paraules


def crear_diccionari_reduit(origen, desti, n=100000, llavor=42, curtes=5):
    """Crea un diccionari petit (~n paraules) a partir del gran.
    Es conserven TOTES les paraules de longitud <= curtes (n'hi ha poques
    i el tauler en necessita), i la resta es mostregen aleatoriament."""

    paraules = sorted(llegir_diccionari(origen))
    curtes_l = [p for p in paraules if len(p) <= curtes]
    llargues = [p for p in paraules if len(p) > curtes]
    random.seed(llavor)
    k = max(0, min(n - len(curtes_l), len(llargues)))
    mostra = curtes_l + random.sample(llargues, k)
    with open(desti, "w", encoding="latin-1") as f:
        f.write("\n".join(mostra) + "\n")
    return len(mostra)


def agrupar_per_longitud(paraules):
    grups = defaultdict(set)
    for p in paraules:
        grups[len(p)].add(p)
    return grups

class Index:
    """Índex : (longitud, posició) -> {lletra: conjunt de paraules}.
    Només es construeix per a les longituds/posicions que es necessiten."""

    def __init__(self, per_longitud):
        self.per_longitud = per_longitud
        self.cache = {}

    def lletres(self, longitud, pos):
        clau = (longitud, pos)
        if clau not in self.cache:
            d = defaultdict(set)
            for p in self.per_longitud.get(longitud, ()):
                d[p[pos]].add(p)
            self.cache[clau] = d
        return self.cache[clau]

# ----------------------------------------------------------------------
# Preparació del problema
# ----------------------------------------------------------------------
def preparar_veins(encreuaments):
    """veins[id] = llista de (id_altra, pos_en_meva, pos_en_altra)."""
    veins = defaultdict(list)
    for e in encreuaments:
        veins[e["var1"]].append((e["var2"], e["pos1"], e["pos2"]))
        veins[e["var2"]].append((e["var1"], e["pos2"], e["pos1"]))
    return veins


def obtenir_candidates(id_variable, variables, per_longitud,
                       assignacio, veins, index):
    """Obté les paraules compatibles amb les lletres ja assignades."""
    variable = next(v for v in variables if v["id"] == id_variable)
    longitud = variable["longitud"]

    candidats = set(per_longitud.get(longitud, set()))

    for altra, pos_meva, pos_altra in veins[id_variable]:
        if altra in assignacio:
            lletra = assignacio[altra][pos_altra]
            compatibles = index.lletres(longitud, pos_meva).get(
                lletra, set()
            )
            candidats.intersection_update(compatibles)

    # No permetre repetir paraules
    candidats.difference_update(assignacio.values())

    return candidats

def seleccionar_mrv(variables, per_longitud, assignacio, veins, index):
    """Selecciona la variable no assignada amb menys candidates."""
    millor_variable = None
    millors_candidates = None

    for variable in variables:
        id_variable = variable["id"]

        if id_variable in assignacio:
            continue

        candidats = obtenir_candidates(
            id_variable, variables, per_longitud,
            assignacio, veins, index
        )

        if millors_candidates is None or len(candidats) < len(millors_candidates):
            millor_variable = id_variable
            millors_candidates = candidats

        if len(millors_candidates) == 0:
            break

    return millor_variable, millors_candidates

def forward_checking_mrv(variables, per_longitud, assignacio,
                         veins, index, comptador):
    """Resol el crossword amb Forward Checking i selecció MRV."""
    if len(assignacio) == len(variables):
        return True

    id_variable, candidats = seleccionar_mrv(
        variables, per_longitud, assignacio, veins, index
    )

    # Si no hi ha candidats, aquesta branca no té solució
    if not candidats:
        return False

    for paraula in sorted(candidats):
        comptador[0] += 1
        assignacio[id_variable] = paraula

        # Forward Checking: comprovar que cap variable
        # pendent es quedi sense candidats
        viable = True

        for variable in variables:
            altra = variable["id"]

            if altra not in assignacio:
                possibles = obtenir_candidates(
                    altra, variables, per_longitud,
                    assignacio, veins, index
                )
                if not possibles:
                    viable = False
                    break

        if viable and forward_checking_mrv(
            variables, per_longitud, assignacio,
            veins, index, comptador
        ):
            return True

        del assignacio[id_variable]

    return False



if __name__ == "__main__":
    tauler = llegir_crossword("MaterialsPractica/crossword_A.txt")
    variables = trobar_variables(tauler)
    encreuaments = trobar_encreuaments(variables)
    veins = preparar_veins(encreuaments)

    print("Llegint diccionari...")
    paraules = llegir_diccionari(
        "MaterialsPractica/diccionari_A.txt"
    )
    print("Paraules úniques:", len(paraules))

    per_longitud = agrupar_per_longitud(paraules)
    index = Index(per_longitud)

    assignacio = {}
    comptador = [0]

    inici = time.perf_counter()

    resultat = forward_checking_mrv(
        variables, per_longitud, assignacio,
        veins, index, comptador
    )

    temps = time.perf_counter() - inici

    print("\nSolució trobada:", resultat)
    print("Paraules candidates provades:", comptador[0])
    print(f"Temps d'execució: {temps:.2f} segons")

    if resultat:
        imprimir_solucio(tauler, variables, assignacio)

