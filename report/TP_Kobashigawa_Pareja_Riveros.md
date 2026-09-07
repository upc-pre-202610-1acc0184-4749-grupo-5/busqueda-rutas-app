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