from core.bot_body import BotBody
import discord, json, os
import datetime

main_path = os.path.dirname(__file__)

""" Load Bot Configurations """
config_path = os.path.join(main_path, "config.json")
with open(config_path, "r") as jsonfile:
    bot_config = json.load(jsonfile)

BotUser = BotBody(bot_config, main_path)
class BotClient(discord.Client):
    user_data = {}

    @staticmethod
    def is_DMChannel(message):
        return isinstance(message.channel, discord.channel.DMChannel)

    def save_log(self, response, message):
        date = datetime.datetime.now()
        file_path = os.path.join(main_path, f"assets/log/{date.strftime('%d%b%y')}.txt")
        with open(file_path, "a", encoding="utf-8") as text_file:
            text_file.write(f"{message.content}\n{response}\n")
        
    async def send_response(self, message):
            if message.author.id not in self.user_data:
                self.user_data[message.author.id] = {}

            response = BotUser(
                message.content,
                self.user_data[message.author.id]
            )

            self.save_log(response, message)

            print(f"{message.author}: {message.content}")
            print(f"@ Bot: {response}")
            
            if response and response != "#notext":
                await message.channel.send(response)

    async def on_ready(self) -> None:
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message : object) -> None:
        if not message.author.bot and self.is_DMChannel(message):
            await self.send_response(message)

if __name__ == "__main__":
    BotClient().run(bot_config["BotToken"])
