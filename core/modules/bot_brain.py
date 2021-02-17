from core.tools.naive_bayes_models import CNBChainModel
from core.modules.bot_module import BotModule
import re, random, os


class BotBrain(BotModule):
    """Esta clase se encarga de aprender y generar texto"""

    def __init__(self, chatbot: object) -> None:
        self.chatbot = chatbot

        self.max_learn_range = 4

        corpus_name = self.chatbot.config["CorpusName"]
        output_length = self.chatbot.config["OutputLength"]
        stemma_state_path = os.path.join(
            self.chatbot.main_path, "core/tools/stemma_save.json"
        )

        self.generator = CNBChainModel(output_length, stemma_state_path)
        self.train(corpus_name)

    def add_match(self, text: str, label: str, pattern: str, user_data: dict) -> None:
        match = re.search(pattern, text.lower())
        if match:
            if not label in user_data:
                user_data[label] = []
            user_data[label].append(match.group(1))

            # Si supera el maximo de objetos aprendidos, olvida los mas viejos
            if len(user_data[label]) >= self.max_learn_range:
                user_data[label].pop(0)

    def learn(self, text: str, user_data: dict) -> None:
        for label in self.chatbot.json_dict["patterns"]:
            for pattern in self.chatbot.json_dict["patterns"][label]:
                self.add_match(text, label, pattern, user_data)

    def replace_labels(self, text: str, label_dict: dict) -> str:
        for label in label_dict:
            text_part = random.choice(label_dict[label])
            pattern = f"{label}|{label.capitalize()}|{label.lower()}"
            text = re.sub(pattern, text_part, text)

        return text

    def train(self, corpus_name: str) -> None:
        corpus_samples, self.chatbot.json_dict = self.chatbot.corpus_loader.load(
            corpus_name
        )
        self.generator.train_vectorizer(corpus_samples)
        self.generator.train(corpus_samples)

    def process(self, **kwargs) -> str:
        input_text = kwargs["InputText"]
        user_data = kwargs["UserData"]

        text = self.generator(input_text)
        self.learn(text, user_data["info"])

        if not re.search("[a-zA-Z]", text):
            text = "NoContext"

        text = self.replace_labels(text, self.chatbot.json_dict["structures"])
        text = self.replace_labels(text, user_data["info"])

        return text
