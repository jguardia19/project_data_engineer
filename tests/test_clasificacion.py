import unittest
import sys
import os
sys.path.append('../src')

class TestSistemaClasificacion(unittest.TestCase):
    def test_import(self):
        """Prueba que se puede importar el módulo"""
        try:
            import sistema_clasificacion
            self.assertTrue(True)
        except ImportError:
            self.fail("No se pudo importar sistema_clasificacion")

if __name__ == '__main__':
    unittest.main()
