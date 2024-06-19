import discord
import json
import loguru
import datetime

def get_config() -> dict:
    with open("config.json", "r") as f:
            jdata = json.load(f)
    return  jdata


async def log(interaction,funk,embed):
    if get_config()[funk] and interaction.author.id != 1252665826616541415:
        logs_channel = interaction.guild.get_channel(get_config()["logs_channel"])
        current_time = datetime.datetime.now()
        embed.set_footer(text=current_time.isoformat())
        await logs_channel.send(embed=embed)
        

async def kick(interaction,member:discord.Member,reason:str):
    try:
        await member.kick(reason=reason)
        if type(interaction) is discord.Interaction:
            embed = create_embed(title="طرد عضو",content=f"طُرد {member.name}\n\n by {interaction.user.name}",color=discord.Color.green())   
            await interaction.followup.send(embed=embed)
        elif type(interaction) is discord.ext.commands.Context:
            embed = create_embed(title="طرد عضو",content=f"طُرد {member.name}\n\n by {interaction.author.name}",color=discord.Color.green())   
            await interaction.send(embed=embed)
        
        await log(interaction=interaction,funk="kicks",embed=embed)
    except Exception as e:
        if type(interaction) is discord.Interaction:
            embed = create_embed(title="حدث خطأ",content=f"حدث خطأ اثناء طرد العضو {member.name}",color=discord.Color.red())
            await interaction.followup.send(embed=embed)
        elif type(interaction) is discord.ext.commands.Context:
            await interaction.send(embed=embed)

        loguru.logger.error(e)

def create_embed(title: str, content: str, color: discord.Color):
    embed = discord.Embed(title=title, color=color)
    embed.description = content
    return embed