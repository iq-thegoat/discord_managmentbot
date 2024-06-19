import discord
from discord import app_commands
from discord.ext import commands
import loguru
import json
from funks import get_config,create_embed,log,kick

class Management(commands.Cog):
    def __init__(self,bot: discord.Client):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="give_role")
    @app_commands.describe(role="the role to give",user="self explanatory")
    async def give_role(self,interaction:discord.Interaction,role:discord.Role,user:discord.Member):
        await interaction.response.defer()


        try:
            await user.add_roles(role)
            embed = discord.Embed(color=discord.Color.green(),title="اعطاء رول")
            embed.description = f"تم اعطاء رول {role.name} بنجاح"
            await interaction.followup.send(embed=embed,ephemeral=True)
            
            await log(interaction=interaction,funk="role_add",embed=create_embed("اعطاء رول",f"اعطي {interaction.user.name}\n رول {role.name} \n الي {user.name}",discord.Color.purple()))
        
        except Exception as e:
            embed = discord.Embed(color=discord.Color.red(),title="اعطاء رول")
            embed.description = f"لم استطع اعطاء رول {role.name}"
            await interaction.followup.send(embed=embed,ephemeral=True)        
            loguru.logger.error(e)

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="remove_role")
    @app_commands.describe(role="the role to remove",user="self explanatory")
    async def remove_role(self,interaction:discord.Interaction,role:discord.Role,user:discord.Member):
        await interaction.response.defer()
        try:
            await user.remove_roles(role)
            embed = discord.Embed(color=discord.Color.green(),title="أخذ رول")
            embed.description = f"تم اخذ رول {role.name} بنجاح"
            await interaction.followup.send(embed=embed,ephemeral=True)
            await log(interaction=interaction,funk="role_add",embed=create_embed("اخذ رول",f"اخذ {interaction.user.name}\n رول {role.name} \n من {user.name}",discord.Color.purple()))

        except Exception as e:
            embed = discord.Embed(color=discord.Color.red(),title="اخذ رول")
            embed   .description = f"لم استطع اخذ رول {role.name}"
            await interaction.followup.send(embed=embed,ephemeral=True)
            loguru.logger.error(e)


    @commands.has_permissions(administrator=True)
    @app_commands.command(name="configurate")
    @app_commands.describe(logs_channel="channel to log to",purge="wether to log purges or not",message_delete="wether to log deleted messages or not",edited_messages="wether to log edited messages or not",bans="wether to log bans or no",kicks="wether to log kicks or no",role_add="wether to log role add to user or no",role_remove="wether to log remove role from user or no")
    async def configurate(self,interaction:discord.Interaction, logs_channel:discord.TextChannel,purge:bool,message_delete:bool,edited_messages:bool,bans:bool,kicks:bool,role_add:bool,role_remove:bool):
        await interaction.response.defer()

        d = {"logs_channel":int(logs_channel.id),
            "purge":purge,
            "message_delete":message_delete,
            "edited_messages":edited_messages,
            "bans":bans,
            "kicks":kicks,
            "role_add":role_add,
            "role_remove":role_remove
            }
        with open("config.json","w") as f:
            json.dump(d,f,indent=6)

        embed = discord.Embed(color=discord.Color.green(),title="عُدل الكونفج")
        embed.description = f"عُدل الكونفج بنجاح ✅️"
        await interaction.followup.send(embed=embed,ephemeral=True)
"""
    @commands.has_permissions(kick_members=True)
    @app_commands.command(name="kicks_member")
    @app_commands.describe(server_member="self explanatory",reason="why did you kick him DEFUALT: admin rights")
    async def kick_member(interaction:discord.Interaction,server_member:discord.User,reason:str="admin rights"):
        await kick(interaction=interaction,member=server_member,reason=reason)
"""
async def setup(bot):
    await bot.add_cog(Management(bot=bot))
