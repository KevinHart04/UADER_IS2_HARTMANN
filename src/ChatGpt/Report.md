# Memoria Técnica: Arquitectura y Aseguramiento de Calidad

**Proyecto:** Calculadora de Notación Polaca Inversa (RPN)
**Materia:** Ingeniería de Software II

---

## 1. Análisis de Métricas Estáticas (Multimetric)

Se ejecutó la herramienta de inspección `multimetric` sobre la iteración inicial (v1) y la versión refactorizada (v2) del código fuente para cuantificar el impacto de las modificaciones arquitectónicas.

### 1.1 Comparativa de Parámetros Evaluados

| Métrica Evaluada           | v1 (rpn.py)     | v2 (rpn_v2.py)  | Impacto / Variación                              |
| :------------------------- | :-------------- | :-------------- | :----------------------------------------------- |
| **Comment Ratio (%)**      | 4.37            | 62.32           | + 57.95% (Supera el umbral del 33%)              |
| **Cyclomatic Complexity**  | 36              | 29              | - 19.44% (Cumple la meta de reducción > 10%)     |
| **Halstead Effort**        | 464,550.55      | 412,865.91      | - 11.13% (Menor carga cognitiva)                 |
| **Halstead Time Required** | 25,808s (~7.1h) | 22,936s (~6.3h) | El código es un 11% más rápido de asimilar.      |
| **Halstead Bugprop**       | 2.011           | 2.047           | + 0.036 (Predicción acertada de ~2 bugs lógicos) |
| **Lines of Code (LOC)**    | 115             | 223             | + 93.91% (Aumento justificado por docstrings)    |

- **Proporción de Comentarios (`comment_ratio`):** Se incrementó del 4.37% al 62.32%. Este valor supera ampliamente el umbral exigido del 33%, logrado mediante la incorporación de docstrings formales en todos los componentes y la documentación de decisiones de diseño.
- **Esfuerzo y Tiempo (`halstead_effort` y `halstead_timerequired`):** El esfuerzo cognitivo calculado descendió un 11.13% (de 464,550.55 a 412,865.91), reduciendo el tiempo estimado de asimilación de ~7.1 a ~6.3 horas. En la práctica, esto se condice con la facilidad experimentada al trazar el flujo de ejecución tras la modularización.
- **Propensión a Defectos (`halstead_bugprop`):** La métrica estimó ~2.04 defectos. Empíricamente, la predicción fue certera, correspondiéndose con los desafíos lógicos resueltos durante el desarrollo (excepciones por dominios matemáticos inválidos y desbordamientos de pila).
- **Complejidad Ciclomática (`cyclomatic_complexity`):** Se redujo el índice de McCabe de 36 a 29, logrando una mejora del 19.44%, superando el objetivo del 10%.

### 1.2 Estrategias de Reducción de Complejidad y Resumen de Acciones

Para reducir la complejidad ciclomática, se implementó un patrón de diseño de despacho por diccionarios (Dictionary Dispatch Pattern), sustituyendo extensas cadenas `if/elif/else` por estructuras de evaluación de complejidad temporal O(1) (`_BASIC_OPS` y `_TRIG`). Las acciones de refactorización culminaron en un artefacto de mayor legibilidad, con delegación de responsabilidades en funciones de dominio específico.

---

## 2. Cobertura de Código (Coverage)

Se integró la librería `coverage` para auditar el alcance de las pruebas automatizadas sobre el código fuente. La ejecución del comando `coverage run -m unittest -v` seguida de `coverage report` arrojó un índice de cobertura de sentencias del **99%**. Este resultado supera holgadamente el requisito mínimo del 90% estipulado en la metodología, garantizando que la casi totalidad de las bifurcaciones lógicas están sometidas a control de calidad.

---

## 3. Pruebas Funcionales (Test Cases)

Se desarrolló una suite de pruebas (test_rpn.py) para asegurar el correcto funcionamiento del intérprete. Los casos de prueba documentados e implementados abarcan:

- **Operaciones Aritméticas Básicas:** Validación de suma, resta, multiplicación y división, incluyendo el manejo de números de punto flotante y enteros negativos.
- **Manejo de Errores (Excepciones):** Verificación de intercepción de fallos críticos, tales como división por cero, evaluación de logaritmos nulos/negativos, raíces cuadradas de números negativos y operaciones con pila insuficiente.
- **Comandos de Pila:** Auditoría del comportamiento mutacional de la estructura de datos principal mediante los comandos `dup`, `swap`, `drop` y `clear`.
- **Constantes y Funciones Avanzadas:** Validación de la inyección de constantes (Pi, Euler, Phi) y la precisión de funciones trigonométricas e inversas.
- **Gestión de Memoria:** Comprobación del almacenamiento persistente (STO) y recuperación (RCL) en los 10 registros disponibles (00-09).

---

## 4. Análisis Estático con Pylint

El código fue sometido a evaluación mediante el analizador estático Pylint, obteniendo una calificación inicial de **9.69/10**.

El reporte arrojó observaciones puntuales:

- **Convenciones Estéticas (C0303, C0304):** Presencia de espacios en blanco residuales y ausencia de salto de línea final. Su resolución fue delegada al formateador automático (Punto 5).
- **Diseño Lógico (R0912 - Too many branches):** Advertencia referida a la cantidad de ramificaciones en las funciones de evaluación matemática.
- **Justificación de Omisión:** Se tomó la decisión arquitectónica de ignorar esta advertencia (`# pylint: disable=too-many-branches`). El patrón de diseño implementado ofrece un balance óptimo entre legibilidad secuencial y modularidad. Abstrayendo aún más las operaciones procedimentales se incurriría en sobreingeniería, lo cual afectaría negativamente la asimilación directa del script sin aportar beneficios funcionales tangibles.

---

## 5. Estandarización y Linting (Black y Ruff)

Se estableció un entorno predecible y estandarizado mediante la creación del archivo de configuración `pyproject.toml`.

- `line-length = 88`: Amplía el límite histórico de PEP8 (79) para mejorar la distribución horizontal en pantallas modernas.
- `target-version = ["py311"]`: Habilita heurísticas específicas para la versión 3.11 de Python.
- `select = ["E", "F", "I", "B", "UP"]`: Activa reglas de validación estilística, detección de variables/importaciones huérfanas, ordenamiento sistemático, prevención de vulnerabilidades lógicas y sugerencias de sintaxis moderna.

La ejecución del formateador `black` resolvió de forma transparente las anomalías estéticas previas. Posteriormente, la ejecución de `ruff check` culminó con el mensaje "All checks passed", certificando la ausencia de defectos sintácticos y de diseño.

---

## 6. Sugerencias de Modificación (Interacción IA)

Durante la fase de consultoría técnica, el motor conversacional sugirió implementar paradigmas de Programación Orientada a Objetos (OOP) para encapsular la memoria global, así como la integración de tipado estático estricto (Type Hinting) en las firmas de los métodos para facilitar la inspección estática.

**Decisión Técnica:**
Se determinó desestimar la implementación de estas modificaciones. La justificación de esta decisión radica en el alto grado de madurez del artefacto actual. Habiendo alcanzado una cobertura de código del 99%, un índice de mantenibilidad superior y habiendo superado sin observaciones las auditorías restrictivas conjuntas de Ruff y Black, el código demuestra ser robusto, predecible y completamente funcional según las especificaciones. Alterar el paradigma procedimental a esta escala constituiría un esfuerzo estructural que no agregaría valor operativo directo a la solución ya estabilizada.
