import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
from icecream import ic
from funks import get_config,create_embed,log,kick
import os
from io import BytesIO

import os

from dotenv import load_dotenv

load_dotenv()


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = os.environ.get("token")


@bot.event
async def on_ready():
    print("Bot is up and ready!")
    await bot.load_extension("management")
    await bot.load_extension("search")

    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        logger.error(str(e))



@commands.has_permissions(manage_messages=True)
@bot.command(name='purge', brief='Deletes a specified number of messages from the current channel')
async def purge(ctx:discord.ext.commands.Context, amount: int):

    # Delete the specified number of messages
    deleted = await ctx.channel.purge(limit=amount+1)
    await log(interaction=ctx,funk="purge",embed=create_embed("رسالات محذوفه",f"حذف {ctx.author.name}\n {amount} رسائل\n من {ctx.channel.mention}",color=discord.Color.brand_red()))

@commands.has_permissions(kick_members=True)
@bot.command(name="kick",brief="kicks a member")
async def kick_member(ctx:discord.ext.commands.Context,user:discord.Member,reason:str="admin rights"):
    print(user)
    if user:
        await kick(interaction=ctx,member=user,reason=reason)
    else:
        await ctx.send(embed=create_embed("لم اجد هذا العضو","",color=discord.Colour.red()))
@bot.event
async def on_message_edit(before,after):
    await log(interaction=before,funk="edited_messages",embed=create_embed("تعديل نص",f"عدل {before.author.name} نص\n\n من {before.content}\n\n الي {after.content}",color=discord.Color.blurple()))



@bot.event
async def on_message_delete(message:discord.Message):
    embed = create_embed("حذف رساله",f"حذف {message.author.name} رساله\n\n {message.content}",color=discord.Color.blurple())
    if len(message.attachments) >= 1:
        img = message.attachments[0].proxy_url
        embed.set_image(url=img)   
    print(embed.to_dict()) 
    await log(interaction=message,funk="edited_messages",embed=embed)


"""
@commands.has_permissions(administrator=True)
@bot.command(name='delrole', brief='Deletes a specified role')
async def purge(ctx, role: discord.Role):
    # Delete the specified number of messages
    try:
        await role.delete()
        embed = discord.Embed(color=discord.Color.green(),title=f"تم مسح {role.name}")
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(color=discord.Color.red(),title=f"لم اتمكن من مسح {role.name}")
        await ctx.send(embed=embed)

@commands.has_permissions(administrator=True)
@bot.command(name="newrole",brief="تصنع رول جديد")
async def new_role(ctx:discord.ext.commands.Context,name:str):
    guild:discord.Guild = ctx.guild
    print(guild)
    role = await guild.create_role(name=name)
    embed = discord.Embed(color=discord.Color.red(),title=f"لم اتمكن من مسح {role.name}")
    await ctx.send(embed=embed)
"""



bot.run(token=TOKEN)