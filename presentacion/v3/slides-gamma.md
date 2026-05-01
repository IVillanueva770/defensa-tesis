# Slides para Gamma — Defensa de tesis

Prompt listo para pegar en Gamma por lotes. **Lote 1**: S2 a S11 (Gamma genera hasta 10 por vez). **Lote 2 en adelante**: generar de a una desde S12.

Donde aparezca `[PLACEHOLDER: GIF ...]` o `[PLACEHOLDER: FIGURA ...]`, dejar un cuadro vacío del tamaño indicado; el asset se inserta manualmente después.

---

## Lote 1 — slides 1 a 11

### S1 — Portada

- **Título**: Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora
- **Subtítulo**: Proyecto Final de Grado · UCASAL · 2026
- **Autor**: Ignacio Villanueva
- **Tutora**: Mg. Lic. Lorena Talamé
- **Facultad**: Ingeniería e Informática — Ingeniería en Informática
- **Visual**: logo UCASAL a la izquierda; a la derecha, ilustración temática — persona haciendo press de hombro con barra.
- **Layout**: título grande izquierda, ilustración derecha (~40 % ancho).

### S2 — Agenda

- **Pill**: `AGENDA`
- **Título (H1)**: Agenda
- **Contenido**: 5 ítems numerados verticalmente, cada uno con su número en amarillo grande:
  1. La pregunta
  2. El sistema
  3. El recorrido experimental
  4. Resultados
  5. Hacia dónde sigue
- **Visual**: línea vertical amarilla a la izquierda conectando los 5 números; sin otras imágenes.
- **Layout**: lista centrada vertical, mucho aire alrededor.

### S3 — La pregunta

- **Pill**: `MOTIVACIÓN`
- **Título (H1)**: La pregunta que abrió el proyecto
- **Frase central (grande, blanco)**:
  > *¿Puede una cámara común evaluar la técnica de un ejercicio de forma automática, objetiva y accesible?*
- **Subtítulo debajo (gris tenue)**: "El punto de partida fue una conversación con el Instituto de Rehabilitación de UCASAL."
- **Visual**: `[PLACEHOLDER: GIF persona haciendo press de hombro con skeleton de keypoints superpuesto — 560×400 px aprox, a la derecha]`
- **Layout**: 2 columnas — texto izquierda (55 %), placeholder derecha (45 %).

### S4 — Por qué importa

- **Pill**: `MOTIVACIÓN`
- **Título (H1)**: Entrenar sin guía correcta es un problema real
- **Contenido**: 3 cards horizontales, cada una con ícono arriba + 1 frase corta:
  1. **Lesiones** — La mala técnica es la primera causa de lesiones en entrenamiento sin supervisión.
  2. **Supervisión humana** — El criterio de un entrenador es subjetivo y no escala a miles de practicantes.
  3. **Sistemas objetivos** — Los que existen hoy requieren laboratorios costosos.
- **Visual**: iconos minimalistas monocromo amarillo (pesa, ojo, laboratorio).
- **Layout**: 3 columnas iguales, cards con borde izquierdo amarillo.

### S5 — Las alternativas existentes

- **Pill**: `ESTUDIO INICIAL`
- **Título (H1)**: Las alternativas existentes son inaccesibles
- **Contenido (tabla)**:

  | Sistema | Tecnología | Costo |
  |---------|-----------|-------|
  | VICON / OptiTrack | Captura 3D con marcadores | USD $10k–$100k+ |
  | Physimax / Kaia Health | IA comercial, SaaS | USD $50–$200/mes |
  | Tempo / Mirror | Hardware dedicado + suscripción | USD $1.500 + $39/mes |
  | **Este proyecto** | **Video RGB estándar + open-source** | **$0** |

- **Subtítulo abajo (gris)**: "El objetivo: una alternativa accesible con utilidad clínica."
- **Visual**: la última fila destacada con fondo amarillo translúcido y texto negro bold.
- **Layout**: tabla centrada ocupando ~60 %, título arriba.

### S6 — Objetivos y alcance

- **Pill**: `OBJETIVOS Y ALCANCE`
- **Título (H1)**: Qué me comprometí a resolver
- **Contenido**: 2 columnas.

  **Columna izquierda — Objetivo general**:
  > Desarrollar un modelo de clasificación de técnica en el ejercicio de **press de hombro**, capaz de identificar y categorizar errores de ejecución desde video.

  **Columna derecha — Objetivos específicos** (4 bullets numerados):
  1. Conformar un conjunto de videos de entrenamiento.
  2. Construir el pipeline de extracción de información biomecánica.
  3. Entrenar y optimizar iterativamente el modelo.
  4. Evaluar el desempeño con métricas estándar y protocolos de validación.

