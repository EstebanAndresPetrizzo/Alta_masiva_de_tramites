# rudi_bulk_new_tramite.py
# -*- coding: utf-8 -*-
"""
@author: Esteban Petrizzo

Programa que a partir de un directorio raíz comenzara, de formar recursiva, a buscar archivos
para dar de alta trámites en RUDI que contengan tales archivos.

Requirements:
- Install Python 3.10.6. \n
- Colocar los archivos en una sub-carpeta dentro de un solo directorio llamado 'Archivos'. \n
- Colocar este archivo (rudi_bulk_new_tramite.py) en el mismo directio donde se encuentra la carpeta 'Archivos'.\n
- Como ejecutar: py rudi_bulk_new_tramite.py {tipo_tramite} {ambiente}.\n
- El parámetro {tipo_tramite}:\n
    Son las iniciales del tipo trámite de RUDI ej: TSTX, REIN, TEST, etc.
    Debe ir en mayúscula.
    Es obligatorio.

- El parámetro {ambiente}:\n
    Es el ambiente donde se desea ejecutar.
    Campos permitidos: dev - qa - pre - prod.
    Es obligatorio.
"""
import logging
import argparse
import util
from util import fetch_recursive_util

logging.basicConfig(filename='bulkFileRudi.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Tipo_Trm --argumento obligatorio
parser = argparse.ArgumentParser()
parser.add_argument("tipo_trm", type=str)
parser.add_argument("ambiente", type=str, choices=["int", "qa", "pre", "prod"],
                    help="Valores permitidos= int, qa, pre, prod")
args = parser.parse_args()

if __name__ == "__main__":
    print("----INICIO DE PROGRAMA----")
    fetch_recursive_util.FetchRecursiveFile("./Archivos")
    print("----FIN DE PROGRAMA----")
