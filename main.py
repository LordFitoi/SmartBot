import discord, json, os
import datetime, random, time

main_path = os.path.dirname(__file__)

""" Load Bot Configurations """
config_path = os.path.join(main_path, "config.json")
with open(config_path, "r") as jsonfile:
    bot_config = json.load(jsonfile)


from core.smartbot import SmartBot
from core.modules.bot_brain import BotBrain
from core.modules.bot_actions import BotActions

bot_modules = [BotBrain, BotActions]
ChatBot = SmartBot(bot_config, bot_modules, main_path)


class BotClient(discord.Client):
    @staticmethod
    def is_DMChannel(message: str) -> bool:
        """Verifica si es un mensaje proveniente es de un canal privado"""
        return isinstance(message.channel, discord.channel.DMChannel)

    def save_log(self, response: str, message: object) -> None:
        """Guarda el historial de conversacion"""
        date = datetime.datetime.now()
        file_path = os.path.join(main_path, f"assets/log/{date.strftime('%d%b%y')}.txt")
        with open(file_path, "a", encoding="utf-8") as text_file:
            text_file.write(f"{message.content}\n{response}\n")

    def load_content(self, name: str) -> dict:
        """Carga contenido .json de la carpeta embeds"""
        embed_path = os.path.join(main_path, f"assets/embeds/{name}.json")
        with open(embed_path, "r", encoding="utf-8") as jsonfile:
            content = json.load(jsonfile)

        return content

    def create_embed(self, content: dict) -> object:
        """Crea un embed basado en el contenido de un diccionario"""
        embed = discord.Embed(
            title=content["title"],
            description=content["description"],
            color=int(content["color"], 16),
        )

        embed.set_thumbnail(url=content["icon_url"])

        for key, value in content["content"].items():
            embed.add_field(name=key, value=value, inline=content["inline"])

        embed.set_footer(text=content["footer"])

        return embed

    def create_response(self, message: object) -> list:
        """Crea una respuesta en base al mensaje, y le da formato usando embeds"""

        response = ChatBot(message.content, str(message.author.id))
        if response != "#NoText":
            embed_content = self.load_content("msg_container")

            face_images = self.load_content("icon_urls")
            if ChatBot.state in face_images:
                embed_content["icon_url"] = face_images[ChatBot.state]
            else:
                embed_content["icon_url"] = random.choice(list(face_images.values()))

            embed_content["description"] = f"`{response}`"
            embed = self.create_embed(embed_content)
        else:
            embed = None
        return response, embed

    async def send_response(self, message: object, is_server=False) -> None:
        """Envia una respuesta por el canal de proveniencia del mensaje."""
        response, embed = self.create_response(message)
        self.save_log(response, message)
        print(f"{message.author}: {message.content}")
        print(f"@ Bot: {response}")

        if response and response != "#notext" and embed:
            if is_server:
                await message.reply(embed=embed)
            else:
                await message.channel.send(embed=embed)

    async def on_ready(self) -> None:
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message: object) -> None:
        if not message.author.bot:
            if self.is_DMChannel(message):
                await self.send_response(message)

            elif not self.is_DMChannel(message) and self.user in message.mentions:
                await self.send_response(message, is_server=True)


def ConsoleChat():
    """Permite utilizar al bot en la consola"""
    fake_user = "Anonimous"
    while True:
        text = input("User >> ")
        if text.lower() == "exit":
            break
        else:
            response = ChatBot(text, fake_user)
            if response != "#NoText":
                print(f"Bot: {response}")
            else:
                print("*Parece que el bot no quiere responder*")


if __name__ == "__main__":
    BotClient().run(bot_config["BotToken"])
    # ConsoleChat()
