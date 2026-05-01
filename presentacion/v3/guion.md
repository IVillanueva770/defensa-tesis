# Guion de exposición — Defensa de tesis

Lo que digo mientras cada slide está de fondo. Primera persona, tono conversacional — pensado para hablar, no para leer. Tiempo estimado por slide entre paréntesis. Total: ~20 min.

---

### S1 — Portada (20 seg)

"Buenas tardes. Mi nombre es Ignacio Villanueva, y vengo a presentar mi Proyecto Final de Grado, titulado *Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora*. Este trabajo fue dirigido por la licenciada Lorena Talamé. Muchas gracias por estar acá."

### S2 — Agenda (20 seg)

"Voy a estructurar la charla en cinco momentos. Primero, la pregunta que movió todo el proyecto. Después, el sistema que construí para responderla. Luego les voy a contar el recorrido experimental, porque hubo tres intentos antes de llegar al número final. Cuarto, los resultados que obtuvimos. Y para cerrar, qué abre este trabajo hacia adelante."

---

> **PUENTE al Acto I** (transición natural desde S2 a S3): la última palabra de S2 es "adelante", la primera de S3 es la pregunta. Silencio breve de 1 segundo para marcar el cambio.

### S3 — La pregunta (45 seg)

"Todo empezó con una conversación con el Instituto de Rehabilitación de UCASAL. Ellos querían mejorar la forma en que evalúan a los pacientes haciendo ejercicios, y se nos planteó una pregunta que parece simple pero no lo es: *¿puede una cámara común, la de un celular o una notebook, evaluar la técnica de un ejercicio de forma automática, objetiva y accesible?* Lo que ven en pantalla es exactamente eso: una persona haciendo press de hombro, y el sistema dibujando sobre su cuerpo los puntos articulares que usa para analizar la técnica. Pero para llegar a eso había mucho camino."

### S4 — Por qué importa (45 seg)

"¿Por qué importa resolver esto? Por tres razones. La primera: la mala técnica es la principal causa de lesiones en entrenamiento no supervisado. La segunda: el criterio de un entrenador humano es subjetivo, varía de persona a persona, y no escala a miles de practicantes. La tercera: los sistemas objetivos que existen hoy — los que usan los equipos profesionales — requieren laboratorios con cámaras especializadas y sensores. No están al alcance de un gimnasio, una clínica chica, o un individuo."

### S5 — Las alternativas existentes (45 seg)

"Acá se ve concretamente el problema. Los sistemas de captura de movimiento profesionales, como VICON u OptiTrack, cuestan entre diez mil y más de cien mil dólares. Hay apps comerciales que cuestan entre cincuenta y doscientos dólares por mes. Productos consumer como Tempo o Mirror cuestan mil quinientos dólares más suscripción. Este proyecto propone una alternativa con la misma utilidad clínica, usando solo video de cámara común y herramientas open source. Costo: cero."

### S6 — Objetivos y alcance (45 seg)

"Con ese diagnóstico en mente, conviene plantear concretamente a qué me comprometí. El objetivo general fue desarrollar un modelo capaz de clasificar la técnica del press de hombro desde video y categorizar errores de ejecución. Para lograrlo definí cuatro objetivos específicos: primero, conformar un conjunto de videos de entrenamiento; segundo, construir el pipeline de extracción de información biomecánica; tercero, entrenar y optimizar el modelo de manera iterativa; y cuarto, evaluar el desempeño con métricas estándar y protocolos de validación. El alcance es acotado a propósito: un solo ejercicio, tres categorías de error, y el dataset Fitness-AQA como referencia. Esta decisión de enfoque permitió profundizar con rigor antes de pensar en extensiones."

---

> **PUENTE al Acto II**: "Con el objetivo definido, lo que había que construir era un sistema de dos etapas."

### S7 — El pipeline en una imagen (50 seg)

"El sistema que construí tiene cuatro componentes. A la entrada, un video cualquiera de una persona haciendo press de hombro. Primero, un modelo llamado ViTPose detecta los puntos articulares de la persona frame por frame — la cabeza, los hombros, los codos, las muñecas, y así. Eso genera una secuencia de coordenadas en formato JSON: diecisiete puntos por frame, cuarenta y ocho frames por video. Esa secuencia pasa a un segundo modelo, PoseConv3D, que analiza todo el movimiento completo y lo clasifica en tres categorías: técnica correcta, error de codos, o error de rodillas. Este pipeline es reproducible de principio a fin — cualquiera puede correrlo con el código que dejé documentado."

### S8 — ¿Por qué ViTPose? (50 seg)

"¿Por qué elegí ViTPose para la primera etapa? Porque tiene una propiedad muy particular. Los enfoques tradicionales, como OpenPose o MediaPipe, analizan la imagen por partes: detectan codos por un lado, hombros por otro, y después tratan de conectar las piezas. ViTPose, que está basado en Vision Transformers, hace algo distinto: ve todas las articulaciones al mismo tiempo, entiende el cuerpo como un todo, no como una suma de partes. Para evaluar técnica, donde lo importante es cómo se relacionan las articulaciones entre sí, esa propiedad es fundamental."

