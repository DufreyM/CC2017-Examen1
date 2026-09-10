# Grupo 6: Comportamiento de la Población y Toma de Decisiones
## CC2017, Modelación y Simulación, Examen Práctico

> Todos los parámetros de este informe provienen del archivo Excel oficial
> del catedrático (`data/raw/Grupo6_ComportamientoPoblacional.xlsx`, hoja
> `Datos_Grupo6`), cargado directamente en `src/grupo6_model.py`. La única
> excepción documentada es la **población absoluta por zona**, que el Excel
> no incluye (solo da porcentajes demográficos y de vulnerabilidad). Se
> asume reparto igualitario de los 250,000 habitantes, 50,000 por zona,
> hasta confirmar lo contrario en el intercambio presencial.

## 1. Justificación del paradigma

Se modela el comportamiento poblacional con **ABM (modelado basado en
agentes)**. La pregunta central de este grupo es qué fracción de la
población evacúa, cuándo, hacia dónde, y cómo la desinformación altera esa
decisión. Eso depende de **decisiones individuales heterogéneas** (umbral
de riesgo propio, vulnerabilidad, acceso a smartphone, confianza en canales
oficiales) y de una **interacción local no lineal**: la decisión de evacuar
de una persona se propaga por su red social real, cuyo grado promedio y
velocidad de propagación de información están medidos por zona en el
Excel (Sección 3).

Un modelo de Dinámica de Sistemas trataría la evacuación como un único
stock agregado con un flow de entrada gobernado por una tasa promedio,
asumiendo mezcla homogénea: cualquier persona tendría la misma probabilidad
de contagiarse de la decisión de evacuar, sin importar en qué zona está ni
con quién está conectada. Eso es justo lo que el Excel contradice. El grado
de red, la velocidad de propagación y la probabilidad de rumor son
distintos en cada zona, y esa heterogeneidad de red es la que explica que
Z4 evacúe proporcionalmente más rápido que Z1 pese a tener, según los datos
de vulnerabilidad, mayor capacidad de autoevacuación de base. Un ABM con
una red social explícita conserva esa estructura, un stock agregado la
borra por construcción.

Dicho de otro modo, el mecanismo de que una persona ve evacuar a sus
vecinos y decide evacuar también es, en su forma más agregada, un ciclo de
realimentación reforzador: más evacuados visibles generan más decisiones de
evacuar. Es la misma estructura matemática que gobierna una curva de
adopción o una curva de contagio. Esa estructura, escrita como una sola
ecuación diferencial, describiría un crecimiento agregado pero no podría
distinguir una zona de otra ni decir cuál se satura primero, y diferenciar
zonas y momentos es exactamente lo que exige la Pregunta 1. Por eso el
mecanismo de contagio se implementa sobre una red de agentes heterogéneos
en vez de colapsarlo en una única ecuación agregada.

Se descarta DES porque el foco no es una cola de eventos discretos
compitiendo por un recurso compartido, ese es el caso de Grupo 2, 3 y 5,
sino la propagación de una decisión a través de una población heterogénea y
su red social.

La regla de decisión implementada combina un **mecanismo de contagio social
explícito sobre grafo** (no un promedio agregado) con la probabilidad real
de que la información que circula en cada zona sea correcta o sea un rumor
(Sección 3 del Excel).

## 2. Descripción del modelo (ODD simplificado)

**Entidades y atributos:** agente representativo, un super agente donde
cada uno pondera por `50,000/2,000 = 25` habitantes reales por zona, con
`zona`, `edad` (menor15/adulto/mayor60, Sección 1), `smartphone` (Sección
1), `tier` de vulnerabilidad (autónomo, necesita_asistencia o dependiente,
Sección 4), y rasgos de comportamiento `espontáneo` y `ayuda_vecinos`
(Bernoulli con las probabilidades globales de la Sección 2).

**Zona:** grado promedio de red social, porcentaje con contactos fuera de
la zona, velocidad de propagación de información (horas por salto),
probabilidad de que la información que circula sea correcta o sea rumor
(Sección 3); y porcentaje autónomo, necesita asistencia y dependiente, más
el índice de riesgo de rezago (Sección 4).

