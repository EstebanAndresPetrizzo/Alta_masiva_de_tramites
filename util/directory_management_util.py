"""
@author: Esteban Petrizzo

Available Functions:\n
- DirectoryManagementOK: Manejo de los datos ya grabados para evitar duplicación en el caso de tener que volver a
    empezar por falta de conexión o errores inesperados. \n

"""
import shutil
import os
import logging
import errno


def DirectoryManagementOK(directorio):
    """
    Crea los directorios asociados a los trámites.
    Mueve los archivos una vez que termina el proceso de Alta.
    Elimina el Directorio de origen.
    :param directorio: Directorio a mover una vez terminado el proceso de alta.
    :except: Cualquier error con el movimiento de archivos.
    """
    if not os.path.exists('./grabadosOK'):
        os.mkdir('grabadosOK')
        logging.info("SE CREA DIRECTORIO -- 'grabadosOK' PARA RESULTADOS SATISFACTORIOS")

    if not os.path.exists('./grabadosOK/%s' % directorio):
        os.mkdir('./grabadosOK/%s' % directorio)
        logging.info("SE CREA DIRECTORIO -- '%s'" % directorio)

    try:
        file_source = './Archivos/%s' % directorio
        file_destination = './grabadosOK/%s' % directorio
        get_files = os.listdir(file_source)

        for file in get_files:
            shutil.move(file_source + '/' + file, file_destination)
            logging.info("MOVIENDO ARCHIVO: %s" % file)

        os.rmdir(file_source)
    except OSError as error:
        if error.errno != errno.EEXIST:
            logging.error(error)
            shutil.rmtree(file_source)
        else:
            logging.error(error)
            print(error)
