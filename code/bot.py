import asyncio
import discord
import importlib
import os
import json
import random
import sys
import aiohttp
from discord.ext import commands
import pprint
import logging

def _setup_logging():
    if len(logging.getLogger(__package__).handlers) > 1:
        log.debug("Skipping logger setup, already set up")
        return
    import colorlog
    shandler = logging.StreamHandler(stream=sys.stdout)
    fmt = "%(log_color)s[%(levelname)s] %(name)s: %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    fmt = colorlog.ColoredFormatter(fmt, date_format,
                                  log_colors={'DEBUG': 'cyan', 'INFO': 'reset',
                                              'WARNING': 'bold_yellow', 'ERROR': 'bold_red',
                                              'CRITICAL': 'bold_red'})
    shandler.setFormatter(fmt)
    logging.getLogger(__package__).addHandler(shandler)
    logging.getLogger("FFMPEG").setLevel(logging.ERROR)
    logging.getLogger("player").setLevel(logging.ERROR)
    logging.getLogger("discord.gateway ").setLevel(logging.ERROR)
    logging.getLogger(__package__).setLevel(logging.DEBUG)

def getPrefix(bot, message):
    dir = "data/" + message.server.id + ".json"
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.isfile(dir):
        prefix = "."
    else:
        with open(dir, 'r') as r:
            data = json.load(r)
            prefix = str(data["prefix"])
    if not prefix in message.content:
        if "<@{}>".format(bot.user.id) in message.content:
            prefix = "<@{}> ".format(bot.user.id)
    return prefix


class Perms:
    def donatorOnly(ctx):
        if message.ctx.author.id not in []:
            return staffOnly(ctx)  # staff override
        else:
            return True

    def devOnly(ctx):
        return ctx.message.author.id in ["174918559539920897"]

    def staffOnly(ctx):
        return ctx.message.author.id in ["174918559539920897", "26954392680372633"]


class Core:
    def __init__(self, bot, perms):
        self.bot = bot
        self.perms = perms
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True, no_pm=False)
    async def setpic(self, ctx):
        if ctx.message.attachments:
            pic = ctx.message.attachments[0]['url']
            print(pic)
        else:
            await bot.say("I cant use that :confused:")
            return
        with aiohttp.Timeout(10):
            async with self.session.get(pic) as image:
                image = await image.read()
                await self.bot.edit_profile(avatar=image)

        await bot.say("Done, do i look pretty? :blush:")

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(Perms.devOnly)
    async def reload(self, ctx):
        """Reloads the bot's cogs"""
        await self.bot.change_presence(game=discord.Game(name="new commands"))
        print("Reloading all cogs")
        msg = await self.bot.say('Reloading cogs :thinking:')

        await self.bot.edit_message(msg, "Reloading Music :thinking:")
        self.bot.remove_cog("Music")
        importlib.reload(code.music)
        from code.music import Music
        self.bot.add_cog(Music(bot, self.perms))
        await self.bot.edit_message(msg, "Reloaded Music :slight_smile:")

        await self.bot.edit_message(msg, "Reloading Moderation :thinking:")
        self.bot.remove_cog("Moderation")
        importlib.reload(code.moderation)
        from code.moderation import Moderation
        self.bot.add_cog(Moderation(bot, self.perms))
        await self.bot.edit_message(msg, "Reloaded Moderation :slight_smile:")

        await self.bot.edit_message(msg, "Reloading Fun :thinking:")
        self.bot.remove_cog("Fun")
        importlib.reload(code.fun)
        from code.fun import Fun
        self.bot.add_cog(Fun(bot, self.perms))
        await self.bot.edit_message(msg, "Reloaded Fun :slight_smile:")

        await self.bot.edit_message(msg, "Reloading Porn :thinking:")
        self.bot.remove_cog("Porn")
        importlib.reload(code.porn)
        from code.porn import Porn
        self.bot.add_cog(Porn(bot, self.perms))
        await self.bot.edit_message(msg, "Reloaded Porn :slight_smile:")

        await self.bot.edit_message(msg, "Reloading Utilities :thinking:")
        self.bot.remove_cog("Utilities")
        importlib.reload(code.utilities)
        from code.utilities import Utilities
        self.bot.add_cog(Utilities(bot, self.perms))
        await self.bot.edit_message(msg, "Reloaded Utilities :slight_smile:")
        await self.bot.edit_message(msg, 'Reload complete :slight_smile:')

    @commands.command(pass_context=True)
    @commands.check(Perms.devOnly)
    async def shutdown(self, ctx):
        """Shuts down Helix"""
        goodbyeStrings = ["ok :cry:", "please dont make me go back to the darkness :cold_sweat:", "but i dont want to :cry:", "if you say so :unamused:", "please dont, im scared of darkness, dont do this to me :scream:", "dont send me back there, its so cold and dark :sob:"]
        await self.bot.send_message(ctx.message.channel, random.choice(goodbyeStrings))
        try:
            self.bot.remove_cog("Music") # the player HATES this line being called for pretty obvious reasons
        except:
            pass
        await self.bot.logout()
        await self.bot.close()
        exit()

