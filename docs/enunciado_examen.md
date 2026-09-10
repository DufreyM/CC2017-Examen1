# CC2017 – Modelación y Simulación
## Examen Práctico

### Instrucciones
- Esta es una actividad en grupos de no más de **4 o 5 integrantes**.
  - Recuerden unirse al grupo de canvas.
- No se permitirá ni se aceptará cualquier indicio de copia. De presentarse, se procederá según el reglamento correspondiente.
- Tendrán hasta el día indicado en Canvas.
  - No se confíen, aprovechen el tiempo en clase para entender todos los ejercicios y avanzar lo más posible.
- **NOTA**: Limiten el uso de IA generativa. Intenten primero buscar en fuentes de internet y si en verdad necesitan usarla, asegúrense de colocar el prompt que utilizan para cada task donde corresponda, así como una explicación de por qué ese prompt funcionó.

### Contexto del escenario
El 14 de noviembre a las 4:00 AM, un terremoto de magnitud 6.8 sacudió Ciudad UVG, una ciudad de 250,000 habitantes dividida en cinco zonas urbanas. El evento causó daños estructurales diferenciados por zona, desplazó a decenas de miles de personas, saturó el sistema hospitalario y comprometió la infraestructura vial.

La Municipalidad activó el Comité de Emergencia. Cada grupo representa una unidad técnica de ese comité con acceso a información específica de su área. Su trabajo es modelar la dinámica de su componente del sistema, producir un análisis técnico formal, y en el intercambio presencial compartir sus conclusiones con los grupos que las necesitan para completar su propio análisis.

El horizonte de simulación es de **72 horas post-evento**, dividido en bloques de **6 horas (12 pasos de tiempo)**.

### Cadena de Dependencia entre Grupos

| Grupo que entrega | Entrega a | Qué entrega |
|---|---|---|
| Grupo 6 | Grupo 1 | Proyección de flujo de desplazados por zona y momento |
| Grupo 1 | Grupo 2 y Grupo 3 | Demanda de atención médica y demanda de suministros por zona |
| Grupo 4 | Grupo 3 y Grupo 5 | Mapa de accesibilidad e índice de aislamiento por zona |
| Grupo 2 | Grupo 7 | Reporte de saturación hospitalaria y recursos críticos |
| Grupo 3 | Grupo 7 | Balance de suministros y cuellos de botella |
| Grupo 5 | Grupo 7 | Plan de despliegue de personal y requerimiento de refuerzos |

Los outputs exactos que debe producir cada grupo están especificados en la última sección de su archivo Excel.

---

## Requisitos del Modelo

Cada grupo debe implementar un modelo de simulación que cumpla los siguientes requisitos mínimos:

- **Paradigma**: el grupo debe justificar formalmente qué paradigma o combinación de paradigmas (SD, ABM, DES) usa para modelar su componente del sistema, y por qué ese paradigma es el más adecuado para la pregunta que responde su grupo. Esta justificación es parte evaluable del reporte.
- **Heterogeneidad**: el modelo debe capturar diferencias entre zonas o entre tipos de entidades. No se acepta un modelo que trate todas las zonas como equivalentes.
- **Dinámica temporal**: el modelo debe producir trayectorias a lo largo de los 12 pasos de tiempo, no solo un resultado estático al final.
- **Incertidumbre**: el modelo debe correr al menos 30 realizaciones y reportar los resultados como distribuciones con media e intervalo de confianza del 95%, no como valores puntuales.
- **Incorporación del intercambio**: el reporte debe mostrar explícitamente cómo la información recibida en el intercambio presencial modificó o complementó el modelo. Si la información recibida contradice algún supuesto del modelo propio, el grupo debe documentar cómo resolvió esa contradicción.

---

## Preguntas por Grupo

### Grupo 1: Dinámica de Población Desplazada

**Pregunta 1 (Análisis propio):**
Con base en su modelo de dinámica de desplazados y la capacidad operativa de los albergues disponibles, determine en qué zona y en qué bloque de tiempo el sistema de albergues supera el 80% de su capacidad operativa por primera vez. ¿Qué ocurre con las personas que no encuentran lugar en ese momento y cómo afecta eso la dinámica del sistema en los bloques siguientes?

**Pregunta 2 (Integración del intercambio):**
El Grupo 6 les entregó la proyección de flujo real de desplazados basada en el comportamiento poblacional modelado. Compare esa proyección con la estimación que su grupo usó antes del intercambio. ¿En cuántas horas difiere el momento de colapso del sistema de albergues entre ambas estimaciones? ¿Qué supuesto de su modelo inicial era incorrecto y cómo lo corrigió?

