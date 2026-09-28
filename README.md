# Despachos de Procesos

Este repositorio contiene un simulador y visualizador de algoritmos de despacho de procesos, desarrollado en Python.

## Autores

Proyecto realizado por:

* Juan José González (juangonzalez22)
* Juan José Gálvez (juangalvez1)

## Descripción

El sistema permite simular la ejecución de un conjunto de procesos en la CPU. Lee los datos de entrada desde un archivo CSV y evalúa el comportamiento de diferentes algoritmos de planificación, generando una visualización de los resultados para facilitar su análisis.

## Algoritmos Implementados

La lógica de los algoritmos se encuentra en el directorio `/algorithms` e incluye:

* FIFO (First In, First Out)
* SJF (Shortest Job First)
* Round Robin
* Prioridad (Priority)

## Estructura del Proyecto

El código está organizado de la siguiente manera:

* `main.py`: Punto de entrada principal de la aplicación.
* `algorithms/`: Contiene los scripts con la lógica de cada algoritmo de planificación.
* `data/`: Directorio que almacena los datos de entrada, como el archivo `procesos.csv`.
* `utils/`: Herramientas auxiliares. Incluye `reader.py` para procesar el archivo CSV y `visualizer.py` para renderizar los resultados de los despachos.