### S9 — ¿Por qué PoseConv3D? (50 seg)

"La segunda etapa, PoseConv3D, tiene otra propiedad interesante. Toma los keypoints — que son coordenadas planas — y los convierte en un volumen de tres dimensiones: dos espaciales más el tiempo. Después aplica convoluciones 3D sobre ese volumen, las mismas que se usan para analizar video. Esto permite capturar al mismo tiempo cómo se configura el cuerpo en cada instante *y* cómo ese movimiento evoluciona frame a frame. Usé una arquitectura llamada ResNet3D SlowOnly, preentrenada en un dataset grande de acciones humanas llamado NTU60. Más adelante ese preentrenamiento va a ser importante."

### S10 — El problema del tracking (60 seg)

"Al trabajar con el pipeline me topé con un problema que no estaba documentado y que requirió una contribución técnica original. ViTPose procesa cada frame de manera independiente — no tiene memoria entre frames. Eso significa que la misma persona puede tener un ID en un frame, desaparecer temporalmente por una oclusión, y reaparecer dos frames después con un ID distinto. En los datos reales, una persona con ID cuarenta y cuatro podía desaparecer dos frames y reaparecer como ID cincuenta y uno. El efecto era que el modelo creía que había tres personas donde había una sola, y aprendía patrones de movimiento fragmentados que no correspondían a nadie."

### S11 — El algoritmo de corrección (60 seg)

"Para resolverlo desarrollé un algoritmo de corrección de tracking basado en similitud de poses. La regla es simple: si un ID desaparece por tres frames o menos, y después aparece un ID nuevo a menos de veinticinco píxeles de distancia en términos de posición promedio de keypoints, asumo que es la misma persona y le reasigno el ID original. Son tres pasos: detectar la discontinuidad, verificar las condiciones de distancia y tiempo, y reasignar. Este algoritmo simple corrigió el ochenta y siete por ciento de las discontinuidades en el dataset. Y como van a ver en un momento, esto fue determinante para los resultados."

---

> **PUENTE al Acto III**: "Con el pipeline en pie y el tracking arreglado, vino la parte más desafiante: entrenar el modelo."

### S12 — Tres preguntas, tres experimentos (40 seg)

"El entrenamiento del modelo no fue un proceso lineal. No fue ajustar hiperparámetros una vez y listo. Fueron tres experimentos, y cada uno respondía una pregunta diferente. La primera: ¿puede el modelo aprender sin ningún conocimiento previo, desde cero? La segunda: si eso no alcanza, ¿ayuda usar conocimiento preentrenado? Y la tercera, que fue la pregunta más reveladora: ¿el problema estaba en el modelo, o estaba en los datos?"

### S13 — Experimento 1: baseline (55 seg)

"El primer experimento fue la configuración base. Entrené ResNet3D desde cero, con pesos inicializados aleatoriamente, usando técnicas estándar de regularización. El resultado: cincuenta y uno coma dos por ciento de precisión. F1 de cero cuarenta y ocho. Y lo más importante — miren la curva de pérdida a la derecha. La línea azul, que es entrenamiento, baja. La naranja, que es validación, no baja. Es la firma clásica del overfitting severo: el modelo memoriza los ejemplos de entrenamiento, pero no generaliza a datos nuevos. La conclusión del experimento uno fue clara: con dos mil videos no alcanza para entrenar una red convolucional 3D desde cero."

### S14 — Experimento 2: transfer learning (55 seg)

"Segunda iteración. Tomé los pesos de un modelo preentrenado en NTU60, un dataset de cincuenta y seis mil ochocientos videos de acciones humanas, y les hice fine-tuning en mi problema. El razonamiento es: las representaciones generales del movimiento humano debieran transferirse. Resultado: setenta coma cinco por ciento. Diecinueve puntos porcentuales sobre el baseline. F1 de cero sesenta y nueve. La curva muestra una mejora real: la brecha entre entrenamiento y validación se redujo. Pero seguía habiendo una brecha del veinticinco por ciento, y el desempeño no era suficiente para una aplicación práctica. Acá me hice la tercera pregunta: ya no era el conocimiento previo, entonces ¿qué más estaba fallando?"

### S15 — Experimento 3: datos (70 seg)

"El tercer experimento llegó al número final: noventa y uno coma seis por ciento. Pero lo interesante no es el número, es de dónde vino. No vino de un modelo más grande. No vino de más capacidad. Vino de entender que los datos estaban corruptos. La tabla muestra los cuatro cambios que introduje. El que más pesó, por lejos, fue aplicar el algoritmo de corrección de tracking al dataset. Antes de corregir, el modelo veía secuencias fragmentadas donde aparecían cinco o diez 'personas' distintas en un solo video. Después de corregir, veía una sola persona moviéndose de forma coherente. Los otros tres cambios — AdamW en lugar de SGD, pose jittering para robustez, y label smoothing para prevenir sobreconfianza — ayudaron, pero el cambio principal fue el de los datos. La curva final muestra convergencia estable, con brecha mínima entre entrenamiento y validación."

---

> **PUENTE al Acto IV**: "Este fue el número final. Vamos a verlo en detalle."

