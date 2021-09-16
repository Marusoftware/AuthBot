from discord.ext import commands
#from discord.ui import Button, Select, View
from user import User
import logging, argparse, discord, os, asyncio
#from discord import ButtonStyle, SelectOption
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

#parse argv
argparser = argparse.ArgumentParser("AuthBot", description="Authentication Bot")
argparser.add_argument("-log_level", action="store", type=int, dest="log_level", default=20 ,help="set Log level.(0-50)")
argparser.add_argument("-token", action="store", type=str, dest="token", required=True ,help="discord bot token")
##argparser.add_argument("--daemon", dest="daemon", help="Start in daemon mode.", action="store_true")
argv=argparser.parse_args()
#setting logging
logging.basicConfig(level=argv.log_level)
logger = logging.getLogger("Main")
#intents
intents=discord.Intents.default()
intents.typing=False
intents.members=True
#bot
bot = commands.Bot(command_prefix="!", intents=intents)
#slash command
slash_client = SlashCommand(bot, sync_commands=True)
#backend
user=User()

#event_on_connect
@bot.event
async def on_ready():
    logger.info("Login")
    await asyncio.start_server(SServer,"localhost",50005, reuse_port=True, start_serving=True)

"""commands"""

@slash_client.slash(name="verify", description="Verify with recaptha and add role.")
async def verify(ctx):
    id=user.mkauth(ctx.guild.id, ctx.author.id)
    await ctx.send(f'Please verify with this [Link](https://marusoftware.net/service/captcha?id={id}&type=discord)',hidden=True)
@bot.command(name="verify")
async def verify(ctx):
    #ctx.channel
    #user.mkauth()
    await ctx.send("Now, this is no supported...")
@slash_client.slash(name="set_authd_role", description="Set the role that add when verify was sucess.", options=[
    create_option(name="role", description="The role", option_type=SlashCommandOptionType.ROLE, required=True)])
async def set_authd_role(ctx, role):
    try:
        member=ctx.guild.get_member(880613350650830909)
        await member.add_roles(role, reason="Permition test")
    except discord.errors.Forbidden:
        await ctx.send("Can't set role. Please check permition of this bot.")
        return
    else:
        await member.remove_roles(role, reason="Permition test")
    user.setrole(ctx.guild.id, role.id)
    await ctx.send("Role was successfully seted.")

"""Socket Server"""
async def SServer(reader, writer):
    print("read")
    id = await reader.read(15)
    id=id.decode("utf-8")
    print("readed")
    auth = user.readauth(id)
    if auth:
        guild=bot.get_guild(auth["gid"])
        member=guild.get_member(auth["mid"])
        role=guild.get_role(auth["rid"])
        print("add")
        try:
            await member.add_roles(role, reason="Captcha was sucessful.")
        except discord.errors.Forbidden:
            writer.write(b'PermERR')
            return
        writer.write(b'OK')
        await writer.drain()
        print("send")
    else:
        print("can't read")

#run
bot.run(argv.token)
