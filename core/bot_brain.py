from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import re
import os

"""
Nota: El dataset utilizado es de muestra, el formato a utilizar,
los * al principio, indican las entradas esperadas del usuario,
las etiquetas siguen el formato de #"Nombre": y solo sirven para
marcar, no tienen ninguna utilidad extra.
"""


class BotBrain:
    tagger = spacy.load("es_core_news_sm") # Una vez listo, cambiar por el modelo "es_core_news_md"
    response_list = {
        "user_sentence" : [],
        "bot_sentence" : []
    }
    last_response = "NoContext"

    def __init__(self, main_path : str) -> None:
        file_path = os.path.join(main_path, "assets/dataset.txt")
        self.train(file_path)

    def format_document(self, text : str) -> str:
        new_text = re.sub("#(.*):", "", text.lower())
        new_text = re.sub("\n+","\n", new_text)
        return new_text.strip()

    def train(self, file_path : str) -> None:
        with open(file_path, "r", encoding="utf-8") as text_file:
            document = text_file.read().strip()
        
        untagged_document = self.format_document(document)
        for pair in untagged_document.split("*"):
            if not "\n" in pair: continue
            text_list = pair.split("\n")
            text_doc = list(self.tagger(text_list[0]).sents)

            self.response_list["user_sentence"].append(text_doc[0].lemma_)
            self.response_list["bot_sentence"].append(text_list[1].strip())

    def get_best_match(self, text_vector : object) -> tuple:
        similarity_vector = cosine_similarity(
            text_vector[-1],
            text_vector
        ).flatten()

        tagged_vector = sorted(list(enumerate(similarity_vector)),
            key = lambda item: item[1])[:-1]

        return tagged_vector[-1]
    
    def learn(self, text : str) -> None:
        text_lemma = [sentence for sentence in self.tagger(self.last_response).sents][0].lemma_
        self.response_list["user_sentence"].append(text_lemma)
        self.response_list["bot_sentence"].append(text)
    
    def predict(self, text : str) -> str:
        # Lematizamos el texto de entrada y lo incluimos a la lista de textos aprendidos (Temporal).
        text_lemma = [sentence for sentence in self.tagger(text).sents][0].lemma_
        lemma_text_list = self.response_list["user_sentence"] + [text_lemma]
        
        # Vectorizamos el texto y calculamos el valor mas parecido al texto de entrada.
        text_vector =  CountVectorizer().fit_transform(lemma_text_list)
        best_match = self.get_best_match(text_vector)
        
        # Obtenemos la respuesta utilizando el BestMatch
        response = self.response_list["bot_sentence"][best_match[0]].capitalize()
        
        # Extra: Aprende una respuesta nueva.
        if self.last_response: self.learn(text)
        self.last_response = response

        return response
