#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

import sys
import os
import pprint
import json
import re
import pickle
from collections import deque
import utils_algoritmica

def syntax():
    print("argumentos <trieGenerado.txt> <palabra> <distancia max>")
    exit(1)

def palabrasCercanas(trie, palabra, distancia):
    pila = deque([(0, 0, 0)])
    cercanos = set()
    while len(pila) > 0:
        nodo_ppal = pila.popleft()
        analizado, nodo, coste = nodo_ppal
        if coste > distancia:
            continue

        # Coincidencia encontrada
        if(trie[nodo][1] != None and coste <= distancia and (len(palabra) == analizado)):
            cercanos.add(trie[nodo][1])

        if analizado < len(palabra) - 1:  # Swap posible
            letra_actual, letra_siguiente = palabra[analizado], palabra[analizado+1]
            if letra_siguiente in trie[nodo][2]:
                nodo_hijo = trie[nodo][2][letra_siguiente]
                if letra_actual in trie[nodo_hijo][2]:
                    nieto = trie[nodo_hijo][2][letra_actual]
                    pila.appendleft((analizado + 2, nieto, coste + 1))  # Swap

        if analizado < len(palabra):  # Hay al menos 1 carácter borrable
            pila.appendleft((analizado + 1, nodo, coste + 1))  # Borrado

        for letra_hijo in trie[nodo][2]:
            nodo_hijo = trie[nodo][2].get(letra_hijo)

            if coste < distancia:
                pila.appendleft((analizado, nodo_hijo, coste + 1))  # Insercion

            if analizado < len(palabra):  # Si hay al menos 1 carácter sustituible
                pila.appendleft((analizado+1, nodo_hijo, coste +
                                 (letra_hijo != palabra[analizado])))  # Sustitucion

    return cercanos


if __name__ == "__main__":

    if len(sys.argv) != 4:
        syntax()
    print(sys.argv)
    fichero = sys.argv[1]
    palabra = sys.argv[2]
    distancia = int(sys.argv[3])

    trie = {}
    with open(fichero, 'rb') as handle:
        trie = pickle.load(handle)

    cercanos = palabrasCercanas(trie, palabra, distancia)
    print(len(cercanos), cercanos)