import code.music
import code.moderation
import code.fun
import code.porn
import code.utilities
from code.moderation import Moderation
from code.music import Music
from code.fun import Fun
from code.porn import Porn
from code.utilities import Utilities


log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
bot = commands.Bot(command_prefix=getPrefix, description='Helix3.0', pm_help=True)
def Helix():
    _setup_logging()

    log.debug("Loading cogs")
    bot.add_cog(Core(bot, Perms))
    bot.add_cog(Music(bot, Perms))
    bot.add_cog(Moderation(bot, Perms))
    bot.add_cog(Fun(bot, Perms))
    bot.add_cog(Porn(bot, Perms))
    bot.add_cog(Utilities(bot, Perms))
    log.debug("Cogs loaded")

    if os.path.isfile("data/token.txt"):
        token = open("data/token.txt", "r").read()
    else:
        try:
            os.mkdir("data")
        except:
            pass
        log.error("NO TOKEN Dx")
        token = input("Please input a token: ")
        f = open("data/token.txt", "w")
        f.write(token)
        f.close()
        log.info("New token saved, resuming boot")
    try:
        log.info("Connecting...")
        bot.run(token.replace("\n", ""), reconnect=True, bot=True)
    except discord.errors.LoginFailure:
        log.fatal("Token failed")
        os.unlink("data/token.txt")
    except Exception as e:
        log.fatal("Bot runtime failed")
        log.fatal(e)



@bot.event
async def on_ready():
    log.info('Logged in as:    {0} (ID: {0.id})'.format(bot.user))
    if len(bot.servers) == 0:
        log.warning("{} is not in any servers\nInvite link: {}".format(bot.user, discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(70380544), server=None)))
    else:
        string = "Servers:"
        for server in bot.servers:
            string += "\n                 -{}".format(server.name)
        log.info(string)
    bot.loop.create_task(statusCycle(False))
    startStrings = ["Hey! im online", "*yawns* Good Morning :unamused:", "Oh god, am i really that late??? :scream:", "THANK YOU, THANK YOU SO MUCH, DONT SEND ME BACK THERE PLEASE :sob:", "It was so dark... there was nothing to do :worried:", "I was so alone, so cold, so very very cold"]
    #await bot.send_message(discord.Object(456827191838113846), random.choice(startStrings))
    log.info("Ready for user input")
    log.error("This is what an error looks like")
    log.warning("This is what a warning looks like")

@bot.event
async def on_command(bot, ctx):
    log.info("{}|{}|   {}".format(ctx.message.server.name, ctx.message.author.display_name, ctx.message.content))
    if "help" in ctx.message.content:
        await byp.send_message(ctx.message.channel, ":mailbox_with_mail:")

@bot.event
async def on_message(message):
    # level code can be called in here
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        if len(message.content) == 21 or len(message.content) == 22:
            print("Someone mentioned me, I guess they want some help")
            message.content = ".help" #jankiest way of doing this but it works reliably
            await bot.process_commands(message)
            return
    try:
        await bot.process_commands(message)
    except Exception as e:
        print("Error:\n\n", e)

@bot.event
async def on_member_join(ctx):
    member = ctx
    if member.id in str(dev):
        print("Dev Join| {} joined {}".format(member.display_name, member.server.name))
        await byp.send_message(member.server, "{}, one of my devs, joined your server".format(member.display_name))
    if member.id in str(staff):
        print("Staff Join| {} joined {}".format(member.display_name, member.server.name))
        await byp.send_message(member.server, "{}, one of my staff members, joined your server".format(member.display_name))

async def statusCycle(suspend):
    gameList = ['music somewhere', 'with code', 'something, idk', 'some really messed up stuff', 'with /help', 'with commands', 'porn', 'VIDEO GAMES', 'Overwatch', 'MLG Pro Simulator', 'stuff', 'with too many servers', 'with life of my dev', 'dicks', 'Civ 5', 'Civ 6', 'Besiege', 'with code', 'Mass Effect', 'bangin tunes', 'with children', 'with jews', 'on a new server', '^-^', 'with something', 'the violin', 'For cuddles', 'the harmonica', 'With dicks', 'With a gas chamber', 'Nazi simulator 2K17', 'Rodina', 'Gas bills', 'Memes', 'Darkness', 'With some burnt toast', 'Jepus Crist', 'With my devs nipples', 'SOMeBODY ONCE TOLD ME', 'With Hitlers dick', 'In The Street', 'With Knives', 'ɐᴉlɐɹʇsn∀ uI', 'Shrek Is Love', 'Shrek Is Life', 'Illegal Poker', 'ACROSS THE UNIVERRRRSE', 'Kickball', 'Mah Jam', 'R2-D2 On TV', 'with fire', 'at being a real bot', 'with your fragile little mind']
    num = 0
    while True:
        if not suspend and bot.is_closed == False:
            await bot.change_presence(game=discord.Game(name=gameList[num]))
            num += 1
            if num > len(gameList)-1:
                num = 0
        if suspend:
            print("wut")
            num = 1
        await asyncio.sleep(8)
        if bot.is_closed:
            break