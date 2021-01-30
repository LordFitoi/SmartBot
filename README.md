# SmartBot
Smartbot es un simple chatbot creado en Python con Sklearn y Spacy

# ¿Como funciona?
Smartbot calcula la similitud vectorial (Similitud de Coseno) para poder indentificar
cuales respuestas son las mas apropiadas a la hora de responder, ademas de ello hace un
preprocesamiento en el cual lematiza cada texto de entrada y las muestras guardadas en su
memoria de entrenamiento para poder reducir cualquier ruido que produsca las palabras con
prefijos y sufijos distintos o que sean de la misma familia mas no esten escritas de la
misma forma.

Para poder probarlo, solo necesitas correr el archivo "main.py", y para poder obtener una
respuesta del bot solo necesitas instanciar la clase BotBody y hacer un simple call del
objeto pasando el texto del usuario.

```python
Bot = BotBody()
print(Bot("¿Por quien fuiste creado?")) # Output -> "Mi creador es WaffleFitoi"
```

# ¿Como entrenarlo?
En la carpeta "assets" se encuentra un archivo .txt el cual contiene los datos de entrenamiento.
El dataset utiliza el siguiente format:
- El asterisco al principio del texto, indica una entrada esperada de parte del usuario.
- Los textos sin asterisco al principio son las respuestas del bot.
- Las etiquetas usan el formato de #"Etiqueta":, no tienen ninguna funcion, solo son para marcar.

> *Nota: Tambien durante la conversacion el bot ira aprendiendo las respuestas del usuario.*

# Requerimientos
- Scikit-learn
- Spacy
- Spacy model "es_core_news_sm"
