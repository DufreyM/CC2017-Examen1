"""
Modelo ABM de Grupo 6 (Comportamiento de la Poblacion y Toma de Decisiones),
CC2017 - Examen Practico, terremoto Ciudad UVG.

Todos los parametros se cargan directamente desde el archivo Excel oficial
del catedratico: data/Grupo6_ComportamientoPoblacional.xlsx (hoja
"Datos_Grupo6"). La UNICA cifra que ese archivo no entrega es la poblacion
absoluta por zona (solo da porcentajes demograficos, de vulnerabilidad y de
red social) -- se documenta como supuesto explicito mas abajo
(POBLACION_ZONA), tal como permite el enunciado del examen ("si el grupo
considera que algun dato es inconsistente o incompleto, puede hacer
supuestos adicionales siempre que los documente explicitamente").
"""

from pathlib import Path

import numpy as np
import networkx as nx
import pandas as pd

RUTA_EXCEL = Path(__file__).parent / "data" / "Grupo6_ComportamientoPoblacional.xlsx"

ZONAS = ["Z1", "Z2", "Z3", "Z4", "Z5"]
N_ZONAS = len(ZONAS)
NOMBRES_ZONA = {
    "Z1": "Centro historico", "Z2": "Norte residencial", "Z3": "Sur industrial",
    "Z4": "Este comercial", "Z5": "Oeste periferico",
}

# SUPUESTO DOCUMENTADO: el Excel de Grupo 6 no incluye poblacion absoluta por
# zona (solo porcentajes). El enunciado general solo da el total de la
# ciudad (250,000 hab. en 5 zonas), sin el desglose. Ante la falta de una
# base para diferenciar, se asume reparto igualitario; se debe revisar si en
# el intercambio presencial otro grupo (p. ej. Grupo 1) aporta el desglose
# real, y en ese caso sustituir este arreglo.
POBLACION_ZONA = np.array([50_000, 50_000, 50_000, 50_000, 50_000])
assert POBLACION_ZONA.sum() == 250_000

N_REP_POR_ZONA = 2000  # agentes representativos (super-agentes) por zona
FACTOR_ESCALA = POBLACION_ZONA / N_REP_POR_ZONA

N_PASOS = 12          # 12 bloques de 6h = 72h de horizonte de simulacion
N_REALIZACIONES = 30  # minimo exigido por el enunciado del examen


# 1. Carga de datos desde el Excel oficial
def cargar_datos_excel(ruta=RUTA_EXCEL):
    """Lee las 4 tablas de la hoja Datos_Grupo6 por posicion de fila fija
    (estructura del archivo entregado por el catedratico)."""
    ws = pd.read_excel(ruta, sheet_name="Datos_Grupo6", header=None)

    demografia = ws.iloc[6:11, 0:6].copy()
    demografia.columns = ["zona", "pct_menor15", "pct_adulto", "pct_mayor60",
                           "pct_discapacidad", "pct_smartphone"]
    demografia["zona"] = ZONAS
    demografia = demografia.set_index("zona").astype(float, errors="ignore")
    demografia[demografia.columns] = demografia[demografia.columns].astype(float)

    comportamiento = ws.iloc[14:22, 0:2].copy()
    comportamiento.columns = ["parametro", "valor"]
    comportamiento = comportamiento.set_index("parametro")["valor"].astype(float)

    redes = ws.iloc[25:30, 0:5].copy()
    redes.columns = ["zona", "grado_promedio", "pct_contacto_otra_zona",
                      "velocidad_prop_h_salto", "prob_info_correcta"]
    redes["zona"] = ZONAS
    redes = redes.set_index("zona").astype(float)

    vulnerabilidad = ws.iloc[33:38, 0:5].copy()
    vulnerabilidad.columns = ["zona", "pct_autonomo", "pct_necesita_asistencia",
                               "pct_dependiente", "indice_riesgo_rezago"]
    vulnerabilidad["zona"] = ZONAS
    vulnerabilidad = vulnerabilidad.set_index("zona").astype(float)

    return demografia, comportamiento, redes, vulnerabilidad


DEMOGRAFIA, COMPORTAMIENTO, REDES, VULNERABILIDAD = cargar_datos_excel()

