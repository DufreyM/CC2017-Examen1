"""Pruebas de integridad y comportamiento basico del modelo ABM."""

import unittest

import numpy as np
from scipy import sparse

from src import grupo6_model as model


class ModeloPoblacionalTests(unittest.TestCase):
    def test_carga_las_cinco_zonas_del_excel(self):
        self.assertEqual(model.DEMOGRAFIA.index.tolist(), model.ZONAS)
        self.assertEqual(model.REDES.index.tolist(), model.ZONAS)
        self.assertEqual(model.VULNERABILIDAD.index.tolist(), model.ZONAS)
        self.assertEqual(int(model.POBLACION_ZONA.sum()), 250_000)

    def test_campana_aumenta_la_probabilidad_de_informacion_correcta(self):
        base = model.prob_info_correcta_campana(False)
        campana = model.prob_info_correcta_campana(True)

        self.assertTrue(np.all(campana >= base))
        self.assertTrue(np.all(campana <= 1.0))

    def test_asistencia_respeta_limites_y_prioridad(self):
        for zona in range(model.N_ZONAS):
            asistencia = model.prob_asistencia(0, zona, "necesita_asistencia")
            dependencia = model.prob_asistencia(0, zona, "dependiente")

            self.assertGreaterEqual(dependencia, 0.02)
            self.assertLessEqual(asistencia, 0.9)
            self.assertLessEqual(dependencia, asistencia)

    def test_realizacion_minima_produce_trayectorias_validas(self):
        zona_de_agente = np.arange(model.N_ZONAS)
        adyacencia = sparse.csr_array((model.N_ZONAS, model.N_ZONAS))

        resultado = model.correr_realizacion(
            adyacencia,
            red=None,
            zona_de_agente=zona_de_agente,
            semilla=123,
        )

        evacuados = resultado["evacuados_por_zona_paso"]
        self.assertEqual(evacuados.shape, (model.N_PASOS, model.N_ZONAS))
        self.assertTrue(np.all(np.diff(evacuados, axis=0) >= 0))
        self.assertTrue(np.all(evacuados >= 0))


if __name__ == "__main__":
    unittest.main()
