from core.bot_brain import BotBrain
from core.corpus_loader import CorpusLoader


class BotBody(BotBrain, CorpusLoader):
    """
    Esta clase sirve para unir todos los componentes del bot.
    """

    def __init__(self, bot_config: dict, main_path: str) -> None:
        self.name = bot_config["BotName"]
        self.creator = bot_config["CreatorName"]
        self.main_path = main_path
        self.structure_dict = {}

        BotBrain.__init__(self, bot_config["OutputLength"], bot_config["CorpusName"])

    def __call__(self, text: str, user_data: dict) -> str:
        response = self.predict(text, user_data).replace("botname", self.name)
        response = response.replace("creatorname", self.creator)

        if user_data["log"]:
            response = response.replace("userlastmsg", user_data["log"][-1][0])

        response = self.default_response(response, self.structure_dict["responses"])
        user_data["log"].append([text, response])

        return response.capitalize()
