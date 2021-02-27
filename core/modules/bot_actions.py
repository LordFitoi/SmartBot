from core.modules.bot_module import BotModule
import re, random


class BotActions(BotModule):
    """
    Esta clase se encarga de ejecutar acciones cuando se detecte una o varias etiquetas
    """

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot
        self.botname_pattern = "BotName|Botname|botname"
        self.creatorname_pattern = "CreatorName|Creatorname|creatorname"

        self.action_funcs = {
            "KeepQuiet": self.keep_quiet,
            "TalkAgain": self.talk_again,
        }

    def add_bot_info(self, text: str) -> str:
        # Remplaza las KeyWords por la info del desarrollador
        bot_name = self.chatbot.config["BotName"]
        creator_name = self.chatbot.config["CreatorName"]

        text = re.sub(self.botname_pattern, bot_name, text)
        text = re.sub(self.creatorname_pattern, creator_name, text)

        return text

    @staticmethod
    def do_default(text: str, label_dict: dict) -> str:
        # Si la respuesta contiene alguna Etiqueta de Default, devuelve un mensaje Default
        for label in label_dict:
            pattern = f"{label}|{label.capitalize()}|{label.lower()}"
            if re.search(pattern, text):
                text = random.choice(label_dict[label])
                break

        return text

    @staticmethod
    def get_last_msg(text: str, user_data: dict) -> str:
        # Remplaza la keyword "UserLastMsg" por el ultimo mensaje del usuario
        if user_data["log"]:
            text = text.replace("UserLastMsg", user_data["log"][-1][0])

        elif "UserLastMsg" in text:
            text = "RememberText"

        return text

    def keep_quiet(self, user_data : dict):
        if random.uniform(0, 1) < self.chatbot.config["KeepQuietProb"]:
            user_data["state"] = "neutral"
            user_data["current_action"] = "KeepQuiet"

    def talk_again(self, user_data : dict):
        if random.uniform(0, 1) <= self.chatbot.config["TalkAgainProb"]:
            user_data["state"] = "happy"
            user_data["current_action"] = None

    def process(self, **kwargs) -> str:
        input_text = kwargs["InputText"]
        user_data = kwargs["UserData"]

        text = input_text
        for tag in self.action_funcs:
            pattern = f"{tag}|{tag.capitalize()}|{tag.lower()}"
            if not re.search(pattern, text):
                continue

            self.action_funcs[tag](user_data)
            break

        if user_data["current_action"]:
            text = user_data["current_action"]

        text = self.add_bot_info(text)
        text = self.get_last_msg(text, user_data)

        text = self.do_default(text, self.chatbot.json_dict["default"])
  
        return text
