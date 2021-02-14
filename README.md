# SmartBot
Smartbot es un chatbot creado en Python con Sklearn para Discord, el chatbot es capaz de aprender a semi-generar las respuestas, basado en las conversaciones que ha aprendido. 

# Novedades
- Se ha añadido compatibilidad con Docker
- Se han añadido herramientas para la interfaz de discord (Carga de embeds y mas)

# ¿Como funciona?
SmartBot cuenta con un generador de texto basado en cadenas de modelos de Bayes, es decir son varios calsificadores de Bayes consecutivos y anidados entre si
con el objetivo de emular las propiedades de un modelo de Markov. Este recibe un texto de entrada que se reparte a todos los clasificadores, y cada uno da el trozo correspondiente de la parte del texto. El tamaño maximo de texto depende exclusivamente de cuantos modelos
encadenados se tenga. Tambien lo podemos expresar de la siguiente forma.

> <img src="https://render.githubusercontent.com/render/math?math=fn%20=%20NaiveBayesClassificator">

> <img src="https://render.githubusercontent.com/render/math?math=Wn%20=%20Word">

> <img src="https://render.githubusercontent.com/render/math?math=M%20=%20[f1,%20f2,%20%20...%20%20fn]">

> <img src="https://render.githubusercontent.com/render/math?math=fn(Vector(Context))=%20Wn">

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

# Interfaz de Discord
El bot cuenta con la api de discord.py es decir que el bot puede interactuar con el usuario atravez de discord. La interfaz del bot es un poco distinta al del usuario, esto con el objetivo de que sea algo mas estetico, llamativo y elegante:
> <img src="https://media.discordapp.net/attachments/810336186010697748/810586527314214912/unknown.png">

El bot tambien cuenta con la capacidad de representar sus estados de animo mediante el icono superio que sale alado del nombre del bot:
> <img src="https://cdn.discordapp.com/attachments/810336186010697748/810587854820212846/unknown.png">

Todo esto se puede modificar accediendo a la ruta "./assets/embeds", ahi encontra los archivos .json que se encargan de darle estructura a cada embed del bot.
El embed que utiliza el bot para los mensajes se llama "msg_container.json", por defecto solo cuenta con el footer. **El archivo "icon_urls.json" no forma parte de ningun embed, este archivo cuenta con las url de los iconos que representan cada estado del bot.** En caso de querer añadir alguno mas solo debe añadir una key y ponerle de valor la url de alguna imagen que desee, los estados se cargan automaticamente cuando la variable "state" de BotBody sea igual a la key de a la de alguna imagen.

# Configuracion
Para terminar de configurar su bot, solo debe de acceder al archivo "config.json", en este encontrara la configuracion basica, desde el corpus a utilizar, el nombre del creador que dira, el nombre con el cual se llamara asi mismo, el tamaño de la salida maxima y el token de la interfaz de discord.

# Requerimientos
- Scikit-learn
- Discord.py