# Parametros de comportamiento (globales, Seccion 2 del Excel)
P_ESPONTANEO = COMPORTAMIENTO["Probabilidad de evacuar espontáneamente (sin instrucción)"]
TIEMPO_DECISION_MEDIA_MIN = COMPORTAMIENTO["Tiempo promedio decisión de evacuación (min)"]
TIEMPO_DECISION_SD_MIN = 8.0  # de la columna Distribucion: LogNormal(mu=18, sigma=8)
P_AYUDA_VECINOS = COMPORTAMIENTO["Prob. de ayudar a vecinos antes de evacuar"]
P_BUSCA_REDES = COMPORTAMIENTO["Prob. de buscar información en redes sociales primero"]
P_SIGUE_OFICIAL = COMPORTAMIENTO["Prob. de seguir instrucciones oficiales vs. rumores"]
VELOCIDAD_CAMINATA_MEDIA = COMPORTAMIENTO["Velocidad de evacuación a pie (km/h)"]
MULT_VULN_MAYOR60 = COMPORTAMIENTO["Multiplicador vulnerabilidad adultos mayores (velocidad)"]
UMBRAL_DANIO_VISIBLE = COMPORTAMIENTO["Umbral de daño visible para decidir evacuar (% daño)"]

MINUTOS_POR_BLOQUE = 6 * 60


def prob_info_correcta_campana(campana_activa):
    """Escenario Pregunta 3: una campana oficial reduce a la mitad la
    probabilidad de que circule un rumor (1 - prob_info_correcta)."""
    p_correcta = REDES["prob_info_correcta"].to_numpy()
    if not campana_activa:
        return p_correcta
    p_rumor = 1 - p_correcta
    return 1 - p_rumor / 2


def prob_evacua_al_exponerse(campana_activa=False):
    """P(el agente decide evacuar al ser expuesto a informacion sobre el
    sismo) = P(la info que circula es correcta) + P(es rumor) * P(el agente
    igual sigue instrucciones oficiales al verificar). Combina
    'prob_info_correcta' (Seccion 3, por zona) con 'Prob. de seguir
    instrucciones oficiales vs. rumores' (Seccion 2, global)."""
    p_correcta = prob_info_correcta_campana(campana_activa)
    return p_correcta + (1 - p_correcta) * P_SIGUE_OFICIAL


def prob_asistencia(t, z_idx, tier):
    """No hay un parametro explicito de capacidad de rescate en el Excel de
    Grupo 6 (eso corresponde a Grupo 5); se aproxima con una capacidad de
    rescate generica que mejora con el tiempo, modulada por el 'indice de
    riesgo de rezago' propio de cada zona (Seccion 4) -- a mayor rezago,
    menor probabilidad de que la asistencia llegue a tiempo. Los agentes
    'dependientes' requieren transporte especializado (factor 0.55) frente a
    quienes solo 'necesitan asistencia'. TODO INTERCAMBIO: si se recibiera el
    plan de despliegue de Grupo 5, sustituir esta funcion por sus datos."""
    rezago = VULNERABILIDAD["indice_riesgo_rezago"].iloc[z_idx]
    base = (0.10 + 0.04 * t) * (1 - 0.6 * rezago)
    factor_tier = 0.55 if tier == "dependiente" else 1.0
    return float(np.clip(base * factor_tier, 0.02, 0.9))


# 2. Red social por zona (grado promedio real, Seccion 3 del Excel)
def construir_red_social(seed=7):
    r = np.random.default_rng(seed)
    grafos = []
    offset = 0
    zona_de_agente = np.zeros(N_REP_POR_ZONA * N_ZONAS, dtype=int)
    for z in range(N_ZONAS):
        k = max(2, int(round(REDES["grado_promedio"].iloc[z])))
        if k % 2 == 1:
            k += 1  # watts_strogatz requiere k par
        g = nx.watts_strogatz_graph(N_REP_POR_ZONA, k=k, p=0.05, seed=int(r.integers(1e6)))
        g = nx.relabel_nodes(g, {n: n + offset for n in g.nodes})
        zona_de_agente[offset:offset + N_REP_POR_ZONA] = z
        grafos.append(g)
        offset += N_REP_POR_ZONA
    red = nx.compose_all(grafos)

    # Enlaces entre zonas segun "% con contactos en otra zona" (Seccion 3)
    n_total = N_REP_POR_ZONA * N_ZONAS
    for z in range(N_ZONAS):
        pct = REDES["pct_contacto_otra_zona"].iloc[z]
        nodos_zona = np.where(zona_de_agente == z)[0]
        n_con_contacto = int(round(pct * len(nodos_zona)))
        elegidos = r.choice(nodos_zona, size=n_con_contacto, replace=False)
        otras_zonas = [zz for zz in range(N_ZONAS) if zz != z]
        for nodo in elegidos:
            zona_destino = r.choice(otras_zonas)
            destino = r.choice(np.where(zona_de_agente == zona_destino)[0])
            red.add_edge(int(nodo), int(destino))

    A = nx.to_scipy_sparse_array(red, nodelist=range(n_total), format="csr", dtype=float)
    return red, A, zona_de_agente


