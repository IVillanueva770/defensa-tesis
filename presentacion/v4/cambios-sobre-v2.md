# Cambios a hacerle al v2 — checklist de edición

Este documento **no es un prompt para Gamma**. Es una lista de edits puntuales sobre el PDF/archivo v2 que ya tenés generado. Cada sección habla de una slide del v2 e indica: qué mantener, qué modificar, y (cuando aplica) qué slide nuevo insertar después.

Resultado final: el v2 queda con ~22 slides, bien acomodadas en 5 actos, sin regenerar desde cero en Gamma.

---

## Cambios generales (aplicar a toda la presentación)

1. **Eliminar todas las "notas de diseño" visibles.** En el v2 se renderizaron instrucciones de autor al diseñador en S1, S9 y S11 (textos como "*Nota de diseño: incluir logo-ucasal.png*", "*incluir gráficos de pérdida...*", "*incluir matriz_confusion.png como visual complementario*"). Estas frases no deberían verse.
2. **Arreglar la imagen rota del S13** ("There was an error generating this image") — reemplazar por la matriz de confusión real del paper (Figura 18, p. 51).
3. **Llenar el panel derecho vacío del S14 Conclusiones** (actualmente hay un placeholder gris) — ver propuesta en la sección correspondiente abajo.

---

## Slide por slide

### S1 — Portada ✏️ MODIFICAR

**Qué cambiar**:
- Quitar la línea "*Nota de diseño: incluir logo-ucasal.png en este slide*".
- Insertar el logo UCASAL real donde se indicaba.

**Todo lo demás queda igual**: título, autor/tutor, ilustración de press de hombro.

---

### ➕ NUEVO SLIDE — Agenda (insertar entre S1 y el actual S2)

Slide nuevo, sobrio:

- **Pill**: `AGENDA`
- **Título**: Agenda
- **Contenido**: 5 ítems numerados con su número en amarillo grande:
  1. La pregunta
  2. El sistema
  3. El recorrido experimental
  4. Resultados
  5. Hacia dónde sigue
- **Visual**: línea vertical amarilla conectando los 5 números. Sin imagen.
- **Layout**: lista centrada, mucho aire.

---

### S2 — El Origen del Proyecto ✏️ SIMPLIFICAR

El v2 tiene 3 cards apiladas (Sin supervisión / Con supervisión humana / La pregunta). Son 3 ideas en una sola slide.

**Qué hacer**:
- **Eliminar** las dos primeras cards ("Sin supervisión" y "Con supervisión humana"). Esa información pasa al nuevo slide "Por qué importa" (ver más abajo).
- **Dejar solo la pregunta central** como única idea:
  > *¿Puede una cámara común evaluar la técnica de un ejercicio de forma automática, objetiva y accesible?*
- Subtítulo gris debajo: "El punto de partida fue una conversación con el Instituto de Rehabilitación de UCASAL."
- Mantener el GIF/imagen de keypoints a la derecha.
- Pill cambia a `MOTIVACIÓN` (ya lo es).

---

### S3 — Un poco de Contexto (UCASAL/Cádiz/POSTECH) 🔀 MOVER AL FINAL

Esta slide interrumpe el hilo técnico cuando está a principio. Queda mucho mejor como cierre personal.

**Qué hacer**:
- **Mover esta slide al final de la presentación** (nueva posición: después del Trabajo Futuro, como cierre).
- Al reubicarla, cambiar el título de "Un poco de Contexto" a "Gracias" o similar.
- Texto del slide allá: una frase personal breve del capítulo "Reflexión Final" del paper:
  > *"Empecé sin conocimiento previo del área. El recurso que lo habilitó fueron las becas que me permitieron formarme donde pude adquirir y aplicar estos conocimientos."*
- El timeline UCASAL → Cádiz → POSTECH queda debajo como apoyo visual.

---

### ➕ NUEVO SLIDE — Por qué importa (insertar donde estaba el S3)

