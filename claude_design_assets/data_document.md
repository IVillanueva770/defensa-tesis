# Documento de Datos — Defensa de Tesis
## Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora

Este documento tiene dos propósitos: (1) fijar los datos exactos para que no se inventen cifras ni nombres, y (2) dar contexto conceptual suficiente para entender qué es cada cosa y por qué importa. Leer la sección de contexto antes de diseñar — los slides cobran sentido distinto cuando se entiende el problema de fondo.

---

## Identificación del trabajo

- **Título completo:** Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora
- **Autor:** Ignacio Villanueva
- **Tutor:** Mg. Lic. Lorena Talamé
- **Institución:** UCASAL — Universidad Católica de Salta
- **Facultad:** Facultad de Ingeniería e Informática
- **Carrera:** Ingeniería en Informática
- **Año:** 2026

---

## Contexto del problema y del trabajo

### ¿De qué se trata el trabajo?
El trabajo desarrolla un sistema que mira un video de una persona haciendo un ejercicio de fuerza y determina automáticamente si la técnica es correcta o si tiene errores específicos — sin necesidad de un entrenador humano presenciando el ejercicio.

El ejercicio elegido para validar el sistema es el **overhead press** (press de hombro o press de barra sobre la cabeza): el atleta sostiene una barra a la altura de los hombros y la empuja verticalmente hasta tener los brazos extendidos sobre la cabeza. Es un ejercicio técnicamente exigente donde los errores son frecuentes y con consecuencias reales (lesión de hombros, compensación con la zona lumbar, pérdida de fuerza).

### ¿Por qué importa la técnica?
Un movimiento incorrecto repetido cientos de veces durante meses produce lesiones por sobreuso que generalmente no duelen hasta que ya está instalada la lesión. La mayoría de las personas que entrenan solas no tienen acceso a retroalimentación técnica continua. Los entrenadores personales son caros, subjetivos (cada uno tiene criterios distintos) y no siempre están disponibles.

### ¿Por qué no existía una solución accesible?
Las soluciones profesionales de análisis de movimiento (VICON, OptiTrack) requieren hardware especializado de decenas de miles de dólares y no salen del laboratorio. Las aplicaciones comerciales de IA para fitness (Physimax, Kaia, Tempo) tienen costos de suscripción que las hacen inaccesibles para centros de rehabilitación pequeños, escuelas o atletas independientes. Este trabajo propone un pipeline completamente basado en herramientas open-source que funciona con video RGB de cualquier cámara.

### ¿Cuál fue el origen concreto del proyecto?
Una conversación con el Instituto de Rehabilitación de UCASAL (la propia universidad del autor) planteó la necesidad de evaluar técnica de ejercicio sin depender de supervisión humana presencial. Ese fue el punto de partida.

### ¿Qué hace el sistema, en términos simples?
1. Recibe un video del ejercicio
2. Detecta a la persona en cada frame y extrae un "esqueleto" de 17 puntos articulares (hombros, codos, muñecas, caderas, rodillas, etc.)
3. Analiza la secuencia completa de ese esqueleto moviéndose en el tiempo
4. Produce una clasificación: Técnica Correcta, Error de Codos, o Error de Rodillas

### ¿Qué NO hace el sistema?
- No detecta todos los errores posibles — solo los tres para los que fue entrenado
- No señala en qué momento del movimiento ocurre el error (solo clasifica el video completo)
- No funciona en tiempo real (requiere el video completo para clasificar)
- No fue validado con usuarios finales reales (solo con el dataset académico Fitness-AQA)

---

## Conceptos técnicos clave explicados

### Estimación de pose (pose estimation)
La estimación de pose es la tarea de detectar las articulaciones del cuerpo humano en una imagen y ubicarlas como puntos en coordenadas (x, y). El resultado es un "esqueleto" digital que representa la posición del cuerpo. El estándar más usado es COCO 17: 17 puntos articulares (nariz, ojos, orejas, hombros, codos, muñecas, caderas, rodillas, tobillos).

La estimación de pose no entiende el movimiento — solo ve un frame y genera puntos. Para entender movimiento, hay que analizar la secuencia temporal de esos puntos.

### ViTPose
ViTPose es el modelo que hace la estimación de pose en este trabajo. Usa Vision Transformers (ViT) como arquitectura base. Los transformers dividen la imagen en "parches" (patches) y aprenden relaciones entre ellos mediante mecanismos de atención — lo que les permite capturar contexto global (por ej., que la posición del codo depende de la posición del hombro y la muñeca juntos, no solo del parche local del codo).

