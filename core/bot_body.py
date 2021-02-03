from core.bot_brain import BotBrain
import os

class BotBody(BotBrain):
    """
    Esta clase sirve para unir todos los componentes del bot.
    """
    def __init__(self, bot_config : dict, main_path : str) -> None:
        self.name = bot_config["BotName"]
        self.creator = bot_config["CreatorName"]

        corpus_path = os.path.join(main_path, "assets/open_talk.txt")
        BotBrain.__init__(self, bot_config["OutputLength"], corpus_path)
    
    def __call__(self, text : str) -> str:
        response = self.predict(text).replace("botname", self.name)
        response = self.predict(text).replace("creatorname", self.creator)

        return response
