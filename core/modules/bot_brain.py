from core.modules.bot_module import BotModule
import re, random, os


class BotBrain(BotModule):
    """Esta clase se encarga de aprender y generar texto"""

    def __init__(self, chatbot: object) -> None:
        self.chatbot = chatbot
        self.max_learn_range = 4

        corpus_name = self.chatbot.config["CorpusName"]   
        self.train(corpus_name)

    def add_match(self, text: str, label: str, pattern: str, user_data: dict) -> None:
        match = re.search(pattern, text.lower())
        if match:
            if not label in user_data:
                user_data[label] = []
            user_data[label].append(match.group(1))

            if len(user_data[label]) >= self.max_learn_range:
                user_data[label].pop(0)

    def learn(self, text: str, user_data: dict) -> None:
        for label in self.chatbot.json_dict["patterns"]:
            for pattern in self.chatbot.json_dict["patterns"][label]:
                self.add_match(text.lower(), label, pattern, user_data)

    def replace_labels(self, text: str, label_dict: dict) -> str:
        for label in label_dict:
            text_part = random.choice(label_dict[label])
            pattern = f"{label}|{label.capitalize()}|{label.lower()}"
            text = re.sub(pattern, text_part, text)

        return text

    def train(self, corpus_name: str) -> None:
        model_path = os.path.join(self.chatbot.main_path, "core/save/model.sav")
        idf_path = os.path.join(self.chatbot.main_path, "core/save/idf.sav")
        vocab_path = os.path.join(self.chatbot.main_path, "core/save/vocab.json")

        not_trained = self.chatbot.generator.load_model(model_path, idf_path, vocab_path)

        corpus_samples, self.chatbot.json_dict = self.chatbot.corpus_loader.load(
            corpus_name, not_trained 
        )

        if not_trained:
            self.chatbot.generator.train_vectorizer(corpus_samples)
            self.chatbot.generator.train(corpus_samples)

            self.chatbot.generator.save_model(model_path, idf_path, vocab_path)


    def process(self, **kwargs) -> str:
        input_text = kwargs["InputText"]
        user_text = kwargs["UserText"]
        user_data = kwargs["UserData"]

        text = self.chatbot.generator(input_text)
        self.learn(user_text, user_data["info"])

        if not re.search("[a-zA-Z]", text):
            text = "NoContext"

        text = self.replace_labels(text, self.chatbot.json_dict["structures"])
        text = self.replace_labels(text, user_data["info"])

        return text
