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


