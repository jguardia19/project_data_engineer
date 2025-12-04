import pandas as pd

class DataTransform:
    def __init__(self):
        self.duplicate_columns = [
            "dispositivo", "tipoinfraccion", "imagen",
            "ubicacion", "zonainteres", "fechahora"
        ]
        
    #funcion para eliminar duplicados
    def eliminar_duplicados(self, dataframe):
        clean_data = dataframe.drop_duplicates(
            subset=self.duplicate_columns,
            keep="first"
        ).reset_index(drop=True)

        return clean_data
    
    #funcion para comparar datos nuevos con enviados para obtener solo nuevos eventos
    def comparar_con_enviados(self, nvidia_df, sent_df, debug=False):

        nvidia_clean = self.remover_duplicados(nvidia_df)

        if sent_df is not None and not sent_df.empty:
            
            new_events = nvidia_clean[~nvidia_clean.isin(sent_df).all(axis=1)]

            if debug:
                print(f" Eventos nvidia limpios: {len(nvidia_clean)}")
                print(f" Eventos ya enviados: {len(sent_df)}")
                print(f"Eventos nuevos a enviar: {len(new_events)}")

            return new_events
        else:
            if debug:
                print(f" Eventos a enviar (sin historial): {len(nvidia_clean)}")
            return nvidia_clean
        
    #funcion para transformar datos
    def transformar_datos(self, df_nvidia, df_sent, flags, debug=False):

        if flags['error']:
            return pd.DataFrame()

        if not flags['eventos_enviados_file_exists'] and flags['nvidia_file_exists']:
            # Solo archivo nvidia existe
            if debug:
                print(" Removiendo duplicados de eventos a enviar")
            return self.eliminar_duplicados(df_nvidia)

        elif flags['eventos_enviados_file_exists'] and flags['nvidia_file_exists']:
            # Ambos archivos existen
            if debug:
                print("🔄 Comparando eventos enviados vs nuevos")
            return self.comparar_con_enviados(df_nvidia, df_sent, debug)

        return pd.DataFrame()   
