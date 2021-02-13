# SmartBot
Smartbot es un chatbot creado en Python con Sklearn para Discord, el chatbot es capaz de aprender a semi-generar las respuestas, basado en las conversaciones que ha aprendido. 

# Novedades
- Se han eliminado algunos archivos obsoletos.
- Se limpiado y documentado mejor el codigo.

# ¿Como funciona?
SmartBot cuenta con un generador de texto basado en cadenas de modelos de Bayes, es decir son varios calsificadores de Bayes consecutivos y anidados entre si
con el objetivo de emular las propiedades de un modelo de Markov. Este recibe un texto de entrada que se reparte a todos los clasificadores y cada uno junto
a la salida del clasificador anterior da el trozo correspondiente de la parte del texto. El tamaño maximo de texto depende exclusivamente de cuantos modelos
encadenados se tenga. Tambien lo podemos expresar de la siguiente forma.

> <img src="https://render.githubusercontent.com/render/math?math=fn%20=%20NaiveBayesClassificator">

> <img src="https://render.githubusercontent.com/render/math?math=Wn%20=%20Word">

> <img src="https://render.githubusercontent.com/render/math?math=M%20=%20[f1,%20f2,%20%20...%20%20fn]">

> <img src="https://render.githubusercontent.com/render/math?math=fn(Vector(Context,%20Wn))=%20Wn">

> *Nota: Este modelo es meramente experimental.*


Para recalcar, Smarthbot cuenta con la capacidad de reconocer patrones usando RegEx, lo que le permite recopilar informacion especifica que luego puede ser usada.
Tambien un sistema para remplazar etiquetas que hayamos creado, por respuestas asignadas a dicha etiqueta.


Ejemplo de preprocesamiento:
```
¿Estas jugando a Minecraft? -> ¿ estar jugar a minecraft ?
Te gusta comer chocolate -> te gustar comer chocolate
¿Quién eres? -> ¿ quién ser ?
```

Para poder probarlo, solo necesitas correr el archivo "main.py", y para poder obtener una
respuesta del bot solo necesitas instanciar la clase BotBody y hacer un simple call del
objeto pasando el texto del usuario.

```python
Bot = BotBody()
print(Bot("¿Por quien fuiste creado?")) # Output -> "Mi creador es WaffleFitoi"
```

# ¿Como puedo entrenarlo?
En la carpeta "assets/corpus" se encuentra un directiorio llamado "es" el cual contiene los datos de entrenamiento. Los archivos .txt son las las muestras de conversaciones a aprender por el bot, y los .json son archivos con patrones/respuestas que se utilizan en el codigo en casos especificos. Al entrenar el bot este carga todo los archivos del directorio.

Para cargar un corpus personalizado, solo debes acceder al archivo "config.json" en la carpeta principal y editar el parametro "CorpusName" colocando el nombre de tu corpus.

Si quieres usar alguna informacion dentro de los archivos .json cargados, solo debes llamar la variable, structure_list dentro de cualquier complemento heredado en el modulo de BotBody, y pasarle el nombre del archivo .json como key, de este modo obtendras la informacion obtenida de dicho corpus

> *Nota: Los archivos estas separados solo para que sea facil su edicion.*

# Requerimientos
- Scikit-learn
- Discord.py
