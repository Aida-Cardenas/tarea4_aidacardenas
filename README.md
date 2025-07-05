
## Archivos incluidos
- `markov_refuerzo.py`: Código principal del programa 
- `datos_ejemplo.csv`: Archivo de ejemplo para probar el programa.

## ¿Qué hace el programa?
1. **Carga un archivo CSV** con datos históricos (por ejemplo, clima y temperatura por día).
2. **Permite seleccionar la columna que representa el día** y define el resto como atributos del estado.
3. **Entrena un modelo de Markov**:
   - Inicializa las probabilidades de transición de manera uniforme
   - Recorre los datos y aumenta la probabilidad de transición entre estados consecutivos 
   - Calcula las probabilidades finales de transición entre estados.
4. **Muestra el modelo de Markov** (matriz de probabilidades de transición) en pantalla.
5. **Permite predecir el siguiente estado**: el usuario puede ingresar un estado actual y el programa predice el estado más probable siguiente según el modelo aprendido.

## Cómo usar el programa

### Interfaz Gráfica
1. Ejecuta el programa:
   ```
   python markov_refuerzo.py
   ```
2. Se abrirá una ventana con los siguientes pasos:
   - **Cargar CSV**: Haz clic y selecciona tu archivo de datos (puedes usar `datos_ejemplo.csv`).
   - **Seleccionar columna de día**: Elige la columna que representa el día en el desplegable.
   - **Entrenar Modelo**: Haz clic para entrenar el modelo de Markov. Se mostrará la matriz de probabilidades de transición.
   - **Predecir Siguiente Estado**: Haz clic, ingresa los valores actuales de los atributos y el programa mostrará el estado más probable siguiente.

Sigue las instrucciones en pantalla para cargar el archivo, seleccionar la columna de día y realizar predicciones.

## Ejemplo de datos (`datos_ejemplo.csv`)
```
Dia,Clima,Temperatura
1,Lluvia,Calor
2,Sol,Frio
3,Lluvia,Frio
4,Sol,Calor
5,Lluvia,Calor
6,Sol,Frio
7,Lluvia,Frio
8,Sol,Calor
```

## Notas importantes
- Solo se consideran transiciones entre días consecutivos (por ejemplo, del día 1 al 2, 2 al 3, etc.).
- El modelo utiliza todos los atributos excepto la columna de día para definir el estado.
- Si el estado ingresado para predecir no existe en el modelo, se mostrará una advertencia.
