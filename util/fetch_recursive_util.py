"""
@author: Esteban Petrizzo
Available Functions:\n
- ClearParameters: Function necesaria para setting las variables al estado inicial. \n
- FetchRecursiveFile: Función principal, búsqueda de archivos. \n

"""

import os

from rudi_bulk_new_tramite import args
from util import base_64_util, call_service_rudi_util

# datos que deseo guardar en la BB DD
# nombre de carpeta (documento cliente)
# id número de trámite
# id de archivo -array (imágenes por trámite)
from util.directory_management_util import DirectoryManagementOK
from util.insert_bbdd import InsertBBDD

LAST_TRAMITE = {"directorio": "",
                "numeroTramite": "",
                "file_id_list": []}

ALTA_RUDI = {"fileName": "",
             "sizeInBase64": "",
             "base64Content": "",
             "isNewTramite": True,
             "lastRequest": {},
             "tramite": args.tipo_trm.upper(),  # No cambia en toda la ejecución
             "ambiente": args.ambiente.lower()}  # No cambia en toda la ejecución


def ClearParameters():
    """
    Reset para el nuevo trámite a procesar.

    """
    LAST_TRAMITE.update({"directorio": "",
                         "numeroTramite": "",
                         "file_id_list": []})
    ALTA_RUDI.update({"fileName": "",
                      "sizeInBase64": "",
                      "base64Content": "",
                      "isNewTramite": True,
                      "lastRequest": {}})


def FetchRecursiveFile(path):
    """

    :param path: Ruta raíz desde donde se comenzara a buscar archivos para el alta de los trámites.
    """
    path_local = os.scandir(path)
    is_new_tramite = True

    for element in path_local:
        # Caso base - que sea un file - intentamos el alta
        if element.is_file():
            elementEncodeBase64 = base_64_util.EncodeToBase64(path + "/" + element.name)
            fileSize = base_64_util.CalculateFileSize(elementEncodeBase64)
            ALTA_RUDI.update({"fileName": element.name,
                              "sizeInBase64": fileSize,
                              "base64Content": elementEncodeBase64,
                              "isNewTramite": is_new_tramite,
                              "lastRequest": LAST_TRAMITE})

            response_service = call_service_rudi_util.CallServicesRudi(ALTA_RUDI)
            LAST_TRAMITE.update({"numeroTramite": response_service[0], "file_id_list": response_service[1]})
            is_new_tramite = False  # hasta que se acaben los archivos en la carpeta actual

        # Caso recursivo - que sea un dir - estos nos indica que se trata de un nuevo trámite
        elif element.is_dir():
            LAST_TRAMITE.update({"directorio": element.name})
            FetchRecursiveFile(path + "/" + element.name)
            DirectoryManagementOK(element.name)
            InsertBBDD(LAST_TRAMITE)
            ClearParameters()
            is_new_tramite = True
