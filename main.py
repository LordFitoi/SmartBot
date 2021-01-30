from core.bot_brain import BotBrain
import os, random

class BotBody(BotBrain):
    main_path = os.path.dirname(__file__)
    def __init__(self):
        BotBrain.__init__(self, self.main_path)
    
    def __call__(self, text : str) -> str:
        return self.predict(text)


"""
Mini chat improvisado, eliminar cuando se vaya a usar con APIs de interfaz.
"""
bot = BotBody()
while True:
    text = input(">> ")
    if text.lower() == "exit": break
    else: print(f"Bot: {bot(text)}")