# 3. Simulacion de una realizacion
def _muestrear_categoria(r, probs, n):
    """Muestra un indice de categoria (0..k-1) por agente segun probs (que
    pueden no sumar exactamente 1 por redondeo del Excel; se normalizan)."""
    probs = np.asarray(probs, dtype=float)
    probs = probs / probs.sum()
    return r.choice(len(probs), size=n, p=probs)


def correr_realizacion(A, red, zona_de_agente, semilla, campana_activa=False):
    r = np.random.default_rng(semilla)
    n_agentes = len(zona_de_agente)

    # Atributos individuales, muestreados de las proporciones reales del Excel
    mayor60 = np.zeros(n_agentes, dtype=bool)
    smartphone = np.zeros(n_agentes, dtype=bool)
    tier = np.empty(n_agentes, dtype=object)  # 'autonomo' | 'necesita_asistencia' | 'dependiente'

    for z in range(N_ZONAS):
        idx = np.where(zona_de_agente == z)[0]
        n_z = len(idx)

        edad_cat = _muestrear_categoria(
            r,
            [DEMOGRAFIA["pct_menor15"].iloc[z], DEMOGRAFIA["pct_adulto"].iloc[z],
             DEMOGRAFIA["pct_mayor60"].iloc[z]],
            n_z,
        )
        mayor60[idx] = edad_cat == 2

        smartphone[idx] = r.random(n_z) < DEMOGRAFIA["pct_smartphone"].iloc[z]

        tier_cat = _muestrear_categoria(
            r,
            [VULNERABILIDAD["pct_autonomo"].iloc[z],
             VULNERABILIDAD["pct_necesita_asistencia"].iloc[z],
             VULNERABILIDAD["pct_dependiente"].iloc[z]],
            n_z,
        )
        etiquetas = np.array(["autonomo", "necesita_asistencia", "dependiente"])
        tier[idx] = etiquetas[tier_cat]

    espontaneo = r.random(n_agentes) < P_ESPONTANEO
    ayuda_vecinos = r.random(n_agentes) < P_AYUDA_VECINOS  # retrasa 1 bloque su salida
    p_expone_red = np.where(smartphone, 1.0, 0.35)  # sin smartphone, solo boca a boca

    p_evacua_expo_zona = prob_evacua_al_exponerse(campana_activa)

    quiere_evacuar = espontaneo.copy()  # el impulso espontaneo ya se activa en t=0
    evacuado = np.zeros(n_agentes, dtype=bool)
    asistido = np.zeros(n_agentes, dtype=bool)
    retraso_pendiente = ayuda_vecinos.copy()
    ya_espero_su_bloque = np.zeros(n_agentes, dtype=bool)  # ya consumio su unico bloque de retraso

    quiere_pero_no_puede = np.zeros((N_PASOS, n_agentes), dtype=bool)
    evacuados_por_zona_paso = np.zeros((N_PASOS, N_ZONAS))
    nuevos_por_zona_paso = np.zeros((N_PASOS, N_ZONAS))
    # destino: 0 = refugio oficial de su zona, 1 = "se dirige a otra zona" (lazo social)
    destino_otra_zona = np.zeros(n_agentes, dtype=bool)
    flujo_destino_zona_paso = np.zeros((N_PASOS, N_ZONAS, 2))  # [:, :, 0]=oficial, [:,:,1]=otra zona

    for t in range(N_PASOS):
        # Difusion de informacion por la red, limitada a los hops que la
        # velocidad de propagacion real de cada zona permite en un bloque
        hops = {z: max(1, int(round(6.0 / REDES["velocidad_prop_h_salto"].iloc[z])))
                for z in range(N_ZONAS)}
        frontera = evacuado.copy()
        alcanzado = evacuado.copy()
        max_hops = max(hops.values())
        for _ in range(max_hops):
            vecinos_frontera = A @ frontera.astype(float) > 0
            nueva_frontera = vecinos_frontera & (~alcanzado)
            alcanzado |= nueva_frontera
            frontera = nueva_frontera
            if not frontera.any():
                break
        recien_expuesto = alcanzado & (~quiere_evacuar) & (~evacuado)
        acepta_exposicion = r.random(n_agentes) < p_expone_red
        recien_expuesto &= acepta_exposicion

        for z in range(N_ZONAS):
            mask_z = recien_expuesto & (zona_de_agente == z)
            if not mask_z.any():
                continue
            decide = r.random(mask_z.sum()) < p_evacua_expo_zona[z]
            idx_mask = np.where(mask_z)[0]
            quiere_evacuar[idx_mask[decide]] = True

        # Rasgo "ayuda a vecinos": la primera vez que el agente quiere
        # evacuar espera un bloque antes de quedar habilitado para salir
        primera_vez_con_retraso = quiere_evacuar & retraso_pendiente & (~ya_espero_su_bloque) & (~evacuado)
        ya_espero_su_bloque |= primera_vez_con_retraso
        habilitado_por_espera = (~retraso_pendiente) | ya_espero_su_bloque
        listos_para_salir = quiere_evacuar & (~evacuado) & habilitado_por_espera

        autonomos = listos_para_salir & (tier == "autonomo")
        vulnerables_listos = listos_para_salir & (tier != "autonomo")

        for z in range(N_ZONAS):
            idx = np.where(vulnerables_listos & (zona_de_agente == z))[0]
            if len(idx) == 0:
                continue
            p_necesita = prob_asistencia(t, z, "necesita_asistencia")
            p_dependiente = prob_asistencia(t, z, "dependiente")
            probs = np.where(tier[idx] == "dependiente", p_dependiente, p_necesita)
            llega_ayuda = r.random(len(idx)) < probs
            asistido[idx[llega_ayuda]] = True
            quiere_pero_no_puede[t, idx[~llega_ayuda]] = True

        nuevos_evacuados = autonomos | (vulnerables_listos & asistido)
        evacuado |= nuevos_evacuados

        # Ruta y destino preferido segun comportamiento real (Seccion 3)
        idx_nuevos = np.where(nuevos_evacuados)[0]
        if len(idx_nuevos) > 0:
            pct_otra = REDES["pct_contacto_otra_zona"].to_numpy()[zona_de_agente[idx_nuevos]]
            va_a_otra_zona = r.random(len(idx_nuevos)) < pct_otra
            destino_otra_zona[idx_nuevos] = va_a_otra_zona

        for z in range(N_ZONAS):
            mask_z = zona_de_agente == z
            evacuados_por_zona_paso[t, z] = evacuado[mask_z].sum() * FACTOR_ESCALA[z]
            nuevos_mask = nuevos_evacuados & mask_z
            nuevos_por_zona_paso[t, z] = nuevos_mask.sum() * FACTOR_ESCALA[z]
            flujo_destino_zona_paso[t, z, 0] = (nuevos_mask & (~destino_otra_zona)).sum() * FACTOR_ESCALA[z]
            flujo_destino_zona_paso[t, z, 1] = (nuevos_mask & destino_otra_zona).sum() * FACTOR_ESCALA[z]

    return {
        "evacuados_por_zona_paso": evacuados_por_zona_paso,
        "nuevos_por_zona_paso": nuevos_por_zona_paso,
        "flujo_destino_zona_paso": flujo_destino_zona_paso,
        "quiere_pero_no_puede": quiere_pero_no_puede,
        "tier": tier,
        "zona_de_agente": zona_de_agente,
    }


if __name__ == "__main__":
    import time

    print("Parametros de comportamiento cargados del Excel:")
    print(COMPORTAMIENTO)
    print("\nRedes sociales por zona:\n", REDES)
    print("\nVulnerabilidad por zona:\n", VULNERABILIDAD)

    red, A, zona_de_agente = construir_red_social()

    t0 = time.time()
    resultados = []
    for i in range(N_REALIZACIONES):
        res = correr_realizacion(A, red, zona_de_agente, semilla=100 + i)
        resultados.append(res["evacuados_por_zona_paso"])
    resultados = np.array(resultados)
    print(f"\n{N_REALIZACIONES} realizaciones en {time.time() - t0:.2f} s")

    media = resultados.mean(axis=0)
    print("\nMedia de evacuados acumulados por zona en el paso 12 (72h):")
    for z, val in zip(ZONAS, media[-1]):
        print(f"  {z}: {val:,.0f} personas")
