"""
@author: Esteban Petrizzo
Available Functions:\n
- CallServicesRudi: Llamada literal a los servicios de RUDI. \n

"""

import requests
import json
import logging


def CallServicesRudi(data):
    """Llamada literal a los servicios de RUDI.
    :param data: {"fileName":"", Nombre del archivo a guardar con el trámite.
                    "sizeInBase64":"", Size del archivo en Base64.
                    "base64Content":"", Archivo encoder en Base64.
                    "isNewTramite": True, Boolean que indica si hacemos un nuevo trámite o añadimos al último creado.
                    "lastRequest": {último trámite creado.
                            "directorio":"", último directorio (DNI del cliente)
                            "numeroTramite":"", id último trámite
                            "file_id_list": []}} lista de archivos de un trámite

    :except: Error en la conexión -- requests.ConnectionError.
    :except: Error en la invocación del servicio -- requests.HTTPError.

    """

    if data.get("ambiente") == "prod":
        ambiente = ""

    urlNewTramite = "http://sgi{}:80/ws.rudi/api/tramites/".format(data.get("ambiente"))
    urlExistingTramite = "http://sgi{}:80/ws.rudi/api/tramites/{}/{}/archivos" \
        .format(data.get("ambiente"),
                data.get("tramite"),
                data.get("lastRequest")
                .get("numeroTramite"))

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    dataNewTramite = ('{"pk": {"tipoTramite": "%s"}, "origen": "ANDY", "observaciones": "prueba",'
                      '"imagenesArchivo": {"items": [{"fileName": "%s", "sizeInBytes": "%s",'
                      '"base64Content": "%s" }]}}' % (data.get("tramite"),
                                                      data.get("fileName"),
                                                      data.get("sizeInBase64"),
                                                      data.get("base64Content")))

    dataExistingTramite = ('{"fileName":"%s", "sizeInBytes": "%s", "base64Content": "%s"}'
                           % (data.get("fileName"),
                              data.get("sizeInBase64"),
                              data.get("base64Content")))

    try:
        if data.get("isNewTramite"):
            jsonData = json.loads(dataNewTramite)
            response = requests.post(urlNewTramite, json=jsonData, headers=headers)
            response.raise_for_status()
            id_images_tramite = response.json().get('imagenesArchivo').get('items')[0].get('pk').get('id')
            id_numero_tramite = response.json().get('pk').get('nroTramite')

            print("--------\nOK NEW TRAMITE {} -- {} \nADD NEW IMAGES -- {}\n--------"
                  .format(data.get("tramite"),
                          id_numero_tramite,
                          id_images_tramite))
            return id_numero_tramite, [id_images_tramite]

        else:
            jsonData = json.loads(dataExistingTramite)
            response = requests.post(urlExistingTramite, json=jsonData, headers=headers)
            response.raise_for_status()
            file_id_list = data.get("lastRequest").get("file_id_list")
            last_id_images = response.json().get('pk').get('id')
            file_id_list.append(last_id_images)
            print("OK EXISTING IMAGES TRAMITE {} -- {}\n--------"
                  .format(data.get("tramite"),
                          last_id_images))

            return data.get("lastRequest").get("numeroTramite"), file_id_list

    except requests.ConnectionError as error:
        logging.error(error.args[0].reason)
        print(error.args[0].reason)

    except requests.HTTPError as error:
        logging.error(error)
        print(error)
