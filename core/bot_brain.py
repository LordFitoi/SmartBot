from core.gaussian_models import GaussianChainModel
import re

class BotBrain:
    def __init__(self, output_length : int, corpus_path : str) -> None:
        self.generator = GaussianChainModel(output_length)
        self.train(corpus_path)

    def train(self, corpus_path : str) -> None:
        with open(corpus_path, "r", encoding="utf-8") as text_file:
            documents = text_file.readlines()
            self.generator.train_vectorizer(documents)
            self.generator.train(documents)


    def predict(self, text : str) -> str: 
        return self.generator(text)
      
