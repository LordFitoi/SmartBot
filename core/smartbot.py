from core.tools.corpus_loader import CorpusLoader
from core.tools.naive_bayes_models import CNBChainModel
import os 

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

        
        output_length = self.config["OutputLength"]
        stemma_state_path = os.path.join(
            self.main_path, "core/tools/stemma_save.json"
        )

        self.generator = CNBChainModel(output_length, stemma_state_path)
        self.modules = [module(self) for module in module_list]

    def fit(self, text, user_id : str) -> None:
        log = self.user_data[user_id]["log"]
        if log:
            x_input = [log[-1][0], text]
            print(x_input)
            self.generator.train(x_input, partial = True)

    def __call__(self, text: str, user_id: str) -> str:

        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "log": [],
                "info": {},
                "state" : "happy",
                "current_action": None
            }

        user_data = self.user_data[user_id]
        
        output = text
        for module in self.modules:
            output = module.process(
                InputText=output,
                UserText=text,
                UserData=user_data)
            
        user_data["log"].append([text, output])
        return output
