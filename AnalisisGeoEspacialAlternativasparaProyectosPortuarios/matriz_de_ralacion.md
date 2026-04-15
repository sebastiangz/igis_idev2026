# PROPUESTA DE MATRIZ DE RELACIÓN PARA EVALUACIÓN COMPARATIVA DE ALTERNATIVAS

Proyecto: Desarrollo del Puerto Nuevo Manzanillo, Vaso II Laguna Cuyutlán

Superficie Requerida: 311 hectáreas

## 1. INTRODUCCIÓN

En cumplimiento a lo señalado en la observación sobre la evaluación comparativa de alternativas, se presenta la metodología de evaluación multi-criterio utilizando algoritmos genéticos, Google Earth Engine (GEE) y QGIS para analizar al menos 3 sitios alternativos para la construcción del proyecto, incluyendo:

- • Alternativa 0: No construcción (línea base)

- • Alternativa 1: Vaso II de la Laguna Cuyutlán (propuesta actual en MIA)

- • Alternativas 2-4: Variantes de ubicación y diseño

## 2. METODOLOGÍA DE EVALUACIÓN MULTI-CRITERIO

La evaluación se basa en una integración de metodologías avanzadas:

### 2.1 Algoritmos Genéticos (NSGA-II)

Se implementa el algoritmo NSGA-II (Non-dominated Sorting Genetic Algorithm II) para optimización multi-objetivo, que permite:

- • Explorar el espacio de soluciones de forma eficiente

- • Identificar el frente de Pareto con soluciones óptimas

- • Considerar simultáneamente objetivos conflictivos

### 2.2 Google Earth Engine (GEE)

Utilizado para análisis geoespacial de gran escala:

- • Análisis de cobertura de manglar (Hansen Global Mangrove)

- • Evaluación de batimetría (GEBCO)

- • Modelado de hidrodinámica costera

- • Análisis de cambios temporales en el sistema lagunar

### 2.3 Método PROMETHEE II

Para el ranking final de alternativas se utiliza PROMETHEE II (Preference Ranking Organization Method for Enrichment Evaluations), que considera preferencias difusas entre alternativas y genera un ranking robusto basado en flujos de preferencia.

## 3. ESTRUCTURA DE CRITERIOS DE EVALUACIÓN

La matriz de relación se estructura en 4 categorías principales con 16 criterios específicos, cada uno con su peso relativo en la evaluación global:

| ID | Criterio | Categoría | Peso (%) | Unidad | Tipo |
| --- | --- | --- | --- | --- | --- |
| AMB-01 | Alteración Hidrodinámica | Ambiental | 15.0 | Índice [0-10] | Minimizar |
| AMB-02 | Calidad del Agua | Ambiental | 10.0 | Índice [0-10] | Minimizar |
| AMB-03 | Impacto en Biodiversidad | Ambiental | 10.0 | Especies afectadas | Minimizar |
| AMB-04 | Superficie de Manglar Afectada | Ambiental | 15.0 | Hectáreas | Minimizar |
| AMB-05 | Generación de Residuos y Emisiones | Ambiental | 5.0 | Toneladas/año | Minimizar |
| AMB-06 | Riesgo de Inundación/Erosión | Ambiental | 5.0 | Índice [0-10] | Minimizar |
|  | SUBTOTAL AMBIENTAL | 60.0% |  |
| TEC-01 | Viabilidad Constructiva | Técnico | 10.0 | Índice [0-10] | Maximizar |
| TEC-02 | Volumen de Dragado Requerido | Técnico | 10.0 | Millones m³ | Minimizar |
| TEC-03 | Accesibilidad y Conectividad | Técnico | 5.0 | Índice [0-10] | Maximizar |
| TEC-04 | Distancia a Infraestructura Existente | Técnico | 5.0 | Kilómetros | Minimizar |
|  | SUBTOTAL TÉCNICO | 30.0% |  |

## 3. ESTRUCTURA DE CRITERIOS (continuación)

| ID | Criterio | Categoría | Peso (%) | Unidad | Tipo |
| --- | --- | --- | --- | --- | --- |
| SOC-01 | Impacto en Comunidades Locales | Social | 7.0 | Índice [0-10] | Minimizar |
| SOC-02 | Generación de Empleo | Social | 5.0 | Empleos directos | Maximizar |
| SOC-03 | Afectación a Actividades Pesqueras | Social | 3.0 | Índice [0-10] | Minimizar |
|  | SUBTOTAL SOCIAL | 15.0% |  |
| ECO-01 | Costo de Construcción | Económico | 7.0 | Millones USD | Minimizar |
| ECO-02 | Costo de Operación y Mantenimiento | Económico | 5.0 | Millones USD/año | Minimizar |
| ECO-03 | Retorno de Inversión | Económico | 3.0 | Años | Minimizar |
|  | SUBTOTAL ECONÓMICO | 15.0% |  |
|  | TOTAL | 100.0% |  |

## 4. ALTERNATIVAS EVALUADAS

Se proponen las siguientes alternativas para evaluación comparativa:

### Alternativa 0 - No Construcción

Escenario base sin proyecto. Mantener el estado actual del sistema lagunar sin realizar ninguna obra de construcción. Esta alternativa sirve como línea base para comparación.

### Alternativa 1 - Vaso II Laguna Cuyutlán (Propuesta MIA Actual)

Proyecto propuesto en la MIA original. Construcción del Puerto Nuevo Manzanillo en el Vaso II de la laguna, con las características y diseño presentados en la manifestación de impacto ambiental.