El enfoque es **top-down**: primero YOLOv8 detecta los bounding boxes de las personas en el frame, y luego ViTPose estima la pose dentro de cada bounding box. Esto permite manejar múltiples personas en el mismo video con alta precisión.

ViTPose produce 133 keypoints (cuerpo completo + manos + cara), pero para este trabajo se usan solo los 17 estándar del cuerpo.

**Limitación importante:** ViTPose procesa cada frame de forma completamente independiente. No tiene memoria entre frames — cada frame es una imagen nueva para él.

### PoseConv3D
PoseConv3D es el modelo que clasifica el movimiento. Su entrada no son imágenes sino **heatmaps de keypoints** (representaciones 2D de la posición de cada articulación) organizados como una secuencia temporal. La arquitectura usa convoluciones 3D que operan simultáneamente sobre el espacio (las coordenadas del esqueleto en el frame) y el tiempo (cómo esas coordenadas cambian a lo largo de la secuencia).

El backbone es ResNet3D SlowOnly: una variante de ResNet (red convolucional profunda) adaptada para trabajar con volúmenes espacio-temporales. "Slow" significa que procesa los frames a velocidad lenta (toma muestras espaciadas en el tiempo), lo que es eficiente para movimientos relativamente lentos como el overhead press.

La secuencia de entrada es de 48 frames uniformemente muestreados de cada video, independientemente de la duración original.

### Vision Transformers (ViT)
Los transformers fueron originalmente diseñados para texto (GPT, BERT). En 2020, Dosovitskiy et al. demostraron que la misma arquitectura funciona para imágenes si se divide la imagen en parches y se trata cada parche como un "token" (al igual que una palabra en texto). La clave es el mecanismo de atención (attention): cada parche puede "mirar" a todos los demás y aprender qué relaciones importan. Esto captura contexto global que las CNNs (que operan localmente, parche por parche) no capturan tan bien.

### Transfer Learning
Entrenar un modelo de redes neuronales profundas desde cero requiere enormes cantidades de datos y tiempo de cómputo. El transfer learning consiste en tomar un modelo que ya fue entrenado en una tarea grande y relacionada, y ajustarlo (fine-tune) para la tarea específica.

En este trabajo: el modelo ResNet3D SlowOnly fue preentrenado en **NTU RGB+D 60**, un dataset de 56,880 videos de movimiento humano con 60 clases de acciones (caminar, aplaudir, levantar objetos, etc.). Aunque ninguna de esas acciones es "overhead press", el modelo aprendió representaciones generales de cómo se mueve el cuerpo humano. Al inicializar con esos pesos y ajustar con los 1,708 videos de entrenamiento del Fitness-AQA, el resultado es mucho mejor que empezar desde cero.

### Overfitting
Cuando un modelo "memoriza" los ejemplos de entrenamiento en lugar de aprender patrones generalizables. Se detecta cuando la pérdida (loss) en entrenamiento baja constantemente pero la pérdida en validación sube o no mejora. El modelo funciona bien en los datos que vio, pero falla en datos nuevos. En el experimento base, con 12 millones de parámetros y solo 1,708 videos, el overfitting fue severo.

### Pose Jittering
Técnica de augmentación (data augmentation) que agrega pequeño ruido gaussiano (σ=2 píxeles) a las coordenadas de los keypoints durante el entrenamiento. El objetivo es que el modelo aprenda que una articulación en (230, 145) y en (232, 143) son esencialmente la misma posición — evitando que memorice posiciones exactas. Equivale a "mover levemente las articulaciones" en cada muestra.

### AdamW
Optimizador (algoritmo que actualiza los pesos del modelo durante el entrenamiento). AdamW es una variante de Adam con regularización por decaimiento de pesos (weight decay) que ayuda a controlar el overfitting. El experimento base usó SGD (gradiente descendente estocástico), que es más simple pero menos adaptativo.

---

## Objetivos del trabajo (texto exacto)

**Objetivo general:**
Desarrollar un sistema de evaluación automática de la técnica en el ejercicio press de hombro (overhead press) mediante el análisis de secuencias de video utilizando visión por computadora y aprendizaje profundo.

**Objetivos específicos:**
1. Investigar y seleccionar los métodos más adecuados de estimación de pose y clasificación de acciones para el contexto del problema.
2. Implementar un pipeline completo que procese video crudo y produzca una clasificación de técnica.
3. Desarrollar técnicas propias para resolver el problema de consistencia temporal de IDs en la estimación de pose.
4. Evaluar el sistema con métricas de clasificación estándar y compararlo con trabajos previos del área.

---

## Tecnologías y herramientas exactas

