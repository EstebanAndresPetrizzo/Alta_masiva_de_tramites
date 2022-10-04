"""
@author: Esteban Petrizzo

Available Functions:\n
- InsertBBDD: Se graba en la BBDD los datos relacionados con el trámite y cliente. \n
"""

import logging


def InsertBBDD(data):  # data is LAST_TRAMITE
    ##temporal hasta que tenga el sp
    logging.info(data)
    if data.get("numeroTramite") != "":
        print("INICIO -- GRABO EN LA BASE DE DATOS")
        file_id_list = data.get("file_id_list")
        print("Directorio: " + data.get("directorio"))
        print("Id Trámite: " + str(data.get("numeroTramite")))
        for id_file in file_id_list:
            print("Id archivo trámite: " + str(id_file))
        print("FIN -- GRABO EN LA BASE DE DATOS")