### Grupo 2: Sistema Hospitalario y Atención Médica

**Pregunta 1 (Análisis propio):**
Con base en su modelo de saturación hospitalaria y los parámetros de atención disponibles, determine qué instalación colapsa primero, en qué bloque de tiempo, y qué recurso específico (camas, personal, suministros médicos) es el cuello de botella determinante. Justifique su respuesta con las trayectorias de su modelo.

**Pregunta 2 (Integración del intercambio):**
El Grupo 1 les entregó la proyección de desplazados que requieren atención médica por zona y bloque de tiempo. Incorpore esa demanda a su modelo y estime cuántas muertes evitables adicionales se producen en las primeras 48 horas respecto al escenario base que su grupo había proyectado antes del intercambio. ¿Qué intervención específica reduciría más esa cifra?

### Grupo 3: Cadena de Suministro de Ayuda Humanitaria

**Pregunta 1 (Análisis propio):**
Con base en su modelo de inventarios y distribución, determine cuál es el primer suministro crítico en agotarse, en qué zona y en qué bloque de tiempo, considerando únicamente sus datos iniciales y las tasas de consumo especificadas. ¿Cuántas horas de margen existen para evitar ese agotamiento si se activa un convoy de reposición en el momento óptimo?

**Pregunta 2 (Integración del intercambio):**
El Grupo 1 les entregó la demanda real de suministros y el Grupo 4 les entregó el mapa de rutas disponibles. Incorpore ambas informaciones a su modelo y determine si la zona más crítica según su análisis inicial sigue siendo la misma. Si cambió, explique qué factor del intercambio modificó esa conclusión. Si no cambió, explique por qué la información recibida confirmó su proyección.

### Grupo 4: Infraestructura y Accesibilidad

**Pregunta 1 (Análisis propio):**
Con base en su modelo de infraestructura vial, determine el índice de aislamiento de cada zona en cada bloque de tiempo. ¿Cuál zona permanece más tiempo en aislamiento crítico (índice menor a 0.3) y qué infraestructura específica, vía, puente o servicio, es la que más contribuye a ese aislamiento?

**Pregunta 2 (Análisis propio):**
Identifique las dos intervenciones de reparación cuya ejecución prioritaria tendría el mayor impacto sobre la accesibilidad global de la ciudad en las primeras 24 horas. Justifique su selección con base en el impacto cuantificado sobre el índice de aislamiento agregado de las zonas críticas, no en el costo de la intervención.

**Pregunta 3 (Análisis propio):**
Con base en el cronograma de reparaciones y los recursos disponibles, determine si es posible que todas las zonas alcancen un índice de aislamiento mayor a 0.6 antes de las 48 horas post-evento. Si no es posible, identifique qué recurso adicional (maquinaria, personal técnico, combustible) sería el determinante para lograrlo y en qué cantidad mínima.

### Grupo 5: Coordinación de Voluntarios y Personal de Rescate

**Pregunta 1 (Análisis propio):**
Con base en su modelo de despliegue de personal y las restricciones operativas especificadas, determine en qué bloque de tiempo el personal de rescate activo en Z1 y Z5 es insuficiente para atender todos los casos activos simultáneamente. ¿Cuántos efectivos adicionales mínimos se necesitan en ese momento para mantener la capacidad de respuesta?

**Pregunta 2 (Integración del intercambio):**
El Grupo 4 les entregó el mapa de accesibilidad e índice de aislamiento por zona. Incorpore esa información a su modelo de despliegue: ¿en qué bloques de tiempo el personal asignado a Z1 o Z5 no puede llegar físicamente a su zona de operación por restricciones de acceso? ¿Cómo reasignaría ese personal durante esos bloques para minimizar la pérdida de capacidad operativa?

### Grupo 6: Comportamiento de la Población y Toma de Decisiones

**Pregunta 1 (Análisis propio):**
Con base en su modelo de comportamiento poblacional y los parámetros de vulnerabilidad por zona, determine qué porcentaje de la población de Z1 y Z5 no podrá autoevacuar sin asistencia activa en las primeras 12 horas. ¿En qué ventana de tiempo específica es más crítica esa intervención y por qué después de esa ventana el impacto de la asistencia se reduce significativamente?

