import pandas as pd


class DataTransformer:

    def __init__(self):
        self.duplicate_columns = [
            "dispositivo", "tipoinfraccion", "imagen",
            "ubicacion", "zonainteres", "fechahora"
        ]

    # funcion que elimina duplicados
    def remove_duplicates(self, dataframe):
        # Elimina registros duplicados

        clean_data = dataframe.drop_duplicates(
            subset=self.duplicate_columns,
            keep="first"
        ).reset_index(drop=True)

        return clean_data

    # funcion que compara datos nuevos con enviados para obtener solo nuevos eventos
    def compare_with_sent_data(self, nvidia_df, sent_df, debug=False):

        # Compara datos nuevos con enviados para obtener solo nuevos eventos

        # Primero eliminar duplicados en nvidia
        nvidia_clean = self.remove_duplicates(nvidia_df)

        if sent_df is not None and not sent_df.empty:
            # Comparar con enviados para obtener solo nuevos
            new_events = nvidia_clean[~nvidia_clean.isin(sent_df).all(axis=1)]

            if debug:
                print(f" Eventos nvidia limpios: {len(nvidia_clean)}")
                print(f" Eventos ya enviados: {len(sent_df)}")
                print(f"Eventos nuevos a enviar: {len(new_events)}")

            return new_events
        else:
            if debug:
                print(
                    f"📊 Eventos a enviar (sin historial): {len(nvidia_clean)}")
            return nvidia_clean

    # funcion que transforma datos para ser enviados al modelo de carga o load
    def transform_data(self, df_nvidia, df_sent, flags, debug=False):

        # Transforma datos según las condiciones de archivos

        if flags['error']:
            return pd.DataFrame()

        if not flags['sent_file_exists'] and flags['nvidia_file_exists']:
            # Solo archivo nvidia existe
            if debug:
                print(" Removiendo duplicados de eventos a enviar")
            return self.remove_duplicates(df_nvidia)

        elif flags['sent_file_exists'] and flags['nvidia_file_exists']:
            # Ambos archivos existen
            if debug:
                print("🔄 Comparando eventos enviados vs nuevos")
            return self.compare_with_sent_data(df_nvidia, df_sent, debug)

        return pd.DataFrame()
