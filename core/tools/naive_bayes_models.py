from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import ComplementNB
from core.tools.stemmatizer import Stemmatizer
import numpy as np
import joblib
import string
import json
import re



class CNBChainModel:
    """
    Este modelo es un experiento en el cual se intenta combinar la capacidad de seguir secuencias
    de una cadena de markov y las grandes capacidades de los clasificadores bayesianos, concretamente
    el Naive Bayes Complementario, para simular la capacidad de generar texto estructurado de la misma
    forma que sucederia en un modelo de Markov, pero con las ventajas que proporcionan los modelos de
    Machine Leaning a la hora del aprendizaje, dotandole la capacidad de escribir en base a contextos.

    Para ello se procede a enlazar N clasificadores para generar una cadena que se comportara como un
    modelo aun mas complejo.

    Entrenamiento: El dataset a utilizar debe estar organizado a pares (Contexto, Respuesta).
    Durante el entrenamiento se le pasa como entrada entrada del usuario y luego se vectoriza.
    Y para la salida se le pasa la palabra o token que vaya a predecir.
    """

    stemmatizer = Stemmatizer()
    vectorizer = TfidfVectorizer(strip_accents="ascii", ngram_range=(1, 1))
    punctuation = (
        string.punctuation[:22] + "¡¿"
    )  # Contiene todos los simbolos de puntuacion.

    def __init__(self, input_length: int, stemma_state_path: str) -> None:
        self.chain = [ComplementNB() for i in range(input_length)]
        if stemma_state_path:
            self.stemmatizer.load_model(stemma_state_path)
    
    def save_model(self, model_path, idf_path, vocab_path):
        joblib.dump(self.chain, model_path)
        joblib.dump(self.vectorizer.idf_, idf_path)
        
        with open(vocab_path, "w", encoding="utf-8") as jsonfile:
            json.dump(self.vectorizer.vocabulary_, jsonfile)
        
        print("@ Model Checkpoint Completed")

    def load_model(self, model_path, idf_path, vocab_path):
        try:
            self.chain = joblib.load(model_path)
            self.vectorizer.idf_ = joblib.load(idf_path)
            with open(vocab_path, "r", encoding="utf-8") as jsonfile:
                self.vectorizer.vocabulary_ = json.load(jsonfile)

            print("@ Model Checkpoint Loaded")
        except Exception as exception:
            print(exception)
            return True


    def format_input(self, text: str) -> str:
        """Permite limpiar el texto de entrada"""
        for symbol in self.punctuation:
            text = re.sub(f"[{symbol}]", f" {symbol} ", text.lower())

        text = re.sub(",", " ,", text)
        text = re.sub("\s+", " ", text)

        return re.sub("\n+", "", text)

    def format_output(self, token_list: list) -> str:
        text = token_list[0].capitalize()
        for i in range(len(token_list) - 1):
            if token_list[i + 1] in ",!?":
                text += f"{token_list[i + 1]} "
            elif re.search("\W", text[-1]):
                text += token_list[i + 1].capitalize()
            else:
                text += f" {token_list[i + 1]}"

        return text

    def get_tokens(self, documents: list) -> list:
        token_list = set(["END", ""])
        for sample in documents:
            word_sequence = self.format_input(sample).split()
            token_list = token_list.union(word_sequence)

        return list(token_list)
    
    def create_dataset(self, documents: list) -> list:
        """
        Crea un dataset tomando como entrada un context C de tal modo que Vector(C)
        sea el dato de entrada y W sea el dato de salida
        """

        x_input_list = [[] for n in range(len(self.chain))]
        y_input_list = [[] for n in range(len(self.chain))]

        for i in range(len(documents) - 1):
            if not documents[i].replace("\n", "") or not documents[i + 1].replace(
                "\n", ""
            ):
                continue
            context = documents[i]
            word_sequence = [""] + self.format_input(documents[i + 1]).split() + ["END"]

            for j in range(len(word_sequence) - 1):
                if j >= len(self.chain):
                    break

                stemma_text = self.get_text_stemma(context)

                x_input = self.vectorizer.transform([stemma_text])
                x_input = x_input.toarray()[0]

                x_input_list[j].append(x_input)
                y_input_list[j].append(word_sequence[j + 1])

        return x_input_list, y_input_list

    def get_text_stemma(self, text: str) -> str:
        text = re.sub("\W|\d|[_]|\s+", " ", text.lower())
        text = re.sub(r"(\w)\1*", r"\1", text)

        word_list = text.split()
        text_stemma = [self.stemmatizer.get_stemma(word) for word in word_list]
        text_stemma = " ".join([f"{root} {subfix}" for root, subfix in text_stemma])

        return text_stemma

    def train_vectorizer(self, documents: str) -> None:
        """Permite entrenar el vectorizador de texto"""
        stemma_docs = [self.get_text_stemma(sample) for sample in documents]
        self.vectorizer.fit(stemma_docs)

    def train(self, documents: list, partial = False) -> None:
        """Permite entrenar el modelo con los datos de entrenamientos creados previamente"""
        x_input_list, y_input_list = self.create_dataset(documents)
        if not partial:
            token_list = self.get_tokens(documents)

        for i in range(len(self.chain)):
            if not x_input_list[i] or not y_input_list[i]:
                break
            
            if not partial:
                self.chain[i].partial_fit(x_input_list[i], y_input_list[i], token_list)
            else:
                self.chain[i].partial_fit(x_input_list[i], y_input_list[i])

        print("@ Model Training Completed")

    def __call__(self, text: str) -> str:
        output = []
        current_word = ""

        stemma_text = self.get_text_stemma(text)

        for i, state in enumerate(self.chain):
            try:
                if current_word == "END":
                    break

                x_input = self.vectorizer.transform([stemma_text])

                output.append(state.predict(x_input.toarray())[0])
                current_word = output[-1]
            except Exception as exception:
                print(f"@ Error: {exception}")
        return self.format_output(output[:-1])
