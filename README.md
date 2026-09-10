# Comportamiento poblacional ante un terremoto

Proyecto del **Grupo 6** para el Examen Práctico de CC2017 — Modelación y
Simulación. Implementa un modelo basado en agentes (ABM) para estudiar cómo la
vulnerabilidad, las redes sociales y la desinformación afectan la evacuación de
250,000 habitantes durante las primeras 72 horas posteriores al evento.

## Entregables principales

- [Informe final](reports/Examen%20Practico%201.pdf)
- [Notebook ejecutable](notebooks/grupo6_modelo.ipynb): modelo, Monte Carlo,
  intervalos de confianza, análisis y respuestas a las tres preguntas.
- [Outputs para el Grupo 1](data/processed/): flujo de desplazados, población
  sin asistencia y rutas preferidas.

## Estructura

```text
.
├── data/
│   ├── raw/          # Excel oficial, sin modificaciones
│   └── processed/    # CSV generados por el notebook
├── notebooks/        # Análisis principal y resultados visibles
├── reports/          # Informe final, PDF y figuras exportadas
├── src/               # Lógica reutilizable del modelo ABM
├── S10_Examen_Practico.md  # Enunciado del examen
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
python -m nbconvert --execute --to notebook --inplace --ExecutePreprocessor.timeout=900 notebooks/grupo6_modelo.ipynb
```

La ejecución actualiza automáticamente los tres CSV de `data/processed/` y las
figuras de `reports/figures/`.

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
- `src/grupo6_model.py` contiene la lógica reutilizable y el notebook contiene
  el flujo de análisis, las simulaciones y la exportación de resultados.
- Las semillas se fijan en el notebook para que los resultados sean repetibles.