| Componente | Herramienta/Modelo | Versión / Detalle |
|---|---|---|
| Estimación de pose | ViTPose-B | Vision Transformer Base |
| Detección de personas | YOLOv8 | Para bounding boxes (top-down approach) |
| Clasificación de acciones | PoseConv3D | ResNet3D SlowOnly |
| Backbone | ResNet3D SlowOnly | 12 millones de parámetros |
| Pre-entrenamiento | NTU RGB+D 60 | 56,880 videos de movimiento humano |
| Framework | MMAction2 | OpenMMLab |
| Keypoints | COCO 17 | Estándar anatómico (de los 133 wholebody, se usan 17) |
| Secuencia de entrada | 48 frames uniformemente muestreados | Por video |
| Lenguaje | Python | — |

---

## Dataset

- **Nombre:** Fitness-AQA (Action Quality Assessment)
- **Ejercicio:** Overhead Press (press de hombro / press de barra sobre cabeza)
- **Total de videos:** 2,135
- **División:**
  - Entrenamiento: 1,708 videos
  - Validación: 427 videos

### Distribución de clases

| Clase | Videos | Porcentaje |
|---|---|---|
| Técnica Correcta | ~895 | ~41.9% |
| Error de Codos | ~641 | ~30.0% |
| Error de Rodillas | ~599 | ~28.1% |

### Descripción de cada clase
- **Técnica Correcta:** El atleta ejecuta el press de hombro manteniendo los codos alineados con el torso, rodillas estables, y trayectoria vertical de la barra.
- **Error de Codos:** Los codos se abren excesivamente hacia afuera durante la fase de empuje, lo cual reduce la eficiencia mecánica y aumenta el riesgo de lesión en hombros.
- **Error de Rodillas:** El atleta flexiona o presenta inestabilidad en las rodillas durante la fase de presión, lo cual indica falta de base estable o compensación incorrecta.

---

## Resultados de experimentos (valores exactos)

### Experimento 1 — Baseline (sin transfer learning)
- **Configuración:** ResNet3D SlowOnly entrenado desde cero
- **Precisión final (val):** 51.2%
- **F1-Score macro:** 0.48
- **Pérdida train:** ~0.07 (al final del entrenamiento)
- **Pérdida validación:** ~1.5 (al final del entrenamiento — sube, diverge)
- **Causa del problema:** Overfitting severo. 12M parámetros con solo 1,708 videos de entrenamiento.
- **Referencia gráfica:** `assets/resultados/baseline_experimento_loss.png`, `baseline_experimento_accuracy.png`

### Experimento 2 — Transfer Learning
- **Cambio respecto a baseline:** Inicialización con pesos preentrenados en NTU60 (en vez de pesos aleatorios)
- **Precisión final (val):** 70.5%
- **F1-Score macro:** 0.69
- **Mejora:** +19.3 puntos porcentuales sobre el baseline
- **Brecha train/val:** ~25% (aún hay overfitting, aunque menor)
- **Referencia gráfica:** `assets/resultados/experimento_250522_loss.png`, `experimento_250522_accuracy.png`

### Experimento 3 — Configuración Final
- **Cambios respecto a Exp 2:**
  - Dataset reconstruido con algoritmo de corrección de tracking (contribución original)
  - Optimizador: AdamW (en lugar de SGD)
  - Augmentación: Pose Jittering (ruido Gaussiano sobre coordenadas de keypoints, σ=2px)
  - Label smoothing: ε=0.1
  - LR scheduler: CosineAnnealingLR
- **Precisión final (val):** 91.6%
- **F1-Score macro:** 0.91
- **Brecha train/val:** 2–4% (convergencia estable)
- **Mejora sobre Exp 2:** +21.1 puntos porcentuales
- **Mejora sobre baseline:** +40.4 puntos porcentuales
- **Referencia gráfica:** `assets/resultados/experimento_250525_loss.png`, `experimento_250525_accuracy.png`

---

## Resultados por clase — Configuración Final

| Clase | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Técnica Correcta | 0.94 | 0.92 | 0.93 | ~179 |
| Error de Codos | 0.90 | 0.92 | 0.91 | ~128 |
| Error de Rodillas | 0.89 | 0.91 | 0.90 | ~120 |
| **Macro avg** | **0.91** | **0.92** | **0.91** | **427** |

- **Referencia gráfica:** `assets/resultados/matriz_confusion.png`

---

## Comparación con trabajo relacionado más relevante

**Parmar et al. (2022)** — trabajo de referencia más cercano en el dominio:
- Usaron clasificadores **binarios** (uno para codos, otro para rodillas) sobre el mismo dataset Fitness-AQA
- F1-Score codos: **0.45**
- F1-Score rodillas: **0.84**
- Metodología: clasificadores separados para cada tipo de error