Este slide recupera la información que sacamos de las cards de S2, pero con una sola idea limpia.

- **Pill**: `MOTIVACIÓN`
- **Título**: Entrenar sin guía correcta es un problema real
- **Contenido**: 3 cards horizontales con ícono arriba + 1 frase:
  1. **Lesiones** — La mala técnica es la primera causa de lesiones en entrenamiento sin supervisión.
  2. **Supervisión humana** — El criterio de un entrenador es subjetivo y no escala a miles de practicantes.
  3. **Sistemas objetivos** — Los que existen hoy requieren laboratorios costosos.
- **Visual**: iconos minimalistas monocromo amarillo (pesa, ojo, laboratorio).
- **Layout**: 3 columnas iguales, cards con borde izquierdo amarillo.

---

### S4 — Las Alternativas Existentes ✅ MANTENER (pequeño ajuste)

Está bien como está. Solo:
- Reducir el texto introductorio de la izquierda ("El sistema desarrollado utiliza video RGB estándar..."). Se puede dejar una sola frase: "Las alternativas existentes son inaccesibles."
- La tabla queda igual.
- Destacar un poco más la fila "Este proyecto" (fondo amarillo más saturado).

---

### ➕ NUEVO SLIDE — Objetivos y alcance (insertar después de S4)

- **Pill**: `OBJETIVOS Y ALCANCE`
- **Título**: Qué me comprometí a resolver
- **Contenido**: 2 columnas.

  **Izquierda — Objetivo general**:
  > Desarrollar un modelo de clasificación de técnica en el ejercicio de **press de hombro**, capaz de identificar y categorizar errores de ejecución desde video.

  **Derecha — Objetivos específicos** (4 bullets numerados):
  1. Conformar un conjunto de videos de entrenamiento.
  2. Construir el pipeline de extracción de información biomecánica.
  3. Entrenar y optimizar iterativamente el modelo.
  4. Evaluar el desempeño con métricas estándar y protocolos de validación.

- **Línea de alcance abajo, gris**: "Alcance: un ejercicio, 3 categorías de técnica, dataset Fitness-AQA (2.135 videos). Entregable: pipeline completo + modelo entrenado."

---

### S5 — La Solución: El Pipeline ✂️ DIVIDIR EN 2

Actualmente mete 3 ideas: el diagrama, ViTPose, y PoseConv3D.

**Qué hacer**:
- **Slide 5a (queda con el nombre actual)**: solo el diagrama de 4 nodos a pantalla completa. **Borrar los dos bloques descriptivos de abajo** (los que empiezan con "ViTPose — Estimación de Poses" y "PoseConv3D — Clasificación Temporal").
- Eliminar también las referencias a assets en texto ("Assets de referencia: keypoints COCO diagram.png...").
- **Slide 5b (nueva)**: se convierte en lo que era el S6 "¿Por qué ViTPose?" — ver abajo.

---

### S6 — ¿Por qué ViTPose? ✏️ INVERTIR JERARQUÍA

El v2 tiene la frase más potente — *"ViTPose entiende el cuerpo como un todo, no como una suma de partes"* — escondida al final, debajo de dos columnas de texto denso.

**Qué hacer**:
- Mover esa frase al **centro del slide, grande, amarillo serif-bold**. Que sea lo primero que se vea.
- Reducir las dos columnas "Otras herramientas" vs "ViTPose" a 2 bullets cortos cada una:
  - **OpenPose / MediaPipe**: analizan por partes locales y después ensamblan.
  - **ViTPose**: ve todas las articulaciones al mismo tiempo (Vision Transformers).
- Agregar un diagrama pequeño de ViT a la derecha (o un placeholder).

---

### ➕ NUEVO SLIDE — ¿Por qué PoseConv3D? (insertar después del ViTPose)

El v2 no lo tiene como slide propio. Es importante explicar la segunda etapa.

