from core.naive_bayes_models import CNBChainModel
import re, random, os


class BotBrain:
    def __init__(self, output_length: int, corpus_name: str) -> None:
        stemma_state_path = os.path.join(self.main_path, "core/stemma_save.json")
        self.generator = CNBChainModel(output_length, stemma_state_path)
        self.train(corpus_name)

    def add_match(self, text: str, label: str, pattern: str, user_data: dict) -> None:
        match = re.search(pattern, text.lower())
        if match:
            if not label in user_data:
                user_data[label] = []
            user_data[label].append(match.group(1))

    def learn(self, text: str, user_data: dict) -> None:
        for label in self.json_dict["patterns"]:
            for pattern in self.json_dict["patterns"][label]:
                self.add_match(text, label, pattern, user_data)

    def replace_labels(self, text: str, label_dict: dict) -> str:
        for label in label_dict:
            text = text.replace(label.lower(), random.choice(label_dict[label]))
        return text.lower()

    def default_response(self, text: str, label_dict: dict) -> str:
        for label in label_dict:
            if label.lower() in text:
                text = random.choice(label_dict[label])
                break

        return text.lower()

    def train(self, corpus_name: str) -> None:
        corpus_samples = self.load_corpus(corpus_name)
        self.generator.train_vectorizer(corpus_samples)
        self.generator.train(corpus_samples)

    def predict(self, text: str, user_data: str) -> str:

        response = self.generator(text)

        # Recolecta informacion dada por el usuario
        self.learn(text, user_data["info"])

        # Si no encuentra caracteres de texto, remplaza el resultado por la etiqueta "NoContext"
        if not re.search("[a-zA-Z]", response):
            response = "NoContext"

        # Remplaza las Etiquetas de "Structuras" por una de sus respuestas equivalentes
        response = self.replace_labels(response, self.json_dict["structures"])

        # Remplaza las Etiquetas de "Patrones" por la informacion obtenida del usuario
        response = self.replace_labels(response, user_data["info"])

        return response
