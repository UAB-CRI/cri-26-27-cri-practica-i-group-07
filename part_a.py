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
