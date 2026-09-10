# Comportamiento poblacional ante un terremoto

Proyecto del **Grupo 6** para el Examen Práctico de CC2017 — Modelación y
Simulación. Implementa un modelo basado en agentes (ABM) para estudiar cómo la
vulnerabilidad, las redes sociales y la desinformación afectan la evacuación de
250,000 habitantes durante las primeras 72 horas posteriores al evento.

## Entregables principales

- [Notebook ejecutable](notebooks/grupo6_modelo.ipynb): modelo, Monte Carlo,
  intervalos de confianza, análisis y respuestas a las tres preguntas.
- [Reporte técnico en PDF](reports/reporte_grupo6.pdf) y
  [fuente Markdown](reports/reporte_grupo6.md).
- [Outputs para el Grupo 1](data/processed/): flujo de desplazados, población
  sin asistencia y rutas preferidas.
- [Enunciado del examen](docs/enunciado_examen.md).

## Estructura

```text
.
├── data/
│   ├── raw/          # Excel oficial, sin modificaciones
│   └── processed/    # CSV generados por el notebook
├── docs/             # Enunciado y registro requerido de uso de IA
├── notebooks/        # Análisis principal y resultados visibles
├── reports/          # Reporte técnico en Markdown y PDF
├── scripts/          # Construcción del notebook y conversión del reporte
├── src/               # Lógica reutilizable del modelo ABM
├── tests/             # Pruebas de integridad y comportamiento básico
├── CONTRIBUTING.md    # Flujo de trabajo grupal y convención de commits
└── requirements.txt  # Dependencias de Python
```

## Inicio rápido

Se recomienda Python 3.11 o posterior. Desde la raíz del repositorio, en
PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Para reconstruir y ejecutar el notebook completo:

```powershell
python scripts/build_notebook.py
python -m nbconvert --execute --to notebook --inplace --ExecutePreprocessor.timeout=900 notebooks/grupo6_modelo.ipynb
```

La ejecución actualiza automáticamente los tres CSV de `data/processed/`.
Para regenerar el reporte PDF después de editar su fuente:

```powershell
python scripts/convertir_a_pdf.py reports/reporte_grupo6.md reports/reporte_grupo6.pdf
```

## Diseño del modelo

El ABM representa 2,000 agentes por zona y escala sus resultados a la población
total. Conserva la heterogeneidad de las cinco zonas, propaga información sobre
una red social explícita y simula 12 bloques de seis horas. Cada escenario usa
30 realizaciones y reporta la media con un intervalo de confianza bootstrap del
95 %.

Todos los parámetros provienen de la hoja `Datos_Grupo6` del Excel oficial. La
única excepción es la población absoluta por zona: como el archivo solo indica
250,000 habitantes en total, se documenta el supuesto provisional de 50,000 por
zona en `src/grupo6_model.py`.

## Datos y reproducibilidad

- `data/raw/` se considera de solo lectura; no se debe editar el Excel oficial.
- `data/processed/` contiene resultados derivados y puede regenerarse.
- `scripts/build_notebook.py` es la fuente estructural del notebook. Si cambia
  una celda permanente, el cambio debe hacerse allí y luego reconstruirse.
- Las semillas se fijan en el notebook para que los resultados sean repetibles.

Si el intercambio presencial aporta población por zona u otro parámetro, se
actualiza el supuesto correspondiente, se ejecutan las pruebas y se regenera el
notebook antes de modificar las cifras del reporte.

## Trabajo en equipo

La [guía de colaboración](CONTRIBUTING.md) propone frentes de trabajo, ramas y
mensajes de commit. Cada integrante debe usar su identidad real de Git y hacer
commits del trabajo que efectivamente realizó o revisó. El
[registro de uso de IA](docs/registro_uso_ia.md) debe completarse antes de la
entrega, como exige el enunciado.