- **Pill**: `ARQUITECTURA · ETAPA 2`
- **Título**: ¿Por qué PoseConv3D?
- **Frase central**:
  > *Convierte los keypoints en un volumen espacio-temporal, y aplica convoluciones 3D sobre él.*
- **Bullets**:
  - **Entrada**: 48 frames × 17 keypoints, apilados como heatmaps gaussianos.
  - **Backbone**: ResNet3D SlowOnly (12 M parámetros), preentrenado en NTU60.
- **Visual**: representación 3D del volumen (placeholder).

---

### S7 — El Problema del Tracking ✂️ DIVIDIR EN 2

El v2 mete el problema + el algoritmo en una sola slide densa.

**Qué hacer**:
- **Slide 7a — El problema**: quedarse con la primera mitad actual (la explicación de que ViTPose no tiene memoria entre frames, IDs saltando).
  - Frase central grande: *"Una persona con ID '44' puede desaparecer 2 frames y reaparecer como '51'. El modelo ve 3 personas donde hay 1."*
  - Visual: tira de 5 frames con IDs cambiando (placeholder o GIF).
- **Slide 7b — El algoritmo**: la segunda mitad, con la regla exacta (≤3 frames + ≤25 px) y los 3 círculos amarillos (detectar / verificar / reasignar).
  - Cifra a la derecha grande: **87 %** de discontinuidades corregidas.

---

### S8 — La Lógica de los Experimentos ✅ MANTENER

Está bien como marco para los 3 experimentos. Solo **borrar las respuestas** que están abajo ("NO — 51.2%, overfitting severo", "PARCIALMENTE — 70.5%...", "LOS DATOS — 91.6%..."). Dejar solo las 3 preguntas.

Las respuestas se revelan una por una en los 3 slides siguientes, no todas juntas acá.

---

### S9 — Evolución del Rendimiento ✂️ DIVIDIR EN 3

Este es el cambio más fuerte. El v2 mete 3 experimentos + tabla + nota de diseño en una sola slide. Para que el tribunal pueda seguir la narrativa, conviene tres slides, uno por experimento.

**Qué hacer**:

- **Slide 9a — Experimento 1 (baseline)**:
  - Cifra gigante: **51.2 %**
  - Subtítulo naranja: *overfitting severo*
  - 2 bullets: "ResNet3D desde cero" / "F1 = 0.48, pérdida val ~1.5"
  - Gráfico: curva de pérdida divergente (Figura 12 del paper)
  - Frase cierre: "El modelo memoriza, no generaliza."

- **Slide 9b — Experimento 2 (transfer learning)**:
  - Cifra gigante: **70.5 %**
  - Subtítulo naranja: *+19.3 pp sobre baseline*
  - 2 bullets: "Preentrenado en NTU60 (56.880 videos)" / "F1 = 0.69, brecha ~25 %"
  - Gráfico: curva de pérdida con transfer learning (Figura 14 del paper)
  - Frase cierre: "Ya no era el conocimiento previo. Algo más seguía fallando."

- **Slide 9c — Experimento 3 (datos corregidos)**:
  - Cifra gigante: **91.6 %**
  - Subtítulo naranja bold: **"El salto no vino de un modelo más grande. Vino de entender los datos."**
  - Gráfico: curva de precisión final con convergencia estable (Figura 16 del paper)
  - Acá se absorbe lo que hoy está en el S10 (ver abajo).

**Borrar** la nota de diseño "*incluir gráficos de pérdida y precisión de los tres experimentos: baseline_experimento_*.png...*" que quedó visible.

---

### S10 — Qué cambia en la configuración final y por qué 🔀 ABSORBER EN S9c

Actualmente es una tabla 4×2 densa. Su contenido se mueve dentro del slide del Experimento 3 (nuevo 9c).

