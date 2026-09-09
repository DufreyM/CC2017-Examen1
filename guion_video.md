# Guion de video, Grupo 6 (3 a 5 minutos)

Recuerden: al menos un integrante hablando en cámara, nada de pantalla sola
sin voz, y nada de guion leído textualmente (usar esto como guía de
contenido, no para leer palabra por palabra).

### Punto 1: Decisión de diseño más difícil (45 segundos)
**Contenido sugerido:** la decisión más difícil no fue elegir ABM, sino
**cómo traducir los datos de red social del Excel (grado promedio,
velocidad de propagación en horas por salto, probabilidad de info
correcta) en un mecanismo real de difusión sobre un grafo**, en vez de un
promedio agregado. Se optó por simular explícitamente cuántos saltos de
red puede recorrer la información en un bloque de 6 horas según la
velocidad real de cada zona (por ejemplo, en Z4 la información recorre
hasta 15 saltos por bloque, en Z5 solo unos 4), usando una red de 2,000
agentes representativos por zona para que fuera computacionalmente
tratable. El trade off: se gana un mecanismo de contagio fiel a los datos
reales de la Sección 3, se pierde la resolución uno a uno con los 250,000
habitantes reales (limitación documentada en el reporte).

### Punto 2: Resultado más importante (60 segundos)
**Mostrar en pantalla:** la gráfica de "Poblacion vulnerable sin asistencia
por bloque (Z1 y Z5)" del notebook (sección 6, output b).
**Explicar verbalmente:** el backlog de personas que quieren evacuar y no
pueden por falta de asistencia llega a un pico de **14,386 personas en Z1 a
las 18 horas** y de **17,232 en Z5 a las 24 horas**, y ese backlog **no
llega a cero ni siquiera a las 72 horas** (quedan 3,627 en Z1 y 5,749 en
Z5). Mencionar el intervalo de confianza: "estas cifras vienen de 30
corridas del modelo, y el intervalo de confianza del 95%, calculado por
bootstrap, sin asumir que la variable se distribuye normal, es de apenas
unos cientos de personas alrededor de la media. La incertidumbre por
aleatoriedad individual es pequeña frente al tamaño del problema, así que
la conclusión de que el sistema no logra atender a tiempo a esta población
es robusta."

### Punto 3: El intercambio presencial (60 segundos)
**Contenido sugerido:** explicar que, según la cadena de dependencias del
examen, Grupo 6 es el que **entrega** información (a Grupo 1: proyección de
flujo, backlog sin asistencia, y mapa de rutas preferidas) y no aparece
como receptor formal de ningún otro grupo. Sus tres preguntas son de
análisis propio. Mencionar el vacío de datos que sí les habría servido: el
Excel de Grupo 6 no trae la población absoluta por zona, así que se asumió
un reparto igualitario de 50,000 habitantes por zona, documentado como
supuesto explícito. Si en el intercambio presencial recibieron ese dato, o
el plan de rescate de Grupo 5, decir aquí concretamente qué cambió al
sustituirlo.

*(Actualizar este punto con lo que realmente ocurra el día del examen.)*

### Punto 4: Pregunta abierta (45 segundos)
Pregunta asignada a Grupo 6: *"¿Considera que el paradigma que eligió es el
más adecuado para capturar el efecto de contagio social, o hay algo en la
naturaleza del fenómeno que su paradigma no puede representar sin importar
qué parámetros use?"*

**Respuesta sugerida (ideas, no texto para leer literal):**
- ABM sí es el paradigma correcto para el contagio social por vecindario
  local. El Excel mismo mide grado de red y velocidad de propagación por
  zona, datos que solo tienen sentido si se simulan sobre un grafo
  explícito. Un modelo agregado de Dinámica de Sistemas no podría
  reproducir que Z4 evacue proporcionalmente más rápido que Z1 y Z5 pese a
  menor daño y aislamiento, simplemente por tener una red mejor conectada.
- Pero hay un límite estructural, no de parámetros: el modelo asume que la
  **estructura de la red social es fija** durante las 72 horas. En la
  realidad, después de un desastre la red de contacto cambia dinámicamente
  (la gente se agrupa físicamente distinto, pierde o gana señal celular, se
  desplaza junto con sus contactos), y ningún ajuste de parámetros dentro
  del modelo actual corrige eso. Haría falta un modelo de red dinámica y
  adaptativa, no solo recalibrar el grado promedio o la velocidad de
  propagación.
- Mencionar también que el modelo trata si la información es correcta o es
  rumor como una probabilidad fija por zona, cuando en la realidad esa
  probabilidad cambia con el tiempo (los rumores se corrigen o se refuerzan
  según lo que la gente observa). Es otra simplificación estructural, no
  un tema de calibración de parámetros.
