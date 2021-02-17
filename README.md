# SmartBot
Smartbot es un chatbot creado en Python con Sklearn para Discord, el chatbot es capaz de aprender a semi-generar las respuestas, basado en las conversaciones que ha aprendido. 

# Novedades
- Se ha cambiado la arquitectura del bot, ahora funciona algo mas parecido a Chatterbot

# ¿Como puedo utilizarlo?
Para poder usar a SmartBot, es necesario haber creado una aplicacion/usuario bot en discord, posteriomente procedes a configurar, accediendo al archivo "config.json",
y por ultimo solo debes ejecutar el archivo "main.py"

# ¿Como funciona? y ¿Como puedo entrenarlo?
SmartBot cuenta con un generador de texto basado en cadenas de modelos de Bayes, es decir son varios calsificadores de Bayes consecutivos y anidados entre si
con el objetivo de emular las propiedades de un modelo de Markov.

Para entrenarlo, en la carpeta "assets/corpus" se encuentra un directiorio llamado "es" el cual contiene los datos de entrenamiento. Los archivos .txt son las las muestras de conversaciones a aprender por el bot, y los .json son archivos con patrones/respuestas que se utilizan en el codigo en casos especificos. Al entrenar el bot este carga todo los archivos del directorio.

> *Nota: Los archivos estas separados solo para que sea facil su edicion.*

# Interfaz de Discord
El bot cuenta con la api de discord.py es decir que el bot puede interactuar con el usuario atravez de discord. La interfaz del bot es un poco distinta al del usuario, esto con el objetivo de que sea algo mas estetico, llamativo y elegante. El bot tambien cuenta con la capacidad de representar sus estados de animo mediante el icono superio que sale alado del nombre del bot:
> <img src="https://media.discordapp.net/attachments/810336186010697748/811457193475964978/unknown.png">

Todo esto se puede modificar accediendo a la ruta "./assets/embeds", ahi encontra los archivos .json que se encargan de darle estructura a cada embed del bot.
El embed que utiliza el bot para los mensajes se llama "msg_container.json", por defecto solo cuenta con el footer. **El archivo "icon_urls.json" no forma parte de ningun embed, este archivo cuenta con las url de los iconos que representan cada estado del bot.** En caso de querer añadir alguno mas solo debe añadir una key y ponerle de valor la url de alguna imagen que desee, los estados se cargan automaticamente cuando la variable "state" de BotBody sea igual a la key de a la de alguna imagen.

# Configuracion
Para terminar de configurar su bot, solo debe de acceder al archivo "config.json", en este encontrara la configuracion basica, desde el corpus a utilizar, el nombre del creador que dira, el nombre con el cual se llamara asi mismo, el tamaño de la salida maxima y el token de la interfaz de discord.

# Requerimientos
- Scikit-learn
- Discord.py
