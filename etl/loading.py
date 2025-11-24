import pandas as pd
import math
from pyhive import hive


class DataLoader:

    def __init__(self, host='localhost', port=10000, user='jose_dev',
                 database='yolo_project', table='yolo_objects'):
        self.host = host
        self.port = port
        self.user = user
        self.database = database
        self.table = table
        self.conn = None
        self.cursor = None

    def esc(self, s: str) -> str:
        """Escapa comillas simples y normaliza backslashes"""
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).replace("\\", "/")
        return s.replace("'", "''")

    def str_literal(self, x) -> str:
        """Devuelve 'texto' o NULL"""
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return "NULL"
        return f"'{self.esc(x)}'"

    def connect_to_hive(self):
        """Establece conexión a HiveQL"""
        try:
            self.conn = hive.Connection(
                host=self.host,
                port=self.port,
                username=self.user,
                database=self.database,
                auth='NONE'
            )
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f" Error conectando a Hive: {e}")
            return False

    def close_connection(self):
        """Cierra conexión a HiveQL"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_batch_to_hive(self, clean_data, batch_size=40, debug=False):
        """
        Inserta datos en HiveQL usando lotes

        Args:
            clean_data: DataFrame con datos limpios
            batch_size: Tamaño del lote
            debug: Activar modo debug

        Returns:
            bool: True si exitoso
        """
        # Validar datos
        if clean_data.empty:
            print("No hay datos para insertar")
            return True

        cols = "(dispositivo, tipoinfraccion, imagen, ubicacion, zonainteres, fechahora)"
        n = len(clean_data)
        total_batches = math.ceil(n / batch_size)

        print(f"📤 Enviando {n} registros en {total_batches} lotes...")

        try:
            for i, start in enumerate(range(0, n, batch_size), start=1):
                chunk = clean_data.iloc[start:start+batch_size]
                print(
                    f" Enviando lote {i}/{total_batches} ({len(chunk)} registros)")

                values = []
                for _, row in chunk.iterrows():
                    dispositivo = self.str_literal(row.get('dispositivo'))
                    tipoinfraccion = self.str_literal(
                        row.get('tipoinfraccion'))
                    imagen = self.str_literal(row.get('imagen'))
                    ubicacion = self.str_literal(row.get('ubicacion'))
                    zonainteres = self.str_literal(row.get('zonainteres'))
                    fechahora = self.str_literal(row.get('fechahora'))

                    tuple_sql = f"({dispositivo},{tipoinfraccion},{imagen},{ubicacion},{zonainteres},{fechahora})"
                    values.append(tuple_sql)

                query = f"INSERT INTO {self.table} {cols} VALUES {', '.join(values)}"

                if debug:
                    print(f"🔍 Query: {query[:100]}...")

                self.cursor.execute(query)

            # Commit cambios
            self.conn.commit()
            print("✅ Datos insertados exitosamente")
            return True

        except Exception as e:
            print(f"❌ Error insertando datos: {e}")
            return False

    def load_data(self, clean_data, debug=False):
        """
        Carga datos completa con manejo de conexión

        Args:
            clean_data: DataFrame con datos limpios
            debug: Activar modo debug

        Returns:
            bool: True si exitoso
        """
        if not self.connect_to_hive():
            return False

        try:
            result = self.insert_batch_to_hive(clean_data, debug=debug)
            return result
        finally:
            self.close_connection()