**Reglas de comportamiento y ecuaciones de estado** (`src/grupo6_model.py`,
función `correr_realizacion`):
1. **Impulso espontáneo:** 35% de los agentes decide evacuar desde el
   bloque 0 (el tiempo de decisión real, unos 18 minutos en promedio, es
   insignificante frente a un bloque de 6 horas).
2. **Difusión de información por la red social:** en cada bloque, la
   evacuación visible de unos agentes se propaga hacia sus vecinos hasta
   `hops = round(6 / velocidad_propagación_zona)` saltos de red, mucho más
   rápido en zonas mejor conectadas (Z4: unos 15 saltos por bloque) que en
   zonas aisladas (Z5: unos 4 saltos por bloque). Los agentes sin
   smartphone solo se enteran boca a boca (alcance de 1 salto).
3. **Decisión al ser expuesto:** `P(evacúa dado expuesto, zona) =
   prob_info_correcta_zona + (1 - prob_info_correcta_zona) * P_sigue_oficial`,
   combinando qué tan confiable es la información que circula en esa zona
   con la probabilidad global (0.54) de que la persona igual termine
   siguiendo instrucciones oficiales aunque haya oído un rumor.
4. **Ayuda a vecinos:** un agente con ese rasgo (48%) retrasa su propia
   salida exactamente un bloque de 6 horas la primera vez que decide
   evacuar.
5. **Restricción de vulnerabilidad:** un agente autónomo evacúa en cuanto
   decide hacerlo. Uno que necesita asistencia o es dependiente solo evacúa
   si recibe asistencia activa ese bloque, con probabilidad calibrada según
   el **índice de riesgo de rezago real de su zona** (a mayor rezago, menor
   probabilidad de asistencia a tiempo) y un factor adicional de 0.55 para
   los dependientes por requerir transporte especializado. Si no recibe
   asistencia, queda registrado como "quiere pero no puede".
6. **Ruta y destino:** al evacuar, un agente con lazos fuera de su zona
   (según el porcentaje de contactos en otra zona real de su zona) se
   dirige a otra zona en vez del refugio oficial asignado.

**Diagrama de estado del agente:**

```
NO EVACUADO (no decidido)
   |  espontaneo=True (bloque 0)
   |  o expuesto por la red y decide creer el mensaje
   v
QUIERE EVACUAR
   |-- si tiene el rasgo "ayuda a vecinos" y aun no espero su bloque:
   |       espera un bloque y vuelve a QUIERE EVACUAR (ya habilitado)
   |-- si es autonomo: EVACUADO (inmediato)
   |-- si necesita asistencia o es dependiente: cada bloque se sortea si
   |       llega asistencia; si no llega, queda "quiere pero no puede" y
   |       reintenta en el bloque siguiente
   v
EVACUADO (estado terminal; elige destino: refugio oficial u otra zona)
```

**Restricción de vulnerabilidad como tasa de riesgo variable en el
tiempo:** `prob_asistencia` no es una probabilidad fija por bloque, crece
con el tiempo (`0.10 + 0.04*t`, penalizada por el índice de rezago de la
zona). Esa elección no es neutra. Si en cambio fuera constante, equivalente
a suponer que la espera adicional no cambia nada, el backlog de personas
sin asistencia bajaría de forma exponencial en vez de acelerar su
resolución conforme se despliegan más recursos de rescate. La forma
creciente es una hipótesis explícita sobre cómo opera el rescate, no un
supuesto de conveniencia.

**Scheduling:** tiempo discreto, 12 bloques de 6 horas, actualización
síncrona, todas las decisiones de un bloque parten del estado al cierre del
bloque anterior. Se elige síncrono sobre asíncrono porque cada bloque ya
representa 6 horas reales, un intervalo donde, en la práctica, miles de
decisiones individuales ocurren de forma continua y desordenada dentro del
mismo bloque. Resolver esa asincronía fina exigiría una resolución temporal
menor a la que da el Excel (bloques de 6 horas). El bloque discreto ya
actúa como una agregación de lo que sería asincronía a escala de minutos,
así que la actualización síncrona entre bloques es la aproximación
consistente con esa escala temporal, no una simplificación arbitraria.

**Comunicación entre entidades:** difusión sobre una red social explícita,
un grafo calibrado al grado promedio real de cada zona, más enlaces entre
zonas según el porcentaje de contactos en otra zona.

**Distribución inicial:** edad, acceso a smartphone y tier de
vulnerabilidad se muestrean por agente según los porcentajes exactos de la
Sección 1 y 4 del Excel, zona por zona.

