from core.bot_brain import BotBrain
import os, json

class BotBody(BotBrain):
    """
    Esta clase sirve para unir todos los componentes del bot.
    """
    def __init__(self, bot_config : dict, main_path : str) -> None:
        self.name = bot_config["BotName"]
        self.creator = bot_config["CreatorName"]

        corpus_path = os.path.join(main_path, "assets/open_talk.txt")
        BotBrain.__init__(self, bot_config["OutputLength"], corpus_path)

        structures_path = os.path.join(main_path, "assets/structures.json")
        with open(structures_path, "r") as jsonfile:
            self.structure_list = json.load(jsonfile)

        patterns_path = os.path.join(main_path, "assets/patterns.json")
        with open(patterns_path, "r") as jsonfile:
            self.pattern_list = json.load(jsonfile)


    def __call__(self, text : str, user_data : dict) -> str:
        response = self.predict(text, user_data).replace("botname", self.name)
        response = response.replace("creatorname", self.creator)

        return response.capitalize()