- **Línea de alcance abajo (ancho completo, gris)**: "Alcance: un ejercicio (press de hombro), 3 categorías de técnica, dataset Fitness-AQA (2.135 videos). Entregable: pipeline completo + modelo entrenado."
- **Visual**: ninguno. Slide de texto limpio.
- **Layout**: 2 columnas arriba (50/50), línea de alcance de ancho completo abajo.

### S7 — El pipeline en una imagen

- **Pill**: `ARQUITECTURA`
- **Título (H1)**: El pipeline, en una sola imagen
- **Contenido**: **ninguno** — la imagen habla.
- **Visual**: diagrama horizontal de 4 nodos conectados con flechas amarillas, a pantalla completa:
  `[Video de entrada] → [ViTPose] → [Keypoints JSON] → [PoseConv3D] → [Clasificación: 3 clases]`
  Cada nodo es una card redondeada con etiqueta amarilla y una línea descriptiva mínima.
- **Layout**: diagrama centrado vertical, con mucho aire alrededor.

### S8 — ¿Por qué ViTPose?

- **Pill**: `ARQUITECTURA · ETAPA 1`
- **Título (H1)**: ¿Por qué ViTPose?
- **Frase central (grande, amarillo, serif bold)**:
  > *ViTPose entiende el cuerpo como un todo, no como suma de partes.*
- **Contenido (2 columnas pequeñas debajo)**:
  - **Enfoques tradicionales (OpenPose, MediaPipe)**: analizan la imagen por partes locales, luego ensamblan.
  - **ViTPose**: ve todas las articulaciones simultáneamente usando Vision Transformers.
- **Visual**: `[PLACEHOLDER: FIGURA arquitectura Vision Transformer — parches de imagen + embedding + encoder — ~400×300 px, a la derecha]`
- **Layout**: frase central arriba (40 %), 2 columnas comparativas abajo (40 %), visual derecha (20 %).

### S9 — ¿Por qué PoseConv3D?

- **Pill**: `ARQUITECTURA · ETAPA 2`
- **Título (H1)**: ¿Por qué PoseConv3D?
- **Frase central**:
  > *Convierte los keypoints en un volumen espacio-temporal, y aplica convoluciones 3D sobre él.*
- **Contenido (2 bullets)**:
  - **Entrada**: 48 frames × 17 keypoints, apilados como heatmaps gaussianos.
  - **Backbone**: ResNet3D SlowOnly (12 M parámetros), preentrenado en NTU60.
- **Visual**: `[PLACEHOLDER: FIGURA volumen 3D con eje temporal — cubo de heatmaps apilados, ~400×300 px, a la derecha]`
- **Layout**: texto izquierda (50 %), visual derecha (50 %).

### S10 — El problema del tracking

- **Pill**: `CONTRIBUCIÓN TÉCNICA`
- **Título (H1)**: ViTPose no tiene memoria entre frames
- **Frase central grande**:
  > *Una persona con ID "44" puede desaparecer 2 frames y reaparecer como "51". El modelo ve 3 personas donde hay 1.*
- **Visual**: `[PLACEHOLDER: GIF o tira de 5 frames mostrando bounding boxes con IDs cambiando entre frames — 900×300 px, horizontal abajo del texto]`. Los IDs en colores distintos para hacer obvio el salto.
- **Layout**: frase arriba (30 %), tira de frames abajo (70 %).

### S11 — El algoritmo de corrección

- **Pill**: `CONTRIBUCIÓN TÉCNICA`
- **Título (H1)**: El algoritmo de corrección
- **Contenido**: regla destacada en recuadro central:
  > **Si desaparece ≤ 3 frames y reaparece a ≤ 25 píxeles, se mantiene el ID original.**
- **3 pasos visuales en fila abajo** (iconos circulares amarillos):
  1. Detectar discontinuidad
  2. Verificar condiciones (distancia euclidiana entre poses)
  3. Reasignar ID
- **Cifra destacada a la derecha (grande, amarillo)**: **87 %** de discontinuidades corregidas
- **Layout**: regla arriba, 3 pasos al medio, cifra derecha alineada con los pasos.

> **Cierre del Lote 1**

---

## Lote 2 en adelante — slides 12 a 23 (generar 1×1)

### S12 — Tres preguntas, tres experimentos

- **Pill**: `LÓGICA EXPERIMENTAL`
- **Título (H1)**: Tres preguntas, tres experimentos
- **Subtítulo arriba (gris)**: "El desarrollo no fue lineal. Cada experimento respondió una pregunta distinta."
- **Contenido**: 3 columnas en forma de flecha, cada una con una pregunta e ícono arriba:
  1. ¿Aprende **sin conocimiento previo**? (ícono: signo de interrogación)
  2. ¿Ayuda el **conocimiento preentrenado**? (ícono: cerebro)
  3. ¿Era el **modelo** o eran los **datos**? (ícono: base de datos)
