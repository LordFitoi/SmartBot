import re, random


class BotActions:
    """
    Esta clase se encarga de ejecutar acciones cuando se detecte una o varias etiquetas
    """

    botname_pattern = "BotName|Botname|botname"
    creatorname_pattern = "CreatorName|Creatorname|creatorname"
    current_action = None

    def add_bot_info(self, text: str) -> str:
        # Remplaza las KeyWords por la info del desarrollador
        text = re.sub(self.botname_pattern, self.name, text)
        text = re.sub(self.creatorname_pattern, self.creator, text)

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

    def keep_quiet(self):
        if random.uniform(0, 1) > self.config["KeepQuietProb"]:
            self.current_action = "KeepQuiet"
            self.state = "neutral"

    def talk_again(self):
        if random.uniform(0, 1) > self.config["TalkAgainProb"]:
            self.current_action = None
            self.state = "happy"

    def do_actions(self, text: str, user_data: dict) -> str:
        for tag in self.action_funcs:
            pattern = f"{tag}|{tag.capitalize()}|{tag.lower()}"
            if not re.search(pattern, text):
                continue

            self.action_funcs[tag]()
            break

        if self.current_action:
            text = self.current_action

        text = self.add_bot_info(text)
        text = self.get_last_msg(text, user_data)

        text = self.do_default(text, self.json_dict["default"])
        user_data["log"].append([text, text])

        return text
