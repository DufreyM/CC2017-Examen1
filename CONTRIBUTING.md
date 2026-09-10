# Guía de colaboración

Este repositorio debe reflejar aportes reales y revisables de cada integrante.
Cada persona configura su propia identidad de Git y realiza los commits del
trabajo que efectivamente desarrolló o revisó.

## Preparación personal

```powershell
git config user.name "Nombre Apellido"
git config user.email "correo@ejemplo.com"
git switch -c tipo/descripcion-corta
```

Usen ramas pequeñas y nombres como `modelo/ajuste-asistencia`,
`analisis/sensibilidad`, `reporte/limitaciones` o `qa/verificacion-outputs`.

## Reparto sugerido

| Frente | Ejemplos de aportes verificables |
|---|---|
| Modelo | Reglas ABM, supuestos, calibración y sensibilidad |
| Análisis | Monte Carlo, intervalos de confianza, gráficas y outputs |
| Reporte | ODD, interpretación, limitaciones e intercambio presencial |
| Calidad | Pruebas, reproducibilidad, revisión de rutas y entrega final |

El reparto es orientativo: documenten en el mensaje del commit qué cambió y
por qué. Si dos personas trabajaron realmente en el mismo cambio, pueden usar
un tráiler `Co-authored-by`; no lo agreguen solo para repartir autoría.

## Convención de commits

```text
modelo: ajusta la probabilidad de asistencia por zona
analisis: compara los escenarios de desinformacion
docs: incorpora conclusiones del intercambio presencial
test: valida los limites de las trayectorias
```

Antes de integrar una rama:

```powershell
python -m unittest discover -s tests -v
python scripts/build_notebook.py
python -m nbconvert --execute --to notebook --inplace --ExecutePreprocessor.timeout=900 notebooks/grupo6_modelo.ipynb
```

No reescriban commits ajenos ya compartidos. Integren mediante pull request o
una revisión presencial y conserven en el historial quién realizó cada aporte.