- **Layout**: 3 columnas de flechas, iguales.

### S13 — Experimento 1: el fracaso instructivo

- **Pill**: `EXPERIMENTO 1 · BASELINE`
- **Título (H1)**: 51.2 %
- **Cifra gigante**: `51.2 %` amarillo, centro superior, tamaño masivo.
- **Subtítulo (naranja)**: *overfitting severo*
- **Contenido (2 bullets)**:
  - ResNet3D entrenado desde cero, sin transfer learning.
  - F1 = 0.48 · Pérdida de validación ~1.5.
- **Visual**: `[PLACEHOLDER: FIGURA curva de pérdida del experimento base — train vs. val divergentes, ~500×350 px, a la derecha]`
- **Frase de cierre (abajo, bold)**: "El modelo memoriza, no generaliza."
- **Layout**: cifra + texto izquierda (50 %), gráfico derecha (50 %).

### S14 — Experimento 2: transfer learning ayuda

- **Pill**: `EXPERIMENTO 2 · TRANSFER LEARNING`
- **Título (H1)**: 70.5 %
- **Cifra gigante**: `70.5 %` amarillo, centro superior.
- **Subtítulo (naranja)**: *+19.3 pp sobre baseline*
- **Contenido (2 bullets)**:
  - Pesos preentrenados en NTU60 (56.880 videos de acciones humanas).
  - F1 = 0.69 · Brecha train/val aún del ~25 %.
- **Visual**: `[PLACEHOLDER: FIGURA curva de pérdida con transfer learning — brecha más chica pero presente, ~500×350 px, a la derecha]`
- **Frase de cierre**: "Ya no era el conocimiento previo. Algo más seguía fallando."
- **Layout**: idéntico a S13 para crear ritmo narrativo.

### S15 — Experimento 3: el problema eran los datos

- **Pill**: `EXPERIMENTO 3 · CONFIGURACIÓN FINAL`
- **Título (H1)**: 91.6 %
- **Cifra gigante**: `91.6 %` amarillo, aún más grande que las anteriores.
- **Subtítulo grande (naranja, bold)**: **El salto no vino de un modelo más grande. Vino de entender los datos.**
- **Contenido (tabla condensada de 4 cambios)**:

  | Cambio | Qué resolvió |
  |--------|--------------|
  | **Dataset con tracking corregido** | El modelo veía 5–10 "personas" donde había 1 |
  | AdamW en lugar de SGD | Convergencia adaptativa por parámetro |
  | Pose Jittering (σ=2 px) | Robustez ante imprecisiones de ViTPose |
  | Label smoothing (ε=0.1) | Previene sobreconfianza |

  Primera fila destacada con fondo amarillo translúcido; las otras en gris tenue.
- **Visual**: `[PLACEHOLDER: FIGURA curva de precisión de configuración final — train y val convergentes con brecha mínima, ~450×300 px, a la derecha]`
- **Layout**: cifra arriba (25 %), tabla izquierda (40 %) + gráfico derecha (35 %).

### S16 — Un número lo resume

- **Pill**: `RESULTADOS`
- **Título (H1)**: Un número lo resume
- **Cifra gigante centrada**: **91.6 %** precisión · **0.91** F1-macro
- **Subtítulo debajo (gris)**: "Evaluado sobre 427 videos de validación del dataset Fitness-AQA."
- **Visual**: ninguno. Pantalla minimalista. Impacto por simplicidad.
- **Layout**: todo centrado, mucho aire.

### S17 — Desglose por clase y matriz de confusión

- **Pill**: `RESULTADOS · POR CLASE`
- **Título (H1)**: El modelo es parejo en las tres categorías
- **Contenido (tabla izquierda)**:

  | Clase | Precision | Recall | F1 | N |
  |-------|-----------|--------|----|----|
  | Técnica correcta | 0.94 | 0.92 | 0.93 | 180 |
  | Error de codos | 0.90 | 0.92 | 0.91 | 130 |
  | Error de rodillas | 0.89 | 0.91 | 0.90 | 117 |
  | **Macro avg** | **0.91** | **0.92** | **0.91** | 427 |

- **Visual**: `[PLACEHOLDER: FIGURA matriz de confusión — 3×3 con diagonal dominante (166/119/106) y errores simétricos en las celdas fuera de diagonal, ~420×420 px, a la derecha]`
- **Bullets de lectura (abajo)**:
  - Diagonal alta → clasificación correcta en la mayoría de los casos.
  - Pocos errores cruzados entre clases.
  - F1 parejo → sin sesgo a la clase mayoritaria.
