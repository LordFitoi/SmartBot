from core.tools.corpus_loader import CorpusLoader


class SmartBot:
    """
    Esta clase sirve para unir todos los componentes del bot.
    """

    def __init__(self, bot_config: dict, module_list: list, main_path: str) -> None:
        self.name = bot_config["BotName"]
        self.creator = bot_config["CreatorName"]

        self.config = bot_config

        self.corpus_loader = CorpusLoader(main_path)
        self.main_path = main_path
        self.json_dict = {}
        self.user_data = {}

        self.state = "happy"

        self.modules = [module(self) for module in module_list]

    def __call__(self, text: str, user_id: str) -> str:

        if user_id not in self.user_data:
            self.user_data[user_id] = {"log": [], "info": {}}

        user_data = self.user_data[user_id]
        output = text
        for module in self.modules:
            output = module.process(InputText=output, UserData=user_data)

        return output
