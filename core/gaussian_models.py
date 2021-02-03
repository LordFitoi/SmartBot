from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import GaussianNB
import re, string


class GaussianChainModel:
    """
    Este modelo es un experiento en el cual se intenta combinar la capacidad de seguir secuencias
    de una cadena de markov y las grandes capacidades de los clasificadores bayesianos, concretamente
    el Gaussiano, para simular la capacidad de generar texto estructurado de la misma forma que sucederia
    en un modelo de Markov, pero con las ventajas que proporcionan los modelos de Machine Leaning a la
    hora del aprendizaje, dotandole la capacidad de escribir en base a contextos.

    Para ello se procede a enlazar N clasificadores para generar una cadena que se comportara como un
    modelo aun mas complejo.

    Entrenamiento: El dataset a utilizar debe estar organizado a pares (Contexto, Respuesta).
    Durante el entrenamiento se le pasa como entrada la salida del clasificador "N - 1" junto a la
    entrada del usuario y luego se vectoriza. Y para la salida se le pasa la palabra o token que
    vaya a predecir.

    """
    vectorizer = TfidfVectorizer(strip_accents="ascii")
    punctuation = string.punctuation[:22] + "¡¿" # Contiene todos los simbolos de puntuacion.
    max_train_length = 0 # Indica hasta que parte del modelo ha sido entrenado.

    def __init__(self, input_length : int) -> None:
        self.chain = [GaussianNB() for i in range(input_length)]
    
    def format(self, text : str) -> str:
        """Permite limpiar el texto de entrada"""
        for symbol in self.punctuation:
            text = re.sub(f"[{symbol}]", f" {symbol} ", text.lower())

        text = re.sub(",", " ,", text)
        text = re.sub("\s+", " ", text)

        return re.sub("\n+", "", text)
        

    def create_dataset(self, documents : list) -> list:
        """
        Crea un dataset tomando como entrada una secuencia de palabras W y un context C
        de tal modo que Vector(C + Wn) sea el dato de entrada y Wn+1 sea el dato de salida
        """
        blocked_list = [[] for n in range(len(self.chain))]
        x_input_list = [[] for n in range(len(self.chain))]
        y_input_list = [[] for n in range(len(self.chain))]

        for i in range(len(documents) - 1):
            if not documents[i].replace("\n", "") or not documents[i+1].replace("\n", ""): continue
            context = documents[i]
            word_sequence = [""]+self.format(documents[i+1]).split() + ["END"]

            for j in range(len(word_sequence)-1):
                if j >= len(self.chain): break
                x_input = self.vectorizer.transform([f"{word_sequence[j]} {context}"])
                x_input = x_input.toarray()[0]

                term_x_input = list(self.vectorizer.inverse_transform(x_input)[0])
                if term_x_input not in blocked_list[j]:
                    x_input_list[j].append(x_input)
                    y_input_list[j].append(word_sequence[j + 1])
                    blocked_list[j].append(term_x_input)
            
        return x_input_list, y_input_list

    def train_vectorizer(self, documents : str) -> None:
        """Permite entrenar el vectorizador de texto"""
        self.vectorizer.fit(documents)

    def step_train(self, documents : list) -> None:
        """Permite entrenar el modelo durante la ejecucion"""
        x_input_list, y_input_list = self.create_dataset(documents)

        for i in range(len(self.chain)):
            if not x_input_list[i] or not y_input_list[i]: break
            self.chain[i].partial_fit(x_input_list[i], y_input_list[i])
            self.max_train_length = i

    def train(self, documents : list) -> None:
        """Permite entrenar el modelo con los datos de entrenamientos creados previamente"""
        x_input_list, y_input_list = self.create_dataset(documents)

        for i in range(len(self.chain)):
            if not x_input_list[i] or not y_input_list[i]: break
            self.chain[i].fit(x_input_list[i], y_input_list[i])
            self.max_train_length = i

        print("@ Model Training Completed")

    def __call__(self, text : str) -> str:
        output = []
        current_word = ""
        for i, state in enumerate(self.chain):
            if current_word == "END" or i > self.max_train_length: break
            x_input = self.vectorizer.transform([f"{current_word} {text}"])

            output.append(state.predict(x_input.toarray())[0])
            current_word = output[-1]

        return " ".join(output[:-1])