**Qué hacer**:
- Condensar la tabla a 4 filas con 1 frase cada una. Destacar la primera fila en amarillo (dataset con tracking corregido), las otras 3 en gris:

  | Cambio | Qué resolvió |
  |--------|--------------|
  | **Dataset con tracking corregido** | El modelo veía 5–10 "personas" donde había 1 |
  | AdamW vs SGD | Convergencia adaptativa |
  | Pose Jittering (σ=2 px) | Robustez ante imprecisiones de ViTPose |
  | Label smoothing (ε=0.1) | Previene sobreconfianza |

- Insertarla en el slide 9c como bloque izquierdo, con la curva de precisión a la derecha.
- **Eliminar S10 como slide independiente.**

---

### ➕ NUEVO SLIDE — Un número lo resume (insertar entre el nuevo 9c y el actual S11)

Slide minimalista de apertura del Acto IV.

- **Pill**: `RESULTADOS`
- **Título**: Un número lo resume
- **Cifra gigante centrada**: **91.6 %** precisión · **0.91** F1-macro
- **Subtítulo gris**: "Evaluado sobre 427 videos de validación del dataset Fitness-AQA."
- Sin visual. Pantalla minimalista. Este slide respira.

---

### S11 — Resultados por Clase ✅ MANTENER (pequeño ajuste)

- **Borrar** la nota de diseño "*incluir matriz_confusion.png como visual complementario*".
- Reducir el texto introductorio de la izquierda.
- Tabla queda igual.
- **Agregar** la matriz de confusión real (Figura 18 del paper) a la derecha — así se absorbe el contenido del S13 (que tiene imagen rota) dentro de este slide.

---

### S12 — Comparación Académica ✅ MANTENER

Está bien como está. Solo:
- Reducir el texto introductorio.
- Destacar más los números de la columna "Este Trabajo" (naranja más grande).
- Resaltar visualmente el salto **0.45 → 0.91** en F1 Codos (flecha, color, lo que sea).

---

### S13 — Qué dice la matriz de confusión ❌ ELIMINAR

Este slide tiene imagen rota y su contenido se duplica con lo de S11. Al incorporar la matriz real en S11, este slide deja de hacer falta.

**Qué hacer**: borrarlo completamente.

---

### ➕ NUEVO SLIDE — Demo (insertar entre S12 y el actual S14)

Este es el slide más importante que le falta al v2. Para una defensa de visión por computadora, ver el sistema funcionando vale más que cualquier tabla.

- **Pill**: `DEMO`
- **Título**: El sistema en acción
- **Contenido**: ninguno.
- **Visual**: GIF del sistema funcionando (hay varios en el repo, elegir uno bueno) a pantalla completa. Label superior: "Press de hombro — predicción: [clase del GIF]".
- **Layout**: el GIF ocupa el 90 % del slide.

---

### S14 — Conclusiones ✂️ DIVIDIR EN 2

El v2 tiene 4 bullets a la izquierda y el panel derecho vacío. Conviene dividir "lo que hace" de "lo que no hace" para después conectar con trabajo futuro.

**Qué hacer**:

- **Slide 14a — Lo que ya funciona** (reemplaza el actual S14):
  - Pill: `CAPACIDADES ACTUALES`
  - Título: Lo que ya está funcionando
  - Los mismos 4 bullets con flecha amarilla (pipeline reproducible, 91.6 %, algoritmo de tracking, alternativa $0).
  - Llenar el panel derecho vacío con un ícono decorativo o cambiar a layout de 1 columna.

- **Slide 14b — Lo que todavía no hace** (nuevo):
  - Pill: `LIMITACIONES`
  - Título: Lo que todavía no hace
  - 4 bullets **numerados** (importante, porque el S15 los va a referenciar):
    1. Cubre **solo un ejercicio** (press de hombro).
    2. Clasifica **solo 3 categorías** de error (no trayectoria de barra, ni core, ni pies).
    3. No dice **cuándo** en el video ocurre el error.
    4. No da **instrucciones correctivas**, solo clasifica.
  - Subtítulo gris: "Ser honesto sobre los límites hace más valioso lo que sigue."

