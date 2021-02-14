from core.bot_brain import BotBrain
from core.bot_actions import BotActions
from core.corpus_loader import CorpusLoader


class BotBody(BotBrain, BotActions, CorpusLoader):
    """
    Esta clase sirve para unir todos los componentes del bot.
    """

    def __init__(self, bot_config: dict, main_path: str) -> None:
        self.name = bot_config["BotName"]
        self.creator = bot_config["CreatorName"]
        self.main_path = main_path
        self.json_dict = {}

        self.state = "neutral"

        BotBrain.__init__(self, bot_config["OutputLength"], bot_config["CorpusName"])

    def __call__(self, text: str, user_data: dict) -> str:

        response = self.predict(text, user_data)
        response = self.do_actions(response, user_data)

        return response