**Pregunta 2 (Análisis propio):**
Su modelo captura el comportamiento real de la población, que no necesariamente sigue las rutas de evacuación óptimas. Compare las rutas que su modelo predice que la población tomará con las rutas óptimas desde el punto de vista de infraestructura. ¿Dónde se generan los mayores cuellos de botella de evacuación? ¿Qué intervención de comunicación o señalización cambiaría ese comportamiento y en qué magnitud?

**Pregunta 3 (Análisis propio):**
Modele el efecto de la desinformación: su modelo incluye una probabilidad de que la información que circula en redes sociales sea incorrecta. Evalúe dos escenarios, uno donde esa probabilidad se mantiene en su valor base y otro donde se reduce a la mitad por una campaña de comunicación oficial activa. ¿Cuántas personas adicionales logran evacuar exitosamente en el escenario optimizado y en qué zonas es más significativa la diferencia?

### Grupo 7: Política Pública y Asignación de Recursos

**Pregunta 1 (Análisis propio):**
Con base únicamente en los datos de su archivo y antes de incorporar la información del intercambio, proponga una asignación inicial de recursos para las primeras 24 horas. Evalúe esa asignación contra las cuatro métricas de política definidas en su archivo. ¿Cuál métrica es la más difícil de cumplir con los recursos disponibles y por qué?

**Pregunta 2 (Integración del intercambio):**
Incorpore los reportes recibidos de los Grupos 2, 3 y 5. ¿Cambia su asignación inicial de recursos? Identifique la decisión que más cambió después del intercambio, justifique con los datos recibidos por qué cambió, y cuantifique el impacto de ese cambio sobre al menos dos de las cuatro métricas de evaluación.

---

## Reporte Técnico

El reporte tiene un **máximo de 8 páginas** y debe seguir esta estructura:

1. **Justificación del paradigma (1 página)** — Argumente formalmente qué paradigma usa y por qué. Si combina paradigmas, justifique la frontera entre ellos. Haga referencia explícita a los criterios de selección vistos en clase.
2. **Descripción del modelo (2 páginas)** — Describa el modelo en formato ODD simplificado: entidades y atributos, reglas de comportamiento o ecuaciones de estado, modo de scheduling si aplica, mecanismo de comunicación entre entidades, y distribución inicial de atributos.
3. **Resultados y análisis (3 páginas)** — Presente las trayectorias del modelo con intervalos de confianza. Identifique los momentos críticos del sistema (cuándo se satura, cuándo colapsa, cuándo se estabiliza). Incluya el análisis del output requerido especificado en su archivo Excel y las respuestas a las preguntas de su grupo.
4. **Incorporación del intercambio (1 página)** — Documente qué recibió en el intercambio presencial, cómo lo incorporó al modelo, y qué cambió en sus conclusiones después de incorporarlo.
5. **Limitaciones y propuestas de mejora (1 página)** — Identifique al menos dos limitaciones estructurales de su modelo. Proponga cómo las resolvería con más tiempo o datos.

---

## Video de Presentación

El video debe tener entre **3 y 5 minutos**. Debe mostrar el modelo en funcionamiento y cumplir los siguientes cuatro puntos en el orden indicado:

- **Punto 1 — Decisión de diseño más difícil (45 seg):** Explique cuál fue la decisión de diseño más difícil que tomó su grupo (paradigma, scheduling, inicialización, regla de comportamiento) y por qué la tomó así. No describa el modelo completo; concéntrese en esa decisión específica.
- **Punto 2 — Resultado más importante (60 seg):** Muestre en pantalla el gráfico o tabla más importante de sus resultados y explíquelo verbalmente. Debe mencionar el intervalo de confianza y qué implica para la incertidumbre de la conclusión.
- **Punto 3 — El intercambio presencial (60 seg):** Explique qué información recibió de otro grupo, cómo la incorporó, y si cambió o confirmó sus conclusiones previas al intercambio.
- **Punto 4 — Pregunta abierta (45 seg):** Al final del video, cada grupo responde la pregunta abierta que se asignará. La pregunta es distinta para cada grupo.

El video debe mostrar al menos un integrante del grupo hablando en cámara. No se aceptan videos de solo pantalla sin voz. No se aceptan guiones leídos.

---

## Preguntas Abiertas

Las siguientes preguntas se asignan el día del examen. Cada grupo recibe únicamente la suya y debe responderla en el Punto 4 del video:

- **Grupo 1:** Su modelo proyecta el flujo de desplazados hacia los albergues, pero los albergues no son el único destino posible: algunas personas se quedan con familiares, otras permanecen en sus viviendas dañadas por miedo o desinformación. ¿Qué supuesto de su modelo considera que tiene mayor potencial de invalidar sus conclusiones sobre el colapso del sistema de albergues, y qué datos reales necesitaría para corregirlo?
- **Grupo 2:** Su modelo identifica cuellos de botella en el sistema hospitalario, pero un modelo siempre simplifica. ¿Qué aspecto de la realidad hospitalaria durante un desastre considera que su modelo captura peor, y cómo esa simplificación podría estar llevando a la Municipalidad a tomar una decisión equivocada con base en sus resultados?
- **Grupo 3:** Su modelo optimiza la distribución de suministros dados los recursos disponibles, pero en una emergencia real la información sobre demanda llega tarde, incompleta y a veces incorrecta. ¿En qué punto de su modelo asumió información perfecta que en la realidad no existiría, y cómo cambiaría su recomendación de distribución si esa información llegara con 6 horas de retraso?
- **Grupo 4:** Su modelo prioriza las intervenciones de reparación según su impacto sobre la accesibilidad, pero la accesibilidad no es el único criterio que un gobierno considera al asignar maquinaria y personal técnico. ¿Qué criterio no capturado en su modelo considera que debería pesar más en la decisión real, y cómo cambiaría el orden de prioridades de reparación si ese criterio se incorporara formalmente?
- **Grupo 5:** Su modelo asume que el personal se despliega donde más se necesita, pero en una emergencia real el personal también toma decisiones propias: va a donde cree que puede ayudar más, donde está su familia, o donde percibe menor riesgo personal. ¿Cómo cambiaría el comportamiento emergente de su modelo si los voluntarios tuvieran reglas de decisión individuales heterogéneas en lugar de seguir el plan de despliegue centralizado?
- **Grupo 6:** Su modelo captura cómo la población decide evacuar o quedarse, pero las decisiones individuales durante un desastre están fuertemente influenciadas por lo que la gente ve que hacen sus vecinos inmediatos. ¿Considera que el paradigma que eligió para modelar este sistema es el más adecuado para capturar ese efecto de contagio social, o hay algo en la naturaleza del fenómeno que su paradigma no puede representar sin importar qué parámetros use?
- **Grupo 7:** Su modelo produce una recomendación de asignación de recursos que maximiza alguna combinación de las métricas definidas, pero toda métrica es una simplificación de lo que realmente importa en una emergencia. ¿Qué dimensión del bienestar humano durante el desastre no está capturada en ninguna de las cuatro métricas de su archivo, y si esa dimensión se incorporara formalmente, qué decisión de asignación cambiaría y a favor de qué zona?

---

## Notas a Considerar

- El uso de IA generativa está permitido y esperado. Sin embargo, toda decisión de diseño debe estar justificada con los criterios vistos en clase. Una justificación que solo repite texto generado por IA sin razonamiento propio no obtendrá puntaje en ese criterio.
- El intercambio presencial es obligatorio. Un grupo que no tenga outputs listos para el intercambio afecta a los grupos receptores y eso se penaliza en la evaluación de ese grupo.
- Los datos de su archivo Excel son el punto de partida. Si el grupo considera que algún dato es inconsistente o incompleto, puede hacer supuestos adicionales siempre que los documente explícitamente en el reporte.
- Cada grupo trabaja con su perspectiva. No está permitido acceder al archivo Excel de otro grupo antes del intercambio presencial. Después del intercambio, cada grupo solo incorpora la información que recibió formalmente, no la que pueda haber visto en el archivo de otro grupo.

---

## Entregas en Canvas

1. Documento PDF con las respuestas a cada task.
2. En la entrega parcial se espera que entreguen lo señalado. En la entrega final deben entregar **TODOS LOS TASK**.
3. Archivo `.ipynb`, o link a repositorio de GitHub (**no se aceptan entregas en otros medios**).
   - El código debe estar comentado explicando la relación con las fórmulas de las diapositivas.

---

## Evaluación

| Componente | Peso |
|---|---|
| Justificación formal del paradigma | 15% |
| Calidad técnica del modelo (heterogeneidad, dinámica, incertidumbre) | 25% |
| Análisis de resultados y respuestas a las preguntas del grupo | 20% |
| Incorporación documentada del intercambio presencial | 15% |
| Video: claridad, profundidad y respuesta a la pregunta abierta | 15% |
| Limitaciones y propuestas de mejora | 10% |