- **Layout**: tabla 45 % izquierda, matriz 45 % derecha, bullets 10 % abajo.

### S18 — Comparación académica

- **Pill**: `ANÁLISIS COMPARATIVO`
- **Título (H1)**: Mejor que el trabajo de referencia en ambas categorías
- **Contenido (tabla)**:

  | Métrica | Parmar et al. (2022) | **Este trabajo** |
  |---------|---------------------|-----------------|
  | Estrategia | 2 clasificadores binarios | **1 clasificador multiclase** |
  | F1 — Codos | 0.45 | **0.91** |
  | F1 — Rodillas | 0.84 | **0.90** |
  | F1 — Global | — | **0.91** |

- **Frase clave abajo (naranja bold)**: "Un clasificador unificado supera a dos especializados. Codos: +0.46 puntos."
- **Visual**: sin gráfico adicional. Números de la columna derecha en naranja grande.
- **Layout**: tabla centrada, ocupa 70 %.

### S19 — Demo

- **Pill**: `DEMO`
- **Título (H1)**: El sistema en acción
- **Contenido**: ninguno.
- **Visual**: `[PLACEHOLDER: GIF del sistema funcionando — video con skeleton superpuesto + etiqueta de predicción visible, a pantalla completa ~1100×600 px]`. Label superior pequeña: "Press de hombro — predicción: [clase del GIF elegido]".
- **Layout**: el visual ocupa 90 % del slide; solo el título arriba.

### S20 — Lo que el sistema hace hoy

- **Pill**: `CAPACIDADES ACTUALES`
- **Título (H1)**: Lo que ya está funcionando
- **Contenido**: 4 bullets con flecha amarilla al inicio:
  - → **Pipeline reproducible** de video crudo a clasificación.
  - → **91.6 % de precisión** sobre 3 categorías de técnica.
  - → **Algoritmo original de corrección de tracking** (87 % de discontinuidades resueltas).
  - → **Alternativa open-source de $0** frente a sistemas de USD $10k–$100k+.
- **Visual**: ninguno o ícono decorativo.
- **Layout**: bullets centrados vertical, una idea por línea.

### S21 — Lo que todavía no hace

- **Pill**: `LIMITACIONES`
- **Título (H1)**: Lo que todavía no hace
- **Contenido**: 4 bullets numerados (los números conectarán con el siguiente slide):
  1. Cubre **solo un ejercicio** (press de hombro).
  2. Clasifica **solo 3 categorías** de error (no trayectoria de barra, ni core, ni pies).
  3. No dice **cuándo** en el video ocurre el error.
  4. No da **instrucciones correctivas**, solo clasifica.
- **Subtítulo debajo (gris)**: "Ser honesto sobre los límites hace más valioso lo que sigue."
- **Layout**: lista numerada centrada, numeración en amarillo grande.

### S22 — Trabajo futuro

- **Pill**: `TRABAJO FUTURO`
- **Título (H1)**: Cada limitación abre una dirección de investigación
- **Contenido (grilla 3×2, cada celda con número amarillo en esquina superior izquierda)**:
  - **① Más ejercicios** — Generalizar el pipeline a sentadilla, peso muerto, press de banca.
  - **② Más errores** — Expandir a trayectoria de barra, core, posición de pies.
  - **③ Localización temporal** — Identificar el frame exacto donde ocurre el error.
  - **④ Integración con LLMs** — Traducir clasificaciones a feedback correctivo en lenguaje natural.
  - **⑤ Validación con usuarios reales** — Estudios con entrenadores y practicantes.
  - **⑥ Optimización para mobile** — Inferencia en tiempo real en dispositivos limitados.
- **Visual**: iconos minimalistas amarillos junto a cada título. Los números en círculo amarillo hacen el puente visual con S21.
- **Layout**: grilla 3 columnas × 2 filas.

### S23 — Cierre

- **Pill**: (ninguna)
- **Título (H1)**: Gracias
- **Contenido**: frase personal breve, centrada:
  > *"Empecé sin conocimiento previo del área. El recurso que lo habilitó fueron las becas que me permitieron formarme donde pude adquirir y aplicar estos conocimientos."*
- **Subtexto debajo (gris pequeño)**: "UCASAL · Universidad de Cádiz · POSTECH"
- **Visual**: timeline horizontal minimalista con las 3 universidades y sus ubicaciones (Salta / España / Corea del Sur). Línea amarilla fina conectando tres puntos.
- **Layout**: frase centrada arriba, timeline abajo, sobrio y espacioso.
