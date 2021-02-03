# SmartBot
Smartbot es un simple chatbot creado en Python con Sklearn

# Novedades
- Se elimino el clasificador de texto
- Se ha eliminado el modulo de Spacy, ahora funciona exclusivamente con Sklearn.
- Se añadio un archivo de configuracion.
- Se limpio y documento el codigo.

# ¿Como funciona?
SmartBot cuenta con un generador de texto basado en cadenas de modelos de Bayes, es decir son varios calsificadores de Bayes consecutivos y anidados entre si
con el objetivo de emular las propiedades de un modelo de Markov. Este recibe un texto de entrada que se reparte a todos los clasificadores y cada uno junto
a la salida del clasificador anterior da el trozo correspondiente de la parte del texto. El tamaño maximo de texto depende exclusivamente de cuantos modelos
encadenados se tenga. Tambien lo podemos expresar de la siguiente forma.

> <img src="https://render.githubusercontent.com/render/math?math=fn%20=%20NaiveBayesClassificator">

> <img src="https://render.githubusercontent.com/render/math?math=Wn%20=%20Word">

> <img src="https://render.githubusercontent.com/render/math?math=M%20=%20[f1,%20f2,%20%20...%20%20fn]">

> <img src="https://render.githubusercontent.com/render/math?math=fn(Vector(Context,%20Wn))=%20Wn+1">

> *Nota: Este modelo es meramente experimental.*


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

# ¿Como entreno al clasificador de texto?
En la carpeta "assets" se encuentra el archivo "open_talk.txt" el cual contiene los datos de entrenamiento.
**El dataset debe tener de manera consecutiva contexto y respuesta** para que el generador de texto aprenda a escribir.

# Requerimientos
- Scikit-learn
