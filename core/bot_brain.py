from core.naive_bayes_models import CNBChainModel
import re, random

class BotBrain:
    def __init__(self, output_length : int, corpus_path : str) -> None:
        self.generator = CNBChainModel(output_length)
        self.train(corpus_path)
        self.log = []

    def add_match(self, text : str, label : str, pattern : str, user_data : dict) -> None:
        match = re.search(pattern, text.lower())
        if match:
            if not label in user_data:
                user_data[label] = []
            user_data[label].append(match.group(1))
    
    def learn(self, text : str, user_data : dict) -> None:
        for label in self.pattern_list:
            for pattern in self.pattern_list[label]:
                self.add_match(text, label, pattern, user_data)

    def replace_labels(self, text : str, label_dict : dict) -> str:
        for label in label_dict:
            text = text.replace(
                label.lower(),
                random.choice(label_dict[label])
            )
        return text.lower()

    def train(self, corpus_path : str) -> None:
        with open(corpus_path, "r", encoding="utf-8") as text_file:
            documents = text_file.readlines()
            self.generator.train_vectorizer(documents)
            self.generator.train(documents)

    def predict(self, text : str, user_data : str) -> str:
        response = self.generator(text)
        response = self.replace_labels(response, self.structure_list)
        response = self.replace_labels(response, user_data)

        if not re.search('[a-zA-Z]', response):
            response = "#NoText"

        self.learn(text, user_data)
        return response
      
