# Grupo 6, CC2017 Examen Práctico

## Archivos
- `data/Grupo6_ComportamientoPoblacional.xlsx`: archivo oficial del
  catedrático (hoja `Datos_Grupo6`: demografía, parámetros de
  comportamiento, redes sociales por zona, vulnerabilidad). El modelo lo
  lee directamente al importar `grupo6_model.py`.
- `grupo6_model.py`: lógica del modelo ABM. Carga todos los parámetros
  desde el Excel oficial (`cargar_datos_excel()`). El único dato que el
  Excel no trae es la población absoluta por zona, así que se asume
  reparto igualitario (`POBLACION_ZONA`, 50,000 por zona), documentado
  explícitamente en el reporte.
- `build_notebook.py`: genera `grupo6_modelo.ipynb` desde cero, por si hay
  que regenerarlo tras editar celdas.
- `grupo6_modelo.ipynb`: notebook principal, con carga de datos, ODD,
  Monte Carlo (30 realizaciones por escenario), respuestas a las 3
  preguntas del grupo, y los 3 outputs formales para Grupo 1. Este es el
  entregable de código.
- `reporte_grupo6.md`: borrador del reporte técnico (máximo 8 páginas al
  pasarlo a PDF), con los resultados de la corrida actual.
- `guion_video.md`: guion de apoyo para el video de 3 a 5 minutos.
- `data/output_a_flujo_desplazados.csv`: output a, proyección de flujo de
  desplazados por zona y bloque, con destino (refugio oficial u otra
  zona).
- `data/output_b_atrapados_sin_asistencia.csv`: output b, personas que no
  pueden evacuar sin asistencia en Z1 y Z5, por bloque.
- `data/output_c_rutas_preferidas.csv`: output c, mapa de rutas preferidas
  por comportamiento (destino real contra refugio oficial).

## Si llega un dato adicional (población por zona, plan de Grupo 5, etc)
1. Si es población por zona, editar `POBLACION_ZONA` en `grupo6_model.py`.
   Si es otro parámetro que reemplaza una función completa, por ejemplo la
   capacidad de rescate de Grupo 5 en vez de la aproximación vía
   `índice_riesgo_rezago`, editar `prob_asistencia()`.
2. Volver a correr todo el notebook:
   `python -c "import nbformat; from nbconvert.preprocessors import ExecutePreprocessor; nb=nbformat.read('grupo6_modelo.ipynb', as_version=4); ExecutePreprocessor(timeout=300).preprocess(nb, {'metadata':{'path':'.'}}); nbformat.write(nb,'grupo6_modelo.ipynb')"`
3. Actualizar los números citados en `reporte_grupo6.md` y `guion_video.md`
   (la estructura de ambos no cambia, solo las cifras).

## Pendiente de confirmar con el catedrático o en el intercambio
- Según la tabla de dependencias del examen, Grupo 6 no recibe insumos
  formales de ningún otro grupo, solo entrega a Grupo 1. Confirmar el día
  del intercambio presencial y documentar en la sección 4 del reporte si
  en la práctica sí llega algo informal.
- El Excel de Grupo 6 no trae población absoluta por zona. Si algún otro
  grupo, por ejemplo Grupo 1, sí la tiene, conseguirla y actualizar el
  modelo.

## Requisitos
`numpy`, `scipy`, `pandas`, `matplotlib`, `networkx`, `openpyxl`,
`nbformat`, `nbconvert`, `ipykernel`, todos ya usados y validados en este
entorno.
