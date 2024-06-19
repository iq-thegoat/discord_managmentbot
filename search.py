import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from funks import create_embed
from thefuzz import process

class search(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="search_in_server")
    @app_commands.describe(
        query="search query EX: name of the book",
        msgcap="how many messages to check in each channel, default=250",
        channel="if you want to search in a specific channel",
        accuracy="how accurate to be DEFUALT=85%"
    )
    async def search_in_server(self, Interaction: discord.Interaction, query: str, msgcap: int=250, channel: discord.TextChannel | None = None,accuracy:int=85):
        await Interaction.response.defer()
        if accuracy > 100:
            accuracy = 100
        if accuracy < 0:
            accuracy = 0

        try:
            messages = {}
            if channel:
                i = channel.history(limit=msgcap)
                async for message in i:
                    messages[i.content] = i.jump_url
            else:
                for channel in self.bot.get_all_channels():
                    if isinstance(channel,discord.CategoryChannel):
                        pass
                    else:
                        if channel:
                            if Interaction.user in  channel.members:
                                print(Interaction.user)
                                print(channel.members[0])
                                i = channel.history(limit=msgcap)
                                async for message in i:
                                    messages[message.content] = message.jump_url
                
            resp = process.extract(query=query,choices=[x for x in messages.keys()],limit=1)
            print(resp)
            if resp[0][1] < accuracy:
                await Interaction.followup.send(
                    embed=create_embed(
                        title="No Results",
                        content="No matching messages found in the specified channel(s).",
                        color=discord.Colour.red(),
                    )
                )
            elif resp[0]:
                await Interaction.followup.send(f"[{resp[0][0]}]({messages[resp[0][0]]})")

        except Exception as e:
            print(e)  # Log the error, you can modify this to log to a file or a logging service
            await Interaction.followup.send(
                embed=create_embed(
                    title="Oops",
                    content="An error occurred while searching in the server.",
                    color=discord.Colour.red(),
                )
            )

async def setup(bot):
    await bot.add_cog(search(bot=bot))