## 2. Descripción del conjunto de datos (Dataset)

Para el desarrollo de este proyecto, hemos seleccionado la ciudad de **Barcelona, España**, debido a su famosa estructura de red vial en cuadrícula (L'Eixample), la cual es un escenario ideal para la aplicación de algoritmos de optimización de rutas. 

La extracción de los datos se realizó de manera automatizada utilizando Python y la librería `osmnx`, la cual consume la base de datos geoespacial global de **OpenStreetMap**. El dataset representa el grafo bidireccional de la red vial para conducción de vehículos y se ha exportado en dos archivos CSV:

### 2.1. Nodos (Intersecciones)
* **Archivo:** `dataset/intersections.csv`
* **Cantidad de registros:** 8997 nodos.
* **Descripción:** Cada registro representa una intersección o punto de conexión en las calles de Barcelona. Las variables obtenidas son las coordenadas geográficas `y` (latitud), `x` (longitud) y el identificador único del nodo (`osmid`). 
* *Nota: La cantidad de nodos extraídos cumple satisfactoriamente con el requisito del curso de superar los 1500 nodos.*

### 2.2. Aristas (Calles)
* **Archivo:** `dataset/streets.csv`
* **Cantidad de registros:** 16702 aristas.
* **Descripción:** Cada registro representa un segmento de calle que conecta dos intersecciones (nodos `u` y `v`). Entre las variables extraídas destacan `length` (distancia en metros), `name` (nombre de la calle) y `maxspeed` (límite de velocidad). Estos datos serán la base matemática para asignar el peso a nuestro grafo en el algoritmo de búsqueda de rutas.

## 3. Propuesta Metodológica

### 3.1. Objetivo
El objetivo principal de esta propuesta es construir un sistema de búsqueda de rutas similar a "Waze", capaz de encontrar el camino óptimo entre dos intersecciones dentro del distrito de L'Eixample y zonas aledañas de Barcelona, optimizando el tiempo de viaje según las condiciones de tráfico.

### 3.2. Metodología y Algoritmos
Para lograr el objetivo, la ciudad se ha representado matemáticamente como un **Grafo Dirigido Ponderado**, donde:
* **Vértices (Nodos):** Son las intersecciones de las calles.
* **Aristas (Edges):** Son los segmentos de calles que unen las intersecciones.

Para realizar la búsqueda de la ruta más corta, implementaremos en las siguientes fases del proyecto el **Algoritmo de Dijkstra**. Este algoritmo de camino mínimo es ideal para grafos ponderados con pesos positivos, garantizando encontrar la ruta óptima desde un nodo origen a un nodo destino evaluando los costos acumulados.

### 3.3. Diseño de la Función de Costo (Pesos)
Con el fin de simular un entorno real de conducción, el "peso" (costo de recorrido) de cada arista no es estático, sino dinámico. El peso de cada calle $e$ se calcula mediante la siguiente fórmula:

$$ Peso(e) = Longitud(e) \times FactorTrafico(h) $$

Donde:
* **Longitud(e):** Es la distancia geométrica real en metros del segmento de calle, obtenida a través de la API espacial.
* **FactorTrafico(h):** Es un multiplicador dinámico basado en la hora del día ($h$). Se ha diseñado una función en Python que clasifica el tráfico en:
  * **Hora Punta (Factor alto ~3.0):** De 07:00 a 09:00 y de 17:00 a 20:00 hrs.
  * **Horario Regular (Factor moderado ~1.5):** Horas diurnas restantes.
  * **Madrugada (Factor mínimo 1.0):** De 23:00 a 05:00 hrs, representando calles descongestionadas.

De esta manera, una ruta que físicamente es más corta pero se encuentra altamente congestionada, tendrá un peso total mayor, logrando que el algoritmo desvíe al usuario hacia una ruta más despejada pero ligeramente más larga, cumpliendo exactamente con la lógica de un sistema GPS moderno.

Referencias:

Adamo, T., Gendreau, M., Ghiani, G., y Guerriero, E. (2024). A review of recent advances in time-dependent vehicle routing. *European Journal of Operational Research*, *319*(1), 1-15. https://doi.org/10.1016/j.ejor.2024.06.016

Área Metropolitana de Barcelona. (2025). *Dades bàsiques de mobilitat, 2024*. https://hdl.handle.net/20.500.14439/485

Hrushka, V. V., Horozhankina, N. A., Boyko, Z. V., Korneyev, M. V., & Nebaba, N. A. (2021). Transport infrastructure of Spain as a factor in tourism development. *Journal of Geology, Geography and Geoecology, 30*(3), 429–440. https://doi.org/10.15421/112139