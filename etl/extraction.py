import pandas as pd
import os


class DataExtractor:

    def __init__(self, script_dir=None):
        self.script_dir = script_dir or os.path.dirname(
            os.path.abspath(__file__))
        self.csvalertpath = os.path.join(
            self.script_dir, "eventosdetectadosnvidia.csv")
        self.csvsentpath = os.path.join(
            self.script_dir, "eventosdetectadosnvidia_inHiveQL.csv")

    # funcion que valida que exista archivo CSV
    def validate_csv_file(self, file_path):

        # Validar que exista un archivo
        if not os.path.exists(file_path):
            return False

        return os.path.exists(file_path)

    # funcion que lee archivo CSV
    def read_csv_file(self, file_path):
        # Leer archivo CSV
        return pd.read_csv(file_path)

    # funcion que extrae datos de archivos CSV
    def extract_data(self, debug=False):
        # Extrae datos de archivos CSV
        df_nvidia = None
        df_sent = None
        flags = {
            'nvidia_file_exists': False,
            'sent_file_exists': False,
            'error': False
        }

        # Validar archivo de eventos enviados
        if self.validate_csv_file(self.csvsentpath):
            try:
                df_sent = self.read_csv_file(self.csvsentpath)
                flags['sent_file_exists'] = True
                if debug:
                    print("Archivo de eventos enviados validado")
            except Exception as e:
                print(f" Error leyendo archivo enviados: {e}")
        else:
            if debug:
                print("No se encontró archivo de elementos enviados")

        # Validar archivo de eventos nuevos
        if self.validate_csv_file(self.csvalertpath):
            try:
                df_nvidia = self.read_csv_file(self.csvalertpath)
                flags['nvidia_file_exists'] = True
                if debug:
                    print("Archivo de eventos a enviar validado")
            except Exception as e:
                print(f" Error leyendo archivo nvidia: {e}")
        else:
            if debug:
                print("No se encontró archivo de elementos a enviar")

        # Validar que hay datos para procesar
        if not flags['nvidia_file_exists'] and not flags['sent_file_exists']:
            print("No hay información para ser procesada")
            flags['error'] = True

        return df_nvidia, df_sent, flags

    # funcion que elimina archivo de eventos enviados
    def delete_sent_file(self):
        """Elimina archivo de eventos enviados"""
        if os.path.exists(self.csvsentpath):
            os.remove(self.csvsentpath)
            print(f" Archivo {self.csvsentpath} eliminado")
            return True
        return False