### S16 — El resultado en un número (30 seg)

"Acá está el resultado resumido. Noventa y uno coma seis por ciento de precisión. F1 macro de cero noventa y uno. Evaluado sobre cuatrocientos veintisiete videos de validación del dataset Fitness-AQA. En términos prácticos, el modelo clasifica correctamente aproximadamente nueve de cada diez ejecuciones."

### S17 — Desglose por clase (50 seg)

"Pero un número promedio puede esconder desbalances, así que miré cómo se comporta en cada clase. La tabla muestra que el modelo es parejo: F1 de cero noventa y tres en técnica correcta, cero noventa y uno en errores de codos, cero noventa en errores de rodillas. La matriz de confusión a la derecha confirma lo mismo visualmente — la diagonal principal es dominante, los errores fuera de diagonal son pocos y simétricos, y no hay sesgo hacia la clase mayoritaria. En un problema de tres clases con un dataset desbalanceado, este balance es un indicador fuerte de que el modelo aprendió los patrones biomecánicos reales, no simplemente memorizó la clase más frecuente."

### S18 — Comparación académica (60 seg)

"¿Cómo se compara este resultado contra el estado del arte? Parmar y colegas publicaron en dos mil veintidós el trabajo de referencia sobre este mismo dataset. Usaron una estrategia distinta: entrenaron dos clasificadores binarios, uno para detectar errores de codos, otro para errores de rodillas. Sus resultados: F1 de cero cuarenta y cinco en codos, cero ochenta y cuatro en rodillas. Mi trabajo usa un solo clasificador multiclase que distingue entre técnica correcta, errores de codos y errores de rodillas simultáneamente. F1 de cero noventa y uno en codos, cero noventa en rodillas. O sea: con un modelo más simple y unificado, superamos la referencia en ambas categorías. La mejora en la clase de codos es particularmente grande: cero cuarenta y seis puntos."

### S19 — Demo (40 seg)

"Y acá está el sistema funcionando. Lo que ven es un video real procesado por el pipeline completo: la persona hace press de hombro, ViTPose extrae los keypoints frame a frame, el algoritmo de tracking los mantiene coherentes, y PoseConv3D analiza los cuarenta y ocho frames y clasifica la técnica. La predicción aparece arriba en la etiqueta. Este mismo flujo se puede correr sobre cualquier video, grabado con cualquier cámara, en cualquier condición de iluminación razonable."

---

> **PUENTE al Acto V**: "El sistema funciona. Pero hay que ser honestos sobre qué puede y qué no puede hacer aún."

### S20 — Lo que el sistema hace hoy (40 seg)

"Voy a resumir entonces qué logró concretamente este trabajo. Primero: un pipeline reproducible, documentado de punta a punta, desde video crudo hasta clasificación. Segundo: noventa y uno coma seis por ciento de precisión en tres categorías de técnica, superando la referencia publicada. Tercero: un algoritmo original de corrección de tracking que es contribución técnica del proyecto y que resolvió un problema no documentado en la literatura. Y cuarto: una alternativa open source con costo cero frente a sistemas comerciales que cuestan entre diez mil y cien mil dólares."

### S21 — Lo que todavía no hace (45 seg)

"Pero el sistema tiene limitaciones claras que conviene declarar. Primero: cubre un solo ejercicio, el press de hombro. Segundo: detecta solo tres categorías de error — no cubre trayectoria de barra, no evalúa activación del core, no analiza la posición de los pies. Tercero: dice *si* hay un error, pero no dice *cuándo* en el video ocurre. Y cuarto: clasifica, pero no explica — el sistema no genera instrucciones correctivas para el usuario. Ser honesto sobre los límites es lo que hace más valioso lo que viene."

### S22 — Trabajo futuro (70 seg)

"Cada una de esas limitaciones abre una dirección concreta de investigación. Extender a más ejercicios — sentadilla, peso muerto, press de banca — siguiendo la misma metodología y aprovechando transfer learning entre ejercicios. Expandir las categorías de error para cubrir más aspectos biomecánicos. Agregar localización temporal, que el modelo identifique el frame exacto donde se deteriora la técnica. Integración con modelos de lenguaje para traducir una clasificación en una instrucción correctiva entendible: en lugar de decir 'error de codos', decir 'el codo derecho está abriéndose más de lo que debería en la fase descendente'. Validación con usuarios reales: estudios de campo con entrenadores y practicantes. Y finalmente, optimización para dispositivos móviles, que es la condición para que esto llegue al usuario final. Estas seis direcciones responden punto por punto a las seis limitaciones del slide anterior."

### S23 — Cierre (40 seg)

"Para cerrar, una reflexión personal. Empecé este proyecto sin conocimiento previo del área. Lo que me habilitó recorrerlo fueron las becas que me permitieron formarme en UCASAL, en la Universidad de Cádiz, y en POSTECH, en Corea del Sur. Sin esos tres pasos por esas tres universidades, este trabajo no existiría. Quiero agradecer a mi tutora Lorena, a mi familia, y al tribunal por el tiempo que se toma hoy. Estoy disponible para las preguntas que quieran hacer. Gracias."
