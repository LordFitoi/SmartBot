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
        self.json_dict = {}

        BotBrain.__init__(self, bot_config["OutputLength"], bot_config["CorpusName"])

    def __call__(self, text: str, user_data: dict) -> str:
        response = self.predict(text, user_data)

        # Remplaza las KeyWords por la info del desarrollador
        response = response.replace("botname", self.name)
        response = response.replace("creatorname", self.creator)

        # Remplaza la keyword "UserLastMsg" por el ultimo mensaje del usuario
        if user_data["log"]:
            response = response.replace("userlastmsg", user_data["log"][-1][0])

        # Si la respuesta contiene alguna Etiqueta de Default, devuelve un mensaje Default
        response = self.default_response(response, self.json_dict["default"])
        user_data["log"].append([text, response])

        return response.capitalize()