## 3. Resultados y análisis

*(30 realizaciones por escenario. Ver `notebooks/grupo6_modelo.ipynb` para las
trayectorias completas y las gráficas generadas.)*

**Verificación del modelo:** antes de interpretar resultados se confirmó
que, primero, el esquema de actualización procesa a cada agente exactamente
una vez por bloque (las decisiones se calculan con operaciones
vectorizadas sobre arreglos de tamaño fijo, sin posibilidad de saltarse o
repetir un agente), y segundo, la distribución inicial de atributos
simulada coincide con la especificada en el Excel: la diferencia máxima
entre el porcentaje simulado y el porcentaje del Excel, comparando las 5
zonas y los 3 niveles de vulnerabilidad, es de apenas 2.0 puntos
porcentuales, ruido esperable por el tamaño finito de la muestra (2,000
agentes por zona), no un error sistemático.

**Intervalos de confianza:** se calculan por bootstrap (remuestreo con
reemplazo de las 30 realizaciones, 2,000 veces, y percentiles 2.5 y 97.5 de
esas medias remuestreadas) en vez de la fórmula paramétrica de la t de
Student, porque los conteos de evacuados están acotados por la población de
cada zona y pueden ser asimétricos, y el bootstrap no requiere asumir
normalidad.

**Momentos críticos:** a las 12 horas (bloque 2), ya se proyectan en
promedio 23,818 evacuados acumulados en Z1 y 37,827 en Z4 (de 50,000
habitantes asumidos por zona). Z4 y Z2, las zonas mejor conectadas, evacúan
más rápido que Z1 y Z5 pese a que estas últimas concentran mayor
daño y aislamiento según el índice de rezago, precisamente porque la
difusión de información es más lenta ahí.

### Pregunta 1: Autoevacuación en Z1 y Z5 en las primeras 12 horas

**Z1.** El 70.6% de la población no autónoma (IC95% entre 70.1% y 71.0%)
quiso evacuar en las primeras 12 horas y no pudo por falta de asistencia a
tiempo.

**Z5.** El 61.6% no pudo hacerlo (IC95% entre 61.2% y 62.2%).

**Ventana crítica.** El backlog de personas "quiere pero no puede" en Z1
alcanza su **pico en el bloque 3 (18 horas)**, con 14,386 personas en
espera, y solo baja a la mitad de ese pico hacia el bloque 8 (48 horas). En
Z5 el pico es aún mayor, 17,232 personas en el bloque 4 (24 horas), y a las
72 horas todavía quedan 5,749 personas sin asistencia en Z5 y 3,627 en Z1.
El bloque con más nuevas evacuaciones, es decir el de mayor efecto marginal
de reforzar la asistencia, es el **bloque 2 (6 a 12 horas) en Z1** y el
**bloque 1 (0 a 6 horas) en Z5**. Dicho de otra forma, la ventana crítica
para desplegar recursos de rescate es **inmediatamente después del sismo**,
no horas después: cuanto más se tarda el primer refuerzo, más crece el
backlog antes de empezar a bajar, y ese backlog nunca llega a cero dentro
del horizonte de 72 horas simulado.

### Pregunta 2: Rutas modeladas contra rutas óptimas
El mayor cuello de botella **no es de capacidad vial** (ese dato pertenece
a Grupo 4 y Grupo 6 no lo recibe formalmente, así que no se inventa), sino
de **planificación de refugios**: en **Z4, el 64.9%** de los evacuados se
dirige a otra zona en vez del refugio oficial asignado (17,331 al refugio
oficial contra 32,033 hacia otra zona, acumulado en 72 horas). En **Z2, el
57.6%** hace lo mismo. En cambio, **Z5 (22.0%) y Z3 (31.0%)** se apegan
mucho más a su refugio oficial. La causa es directamente el dato real de la
Sección 3 del Excel, el porcentaje de contactos en otra zona: las zonas con
redes sociales más extendidas fuera de su zona son las que más se desvían
del plan oficial de refugios. La intervención más costo efectiva no es
forzar a la población a seguir la ruta oficial contra su comportamiento
real, sino **anunciar explícitamente que los refugios aceptan evacuados de
cualquier zona y coordinar el transporte de suministros según el flujo real
observado**, no según la zona de residencia registrada.

