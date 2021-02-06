# Objetivo:
El objetivo de SmartBot es crear un chatbot inteligente utilizando algoritmos de Machine Learning y NLP para la interfaz de discord, lo mas compacto pero funcional posible. De momento el Bot solo se limitara a utilizar Sklearn y Discord.py, en caso de querer utilizar mas modulos, primero contacteme en discord WaffleFitoi#6492, para discutir sobre la direccion del proyecto.

# Como contribuir "Codigo":
Contribuir al proyecto es muy sencillo, solo requiere de descargar el Repositorio y proceder a editarlo, las factores a tomar en cuenta son:
- Solo se utilizara Sklearn como algoritmo de Machine Learning, el objetivo es mantener un proyecto lo mas compacto posible.
- Limpiar la estructura del codigo usando el modulo de Black.py.
- Los commits deben estar en una rama por separada de la principal.

# Formato de Commits:
Los commits deben por obligacion llevar un mensaje/titulo con el siguiente formato:
"Update #DiaMesAñoLetra; Titulo", La letra es para indicar que version del dia se esta subiendo, v

Ejemplos: 
- Update #060221A; Wikipedia Api added.
- Update #060221B; Math Equations.
- Update #070321A; Moderator Commands.

# Como contribuir "Corpus":
Para contribuir en el corpus es muy sencillo, solo debes ir a la carpeta "assets/corpus" y ahi estaran todos los corpus creados hasta el momento para el bot, **dentro de cada corpus se encuentra un conjunto de archivos .txt y .json**. Los archivos .txt contienen ejemplos de conversacion para que el Bot aprenda mientras que los .json contienen Etiquetas los cuales se remplazaran por una de las oraciones aleatorias que contenga, si este la escribe.

Para escribir un ejemplo de conversacion solo tienes que escribir los mensajes por pares siendo el mensaje A el contexto y el B la respuesta que el Bot debe de decir. **Actualmente el bot usa un modelo que encadena varios clasificadores de NaiveBayes para podre crear un modelo capaz de semi-generar el texto**. Si quiere crear un corpus personalizado (Ejemplo un corpus en ingles), no hay problema con ello, solo asegurese de que contenga los tres archivos .json

> *Nota: En caso de haber una linea en vacia entre cada par de muestra, el Bot simplemente lo ignorara y seguira con la siguiente.*


Att - LordFitoi


