from core.bot_body import BotBody
import discord, json, os

main_path = os.path.dirname(__file__)

""" Load Bot Configurations """
config_path = os.path.join(main_path, "config.json")
with open(config_path, "r") as jsonfile:
    bot_config = json.load(jsonfile)

BotUser = BotBody(bot_config, main_path)
class BotClient(discord.Client):
    @staticmethod
    def is_DMChannel(message):
        return isinstance(message.channel, discord.channel.DMChannel)

    async def send_response(self, message):
            response = BotUser(message.content)
            
            print(f"{message.author}: {message.content}")
            print(f"@ Bot: {response}")
            
            if response: await message.channel.send(response)

    async def on_ready(self) -> None:
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message : object) -> None:
        if not message.author.bot and self.is_DMChannel(message):
            await self.send_response(message)

if __name__ == "__main__":
    BotClient().run(bot_config["BotToken"])