### Pregunta 3: Efecto de la desinformación
Comparando el escenario base (probabilidad real de información correcta
por zona) contra una campaña oficial que reduce a la mitad la probabilidad
de rumor, a las 48 horas se evacúan adicionalmente (media, IC95%):

| Zona | Personas adicionales | IC 95% |
|---|---|---|
| Z3 | 690 | 480 a 900 |
| Z1 | 579 | 377 a 781 |
| Z5 | 467 | 218 a 715 |
| Z2 | 130 | -34 a 294 |
| Z4 | -27 | -125 a 72 |

El efecto es estadísticamente significativo (IC lejos de cero) en **Z3, Z1
y Z5**, precisamente las zonas con menor probabilidad de información
correcta de base (Z5: 0.48, Z3: 0.55, Z1: 0.61), y por tanto más margen de
mejora. En **Z2 y Z4** (las zonas con información ya más confiable, 0.74 y
0.81) el intervalo cruza cero: una campaña de comunicación ahí tiene un
efecto no distinguible de cero con esta parametrización, porque el
problema en esas zonas no es la desinformación sino la velocidad de
decisión, que la campaña no ataca.

**Robustez de esta conclusión:** el mecanismo de la Pregunta 3 depende de
`P_SIGUE_OFICIAL` (probabilidad de seguir instrucciones oficiales en vez de
un rumor), que el Excel reporta como un valor puntual de encuesta (0.54),
pero toda encuesta de comportamiento tiene margen de error de muestreo. Se
repitió la comparación campaña contra base variando ese valor entre 0.39 y
0.69 (15 muestras): en las 15 muestras, **Z3 se mantuvo como la zona más
beneficiada por la campaña**, es decir, la conclusión no depende del
decimal exacto que reporta el Excel para ese parámetro.

## 4. Incorporación del intercambio presencial

Según la tabla de dependencias del examen, **Grupo 6 es proveedor puro**:
entrega la proyección de flujo de desplazados a Grupo 1 (outputs a, b y c,
ver `data/processed/output_a_flujo_desplazados.csv`,
`output_b_atrapados_sin_asistencia.csv` y `output_c_rutas_preferidas.csv`),
pero no figura como receptor formal de ningún otro grupo. Las tres
preguntas de Grupo 6 son de análisis propio. *(Pendiente: confirmar con el
catedrático el día del intercambio si aplica alguna entrega informal, en
particular el desglose real de población por zona, que este modelo tuvo
que suponer igualitario por no venir en el Excel. Si se recibe, actualizar
`POBLACION_ZONA` en `src/grupo6_model.py` y volver a correr el notebook
completo; la estructura del modelo no cambia.)*

## 5. Limitaciones y propuestas de mejora

1. **Población por zona asumida igualitaria (50,000 en cada una):** el
   Excel de Grupo 6 no incluye este dato. Con más tiempo se solicitaría
   explícitamente al catedrático o se validaría contra el dato que sí
   maneja Grupo 1.
2. **Escala de agentes:** se simulan 2,000 agentes representativos por zona
   (10,000 en total) en vez de 250,000 habitantes reales, mediante un
   factor de escala de 25. Se validó que el grado promedio de la red
   simulada coincide con el del Excel (comparación en el notebook, sección
   3), pero no se validó que el factor de escala no distorsione la
   velocidad de propagación a nivel poblacional completo.
3. **Capacidad de asistencia y rescate sin dato propio:** Grupo 6 no recibe
   el plan de despliegue de Grupo 5, así que la probabilidad de asistencia
   es una función genérica calibrada solo con el índice de riesgo de
   rezago propio de cada zona. Si se recibiera el dato real de Grupo 5, se
   reemplazaría esa función directamente.
4. **Actualización síncrona por bloque:** dentro de cada bloque de 6 horas
   todas las decisiones se calculan a partir del mismo estado inicial del
   bloque, sin un orden de activación explícito entre agentes. Es
   razonable a la escala de 6 horas que impone el Excel, pero no captura
   el orden exacto en que las decisiones se propagan dentro de una misma
   ventana de horas. Hacerlo requeriría una resolución temporal más fina
   con activación secuencial, lo que multiplicaría el costo computacional
   sin un beneficio claro dado que el Excel ya entrega los datos agregados
   por bloques de 6 horas.
