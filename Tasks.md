### 👩‍💻 Persona 1: Extractor de Datos (Data Miner) - Marce
*   *Parte de Código (Python):* Se encarga de crear el script principal (extraer_mapa.py) usando la librería osmnx. Su misión es descargar el mapa de la ciudad elegida, extraer los nodos (intersecciones) y las aristas (calles), y exportar todo a un archivo CSV. Debe asegurarse de que haya *más de 1500 nodos*.
*   *Parte del Informe (Markdown):* Redacta la sección *"Descripción del conjunto de datos (dataset)"*. Explica de dónde salió la data (OpenStreetMap), cuántos nodos y aristas hay, y qué columnas tienen los CSV (latitud, longitud, id).

### 🎨 Persona 2: Visualizador y Contexto (Graph & Context)
*   *Parte de Código (Python):* Se encarga de crear un script (visualizar_grafo.py) que lea los CSV generados por la Persona 1 y dibuje el grafo. Debe generar las imágenes del mapa completo y algunos subgrafos (hacer zoom a un barrio específico) usando librerías como networkx o matplotlib.
*   *Parte del Informe (Markdown):* Redacta la sección *"Descripción del problema"*. Explica el contexto real del proyecto (por ejemplo, el caos vehicular en Lima o la necesidad de optimizar rutas para ambulancias) y cita al menos un par de fuentes académicas o noticias. Además, inserta las imágenes generadas con su código.

### 🚥 Persona 3: Lógica de Tráfico y Metodología (Traffic & Proposal)
*   *Parte de Código (Python):* El proyecto exige que el peso de las calles cambie según el tráfico y la hora. Esta persona crea un script (generar_trafico.py) que tome el CSV de las calles y le agregue una nueva columna calculando el "factor de tráfico" (simulando tráfico alto en hora punta y bajo de madrugada).
*   *Parte del Informe (Markdown):* Redacta la sección *"Propuesta". Explica el objetivo del proyecto de forma preliminar y detalla la metodología: qué algoritmo van a usar en los siguientes hitos (ej. Dijkstra o A) para encontrar la ruta más corta considerando esa lógica de tráfico que programó. Además, se encarga de unificar el archivo final en Markdown y exportarlo a PDF.