### Alternativa 2 - Zona Norte Vaso II

Variante de ubicación en la zona norte del Vaso II, diseñada para minimizar el impacto directo sobre áreas de manglar mejor conservadas. Requiere ajustes en el diseño de accesos y dragado.

### Alternativa 3 - Zona Costera Adyacente

Construcción en zona costera externa al sistema lagunar. Requiere mayor volumen de dragado pero evita impactos directos en el ecosistema lagunar. Mayor exposición a oleaje y condiciones marinas.

### Alternativa 4 - Zona Sur Sistema Lagunar

Ubicación al sur del sistema lagunar, aprovechando mayor profundidad natural que reduce el volumen de dragado requerido. Requiere extensión de infraestructura de acceso terrestre.

## 5. METODOLOGÍA DETALLADA DE EVALUACIÓN

### 5.1 Fase 1: Evaluación de Criterios por Alternativa

Para cada alternativa, se evalúan los 16 criterios definidos mediante:

- • Análisis espacial con Google Earth Engine para criterios ambientales

- • Modelado hidrodinámico para alteración de corrientes y calidad de agua

- • Análisis de superposición con capas de manglar, biodiversidad y hábitats críticos

- • Cálculo de volúmenes de dragado basado en batimetría GEBCO

- • Evaluación técnica y económica basada en ingeniería de detalle

- • Análisis de proximidad a comunidades y zonas de pesca

### 5.2 Fase 2: Normalización de Scores

Los valores de cada criterio se normalizan a escala [0-1] mediante:

- • Para criterios a minimizar: score = (max - valor) / (max - min)

- • Para criterios a maximizar: score = (valor - min) / (max - min)

Donde max y min son los valores máximo y mínimo observados entre todas las alternativas para ese criterio.

### 5.3 Fase 3: Ponderación y Score Total

El score total ponderado para cada alternativa se calcula como:

Score_Total = Σ (peso_i × score_normalizado_i)

Donde i representa cada uno de los 16 criterios.

### 5.4 Fase 4: Ranking PROMETHEE II

Se aplica el método PROMETHEE II para obtener un ranking robusto considerando:

- • Flujo positivo Φ⁺(a): preferencia agregada de la alternativa 'a' sobre las demás

- • Flujo negativo Φ⁻(a): preferencia agregada de las demás sobre 'a'

- • Flujo neto Φ(a) = Φ⁺(a) - Φ⁻(a): indicador final de preferencia

El ranking final ordena las alternativas de mayor a menor flujo neto, identificando objetivamente la alternativa más viable desde la perspectiva de sustentabilidad.

## 6. PRODUCTOS ENTREGABLES

La evaluación comparativa generará los siguientes productos:

### 6.1 Tablas Comparativas

- • Matriz de evaluación con valores de todos los criterios para cada alternativa

- • Tabla de scores normalizados [0-1]

- • Ranking PROMETHEE II con flujos de preferencia

- • Resumen por categoría (Ambiental, Técnico, Social, Económico)

### 6.2 Mapas Comparativos

- • Mapa de ubicación de todas las alternativas

- • Mapas de afectación de manglar por alternativa

- • Mapas de batimetría y volúmenes de dragado

- • Mapas de proximidad a comunidades y zonas de pesca

- • Mapa integrado con score ponderado por alternativa

### 6.3 Visualizaciones Interactivas

- • Gráficos de radar comparando scores por categoría

- • Gráficos de barras con ranking de alternativas

- • Visualización 3D del frente de Pareto

- • Mapas interactivos HTML con capas de Google Earth Engine

### 6.4 Informe Técnico

- • Justificación documentada de la selección de la alternativa propuesta

- • Análisis de trade-offs entre criterios ambientales, técnicos, sociales y económicos

- • Análisis de sensibilidad a variaciones en los pesos de los criterios

- • Conclusiones y recomendaciones

## 7. VENTAJAS DE LA METODOLOGÍA PROPUESTA

La metodología integrada de algoritmos genéticos, Google Earth Engine y análisis multi-criterio ofrece:

- • Objetividad: Evaluación cuantitativa basada en datos geoespaciales verificables

- • Transparencia: Todos los criterios, pesos y cálculos están claramente documentados

- • Reproducibilidad: Los resultados pueden ser verificados y reproducidos por terceros

- • Integralidad: Considera simultáneamente aspectos ambientales, técnicos, sociales y económicos

- • Escalabilidad: Permite incorporar criterios adicionales o modificar pesos según necesidades

- • Robustez: El método PROMETHEE II genera rankings estables ante pequeñas variaciones en los datos

## 8. CONCLUSIÓN

La presente propuesta de matriz de relación para evaluación comparativa de alternativas cumple con los requisitos establecidos en la observación, proporcionando:

- 1. Evaluación de al menos 3 sitios alternativos además de la alternativa cero

- 2. Criterios ambientales que valoran hidrodinámica, calidad de agua, biodiversidad, manglar, residuos/emisiones y riesgo de inundación/erosión

- 3. Criterios técnicos, sociales y económicos complementarios

- 4. Justificación clara y documentada de la selección de la alternativa propuesta

- 5. Tablas y mapas comparativos para identificación objetiva de la alternativa más viable

La metodología propuesta garantiza una evaluación rigurosa, transparente y científicamente fundamentada que permitirá la toma de decisiones informada en materia de sustentabilidad del proyecto.
