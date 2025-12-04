import pandas as pd
import os

class DataExtract:
    def __init__(self, script_dir=None):
        self.script_dir = script_dir or os.path.dirname(
            os.path.abspath(__file__))
        self.csvalertpath = os.path.join(
            self.script_dir, "eventosdetectadosnvidia.csv")
        self.csvsentpath = os.path.join(
            self.script_dir, "eventosdetectadosnvidia_inHiveQL.csv")
        
    #funcion para validar que un archivo exista
    def validate_csv_file(self, file_path):
        if not os.path.exists(file_path):
            return False
        
        return os.path.exists(file_path)
    

    #funcion para leer archivo CSV
    def read_csv_file(self, file_path):
        return pd.read_csv(file_path)
    
    #funcion para extraer datos de los archivos CSV
    def extract_data(self, debug=False):
        df_nvidia = None
        df_eventos_enviados = None
        flags = {
            'nvidia_file_exists': False,
            'eventos_enviados_file_exists': False,
            'error': False
        }

        # Validar archivo de eventos enviados
        if self.validate_csv_file(self.csvalertpath):
            try:
                df_eventos_enviados = self.read_csv_file(self.csvsentpath)
                flags['eventos_enviados_file_exists'] = True
                if debug:
                    print("Archivo de eventos enviados validado")
            except Exception as e:
                print(f" Error leyendo archivo enviado: {e}")
        else:
            if debug:
                print("No se encontró archivo de eventos enviados")

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
                print("No se encontró archivo de eventos a enviar")

        # Validar que hay datos para procesar
        if not flags['nvidia_file_exists'] and not flags['eventos_enviados_file_exists']:
            print("No hay información para ser procesada")
            flags['error'] = True

        return df_nvidia, df_eventos_enviados, flags

    #funcion que elimina archivo de eventos enviados
    def delete_sent_file(self):
        if os.path.exists(self.csvsentpath):
            os.remove(self.csvsentpath)
            print(f" Archivo {self.csvsentpath} eliminado")
            return True
        return False    