---

### S15 — Trabajo Futuro ✏️ CONECTAR CON LIMITACIONES

El v2 tiene 5 direcciones en grilla 3×2 (uno está vacío). El contenido está bien pero le falta el puente con las limitaciones que acabamos de declarar.

**Qué hacer**:
- Cambiar el título a: *"Cada limitación abre una dirección de investigación"*.
- Agregar un **número pequeño en la esquina superior izquierda de cada card** (①②③④⑤⑥), que haga match con los números del slide anterior de limitaciones.
- Completar a 6 tarjetas (llenar la que está vacía):
  - **① Más ejercicios** — sentadilla, peso muerto, press de banca.
  - **② Más errores** — trayectoria de barra, core, pies.
  - **③ Localización temporal** — frame exacto donde ocurre el error.
  - **④ Integración con LLMs** — feedback correctivo natural.
  - **⑤ Validación con usuarios reales** — estudios con entrenadores.
  - **⑥ Optimización para mobile** — inferencia en tiempo real.

---

### ↩️ Slide final — Cierre personal (reubicado desde el v2 S3)

El antiguo S3 ("Un poco de Contexto" con UCASAL/Cádiz/POSTECH) se reubica acá.

**Qué hacer**:
- Cambiar el título a "Gracias".
- Reemplazar "Nula experiencia inicial / Distintos campos del conocimiento / Intercambios estudiantiles" por una frase personal del capítulo "Reflexión Final":
  > *"Empecé sin conocimiento previo del área. El recurso que lo habilitó fueron las becas que me permitieron formarme donde pude adquirir y aplicar estos conocimientos."*
- Mantener el timeline UCASAL → Cádiz → POSTECH abajo.

---

## Orden final resultante (22 slides)

1. Portada *(v2 S1, modificado)*
2. Agenda *(nuevo)*
3. La pregunta *(v2 S2, simplificado)*
4. Por qué importa *(nuevo)*
5. Las alternativas existentes *(v2 S4)*
6. Objetivos y alcance *(nuevo)*
7. El pipeline *(v2 S5a, depurado)*
8. ¿Por qué ViTPose? *(v2 S6, con frase central reposicionada)*
9. ¿Por qué PoseConv3D? *(nuevo)*
10. El problema del tracking *(v2 S7a, partido)*
11. El algoritmo de corrección *(v2 S7b, partido)*
12. Tres preguntas, tres experimentos *(v2 S8, sin respuestas)*
13. Experimento 1: 51.2 % *(v2 S9a, partido)*
14. Experimento 2: 70.5 % *(v2 S9b, partido)*
15. Experimento 3: 91.6 % *(v2 S9c, partido + S10 absorbido)*
16. Un número lo resume *(nuevo)*
17. Resultados por clase + matriz *(v2 S11, con S13 absorbido)*
18. Comparación académica *(v2 S12)*
19. Demo *(nuevo)*
20. Lo que ya funciona *(v2 S14, reformateado)*
21. Lo que todavía no hace *(nuevo)*
22. Trabajo futuro *(v2 S15, conectado con limitaciones)*
23. Gracias *(v2 S3 reubicado)*

---

## Resumen rápido de acciones

- **Slides a eliminar**: S13 (1).
- **Slides a dividir**: S5 → 2, S7 → 2, S9 → 3, S14 → 2 (total 9 slides nuevos de dividir).
- **Slides a reubicar**: S3 al final.
- **Slides a mantener casi igual**: S1, S4, S8, S11, S12, S15 (6 slides con ediciones menores).
- **Slides nuevos a crear**: Agenda, Por qué importa, Objetivos y alcance, PoseConv3D, Un número lo resume, Demo (6 slides).

Total: de 15 slides en v2 a 22–23 slides en la versión final.