**Este trabajo:**
- Clasificador **multiclase único** (3 clases simultáneas)
- F1-Score codos: **0.91**
- F1-Score rodillas: **0.90**
- F1-Score global (macro): **0.91**

*Nota importante: la comparación es referencial. Parmar et al. abordaron el problema con una estrategia diferente (binaria + especializada por error). Este trabajo unifica las 3 clases en un solo modelo y supera sus resultados en ambas categorías.*

---

## Contribución técnica original: Algoritmo de corrección de tracking

**El problema:**
ViTPose procesa cada frame de forma independiente, sin memoria entre frames. Los IDs de personas detectadas se reasignan en cada frame. Si una persona desaparece por oclusión y reaparece, recibe un nuevo ID — el modelo la trata como una persona distinta.

**Consecuencia sin corrección:**
Para una secuencia de 48 frames, el modelo podría ver 5–10 "personas distintas" cuando en realidad hay una sola. Las secuencias temporales del esqueleto son incoherentes.

**El algoritmo (parámetros exactos):**
- Si una persona desaparece por ≤3 frames consecutivos Y
- Al reaparecer, la posición de su centroide está a ≤25 píxeles de distancia euclidiana de donde desapareció
- → Se reasigna el ID original (se corrige la discontinuidad)

**Resultado:** El 87% de las discontinuidades de tracking fueron corregidas correctamente en el conjunto de validación.

---

## Sistemas de costo comparado (para slide de alternativas)

| Sistema | Tecnología | Costo aproximado |
|---|---|---|
| VICON / OptiTrack | Captura de movimiento 3D con marcadores | USD $10,000–$100,000+ |
| Physimax / Kaia Health | IA para análisis de movimiento, SaaS | USD $50–$200/mes |
| Tempo / Mirror | Hardware dedicado + suscripción software | USD $1,500 + $39/mes |
| **Este proyecto** | **Video RGB estándar + herramientas open-source** | **$0** |

---

## Trayectoria académica del autor

1. **UCASAL** — Salta, Argentina — Carrera base: Ingeniería en Informática
2. **Universidad de Cádiz** — Cádiz, España — Intercambio académico (visión por computadora)
3. **POSTECH** (Pohang University of Science and Technology) — Corea del Sur — Intercambio de investigación (aprendizaje profundo)

---

## Parámetros técnicos adicionales

- **Tamaño de entrada del modelo:** Secuencia de 48 frames, resolución 56×56 (heatmaps de keypoints)
- **Épocas de entrenamiento:** 50 (con early stopping)
- **Batch size:** 16
- **Learning rate inicial:** 0.0001
- **Número de parámetros:** ~12 millones (ResNet3D SlowOnly)
- **Tiempo de inferencia aproximado:** <2 segundos por video en GPU

---

## Archivos de assets disponibles

```
assets/
├── logo-ucasal.png                          → Slide 1 (portada)
├── imagenes_teoricas/
│   ├── 2.4 Dosovitskiy ViT architecture.png  → Slide 7 (ViTPose/ViT)
│   ├── 2.5 keypoints COCO diagram.png         → Slide 7 (keypoints)
│   ├── 2.8 tensorflow 3DCNN.png               → Slide 8 (PoseConv3D)
│   ├── 01 overhead-press correct technique.jpg → Slide 3/4
│   └── 01 error overhead-press-legs.jpg        → Slide 3/4
├── pipeline/
│   └── arquitectura detallada.jpg             → Slide 6 (pipeline completo)
├── resultados/
│   ├── baseline_experimento_loss.png          → Slide 11
│   ├── baseline_experimento_accuracy.png      → Slide 11
│   ├── experimento_250522_loss.png            → Slide 12
│   ├── experimento_250522_accuracy.png        → Slide 12
│   ├── experimento_250525_loss.png            → Slide 13
│   ├── experimento_250525_accuracy.png        → Slide 13
│   └── matriz_confusion.png                   → Slide 15
└── personal/
    └── video mio en corea mientras investigaba.mp4 → Slide 18

videos_keypoints/
├── correct_79235_2_kp.mp4       → Técnica Correcta (ejemplo 1)
├── correct_79540_1_kp.mp4       → Técnica Correcta (ejemplo 2)
├── elbows_error_62866_3_kp.mp4  → Error de Codos (ejemplo 1)
├── elbows_error_62876_2_kp.mp4  → Error de Codos (ejemplo 2)
├── knees_error_62908_1_kp.mp4   → Error de Rodillas (ejemplo 1)
└── knees_error_63176_3_kp.mp4   → Error de Rodillas (ejemplo 2)
```
