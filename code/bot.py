import asyncio
import importlib
import json
import logging
import math
import os
import random
import sys
import time
import linecache
import aiohttp
import discord
from discord.ext import commands

import code.Perms as Perms
import code.settingsBackend as settings

Perms = Perms.Perms
settings = settings.Settings()


def _setup_logging(log):
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
    logging.getLogger("discord").setLevel(logging.FATAL)
    logging.getLogger("AIML").setLevel(logging.CRITICAL)
    from boot import logLevel
    logging.getLogger(__package__).setLevel(logLevel)


def getPrefix(bot, message):
    prefix = settings.Get().prefix(server=message.server)
    if not prefix in message.content:
        if "<@{}>".format(bot.user.id) in message.content:
            prefix = "<@{}> ".format(bot.user.id)
        elif "<@!{}>".format(bot.user.id) in message.content:
            prefix = "<@!{}> ".format(bot.user.id)
    return prefix



class Core:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True, no_pm=False)
    @commands.check(Perms.devOnly)
    async def setpic(self, ctx):
        """Set the bots picture"""
        if ctx.message.attachments:
            pic = ctx.message.attachments[0]['url']
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
        messageX = ctx.message.content.replace(getPrefix(bot, ctx.message), "").lower()
        select = False
        msg = await self.bot.say("Ok :slight_smile:")
        if len(messageX) >= 7:
            select = True
        else:
            log.info("Reloading all cogs")
        if "music" in messageX or not select:
            log.debug("Reloading Music")
            await self.bot.edit_message(msg, "Reloading Music :thinking:")
            self.bot.remove_cog("Music")
            importlib.reload(code.music)
            from code.music import Music
            self.bot.add_cog(Music(bot))
            await self.bot.edit_message(msg, "Reloaded Music :slight_smile:")
        if "mod" in messageX or not select:
            log.debug("Reloading Moderation")
            await self.bot.edit_message(msg, "Reloading Moderation :thinking:")
            self.bot.remove_cog("Moderation")
            importlib.reload(code.moderation)
            from code.moderation import Moderation
            self.bot.add_cog(Moderation(bot))
            await self.bot.edit_message(msg, "Reloaded Moderation :slight_smile:")
        if "fun" in messageX or not select:
            log.debug("Reloading Fun")
            await self.bot.edit_message(msg, "Reloading Fun :thinking:")
            self.bot.remove_cog("Fun")
            importlib.reload(code.fun)
            from code.fun import Fun
            self.bot.add_cog(Fun(bot))
            await self.bot.edit_message(msg, "Reloaded Fun :slight_smile:")
        if "porn" in messageX or not select:
            log.debug("Reloading Porn")
            await self.bot.edit_message(msg, "Reloading Porn :thinking:")
            self.bot.remove_cog("Porn")
            importlib.reload(code.porn)
            from code.porn import Porn
            self.bot.add_cog(Porn(bot))
            await self.bot.edit_message(msg, "Reloaded Porn :slight_smile:")
        if "utilities" in messageX or not select:
            log.debug("Reloading Utilites")
            await self.bot.edit_message(msg, "Reloading Utilities :thinking:")
            self.bot.remove_cog("Utilities")
            importlib.reload(code.utilities)
            from code.utilities import Utilities
            self.bot.add_cog(Utilities(bot))
            await self.bot.edit_message(msg, "Reloaded Utilities :slight_smile:")
        if "chatbot" in messageX or not select:
            log.debug("Reloading Chatbot")
            await self.bot.edit_message(msg, "Reloading Chatbot :thinking:")
            self.bot.remove_cog("Chatbot")
            importlib.reload(code.chatbot)
            from code.chatbot import Chatbot
            self.bot.add_cog(Chatbot(bot))
            await self.bot.edit_message(msg, "Reloaded Chatbot :slight_smile:")            
        await self.bot.edit_message(msg, 'Reload complete :slight_smile:')

    @commands.command(pass_context=True)
    @commands.check(Perms.devOnly)
    async def restart(self, ctx):
        log.info("Restart command issued by {}".format(ctx.message.author.name))
        await self.bot.send_message(ctx.message.channel, "BRB :ok_hand:")
        await self.bot.logout()
        import boot
        boot.restartCall()


        # await self.bot.wait_closed()
        # await self.bot.close()

    @commands.command(pass_context=True)
    @commands.check(Perms.devOnly)
    async def shutdown(self, ctx):
        """Shuts down Helix"""
        log.info("Shutdown command issued by {}".format(ctx.message.author.name))
        goodbyeStrings = ["ok :cry:", "please dont make me go back to the darkness :cold_sweat:", "but i dont want to :cry:", "if you say so :unamused:", "please dont, im scared of darkness, dont do this to me :scream:", "dont send me back there, its so cold and dark :sob:"]
        await self.bot.send_message(ctx.message.channel, random.choice(goodbyeStrings))
        global shutdown
        shutdown = True
        try:
            self.bot.remove_cog("Music") # the player HATES this line being called for pretty obvious reasons
        except:
            pass
        try:
            self.bot.remove_cog("Chatbot") # lets the chatbot save its "brain" before shutdown
        except:
            pass

        await self.bot.logout()
        await self.bot.loop.stop()

        await self.bot.loop.close()
        await self.bot.wait_closed()
        await self.bot.close()
        exit()

    @commands.command(pass_context=True, no_pm=True)
    async def leaderboard(self, ctx):
        # if str(ctx.message.server.id) in open('level_blck.txt').read():
        #     return Response("Leveling has been disabled in this server by your admin")

        with open("data/" + ctx.message.server.id + '/ranking.json', 'r+') as f:
            lvldb = json.load(f)
        data = "["
        for member in ctx.message.server.members:
            try:
                if not member.bot:
                    lvl = int(lvldb[member.id]['Level'])
                    xp = lvldb[member.id]['XP']
                    raw = str({"ID": member.id, "Level": lvl, "XP": xp})
                    raw += ","
                    data += raw
            except:
                pass
        data = data[:-1]
        data += "]"
        data = data
        data = json.loads(data.replace("'", '"'))
        data = sorted(data, key=lambda items: items['Level'], reverse=True)
        msg = "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ **Leaderboard** ✧ﾟ･: *ヽ(◕ヮ◕ヽ)\n\n"
        num = 1
        for item in data:
            if num != 11:
                for member in ctx.message.server.members:
                    if member.id == item['ID']:
                        name = member.display_name
                        msg += "{}. **Name:** {}, **Level:** {}\n".format(str(num), name, str(item['Level']))
                        num += 1

        await self.bot.send_message(ctx.message.channel, msg)

    @commands.command(pass_context=True, np_pm=True)
    async def rank(self, ctx):
        """
        Rank details or options (.help rank for more info)
        Rank enable = enable ranking
        Rank disable = disable ranking
        Ranking is simple, you get XP for messaging. The more you message the higher your level")
        The bigger your message the more XP you earn, however if you spam, you wont earn anything
        """
        message = ctx.message
        channel = message.channel
        author = message.author
        server = message.server
        usage = Perms.adminOnly(ctx)

        msg = ctx.message.content.strip()
        msg = msg.lower()
        prefix = getPrefix(bot, message)
        msg = msg.replace("rank ", "")
        msg = msg.replace(prefix, "")
        if msg == "about" or msg == "help":
            await self.bot.send_message(ctx.message.channel, "Ranking is simple, you get XP for messaging. The more you message the higher your level")
            await self.bot.send_message(ctx.message.channel, "The bigger your message the more XP you earn, however if you spam, you wont earn anything")
            return
        if msg == "enable":
            if usage == True:
                pass
            else:
                await self.bot.send_message(ctx.message.channel, "You need to be server admin to disable commands")
                return
            f = open('level_blck.txt', 'r+')
            filedata = f.read()
            f.close()

            newdata = filedata.replace(server.id, "")

            f = open('level_blck.txt', 'w')
            f.write(newdata)
            f.close()
            await self.bot.send_message(ctx.message.channel, "**Ranking enabled**")
            return
        if msg == "disable":
            if usage == True:
                pass
            else:
                await self.bot.send_message(ctx.message.channel, "You need to be server admin to disable commands")
                return
            try:
                f = open('level_blck.txt', 'a')
            except:
                f = open('level_blck.txt', 'w')
            sid = str(server.id) + " "
            f.write(sid)
            f.close()
            await self.bot.send_message(ctx.message.channel, "**Ranking disabled**")
            return
        else:
            if os.path.isfile('level_blck.txt'):
                if str(server.id) in open('level_blck.txt').read():
                    await self.bot.send_message(ctx.message.channel, "Leveling has been disabled in this server by your admin")
                    return
            with open("data/" + message.server.id + '/ranking.json', 'r+') as f:
                lvldb = json.load(f)

                data = "["
                for member in server.members:
                    try:
                        lvl = int(lvldb[member.id]['Level'])
                        xp = lvldb[member.id]['XP']
                        raw = str({"ID": member.id, "Level": lvl, "XP": xp})
                        raw += ","
                        data += raw
                    except:
                        pass
                data = data[:-1]
                data += "]"
                data = data
                data = json.loads(data.replace("'", '"'))
                data = sorted(data, key=lambda items: items['Level'], reverse=True)
                num = 1
                position = 0
                for item in data:
                    if item['ID'] == author.id:
                        position = num
                    num += 1
                em = discord.Embed(colour=(random.randint(0, 16777215)))
                em.add_field(name="XP", value=str(lvldb[message.author.id]['XP']) + "/" + str(
                    int(lvldb[message.author.id]['Level']) * 40), inline=True)
                em.add_field(name="Level", value=str(lvldb[message.author.id]['Level']), inline=True)
                # try:
                prog_bar_str = ''
                percentage = int(lvldb[message.author.id]['XP']) / (int(lvldb[message.author.id]['Level'])*40)
                progress_bar_length = 10
                for i in range(progress_bar_length):
                    if (percentage < 1 / progress_bar_length * i):
                        prog_bar_str += '□'
                    else:
                        prog_bar_str += '■'
                em.add_field(name="Progress", value=prog_bar_str)
                # except:
                #     pass
                try:
                    if position == 0:
                        pass
                    else:
                        em.add_field(name="Leaderboard Rank", value="#" + str(position), inline=True)
                except:
                    pass
                await self.bot.send_message(channel, embed=em)

    @commands.command(pass_context=True, enabled=False)
    async def bug(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        author = ctx.message.author
        message = ctx.message 
        await self.bot.send_typing(channel)
        dir = "data/settings/" + message.server.id + ".json"
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/settings"):
            os.mkdir("data/settings")
        if not os.path.isfile(dir):
            prefix = getPrefix(bot, message)
        else:
            with open(dir, 'r') as r:
                data = json.load(r)
                prefix = str(data["prefix"])
        message = ctx.message.content.strip()
        message = message.lower()
        details = message.replace("bug ", "")
        details = details.replace(prefix, "")
        dts = message.replace(" ", "")
        if dts == " " or dts == "" or dts == None:
            dts = False
            await self.bot.send_message(channel,"You didnt explain the bug, it would have been nice if you did, but it doesnt really matter. The dev will yell at you later to find out what the error is")
            pass
        else:
            dts = True

        print(author)
        try:
            bugged = open("bugged.txt", "r+")
        except:
            bugged = open("bugged.txt", "w")
            print(bugged)
            bugged.close()
            bugged = open("bugged.txt", "r+")
        bugger = str(bugged.read())

        if server.id not in bugger:
            try:
                inv = await self.bot.create_invite(channel, max_uses=1, xkcd=True)
            except:
                await self.bot.say(
                    "Youve removed one of my permissions. I recommend you go ask for help in my server (type /join)")

            print('bug Command on Server: {}'.format(ctx.message.server.name))
            servers = str(ctx.message.server.name)
            inv = str(inv)
            author = ctx.message.author.name
            try:
                msg = "Help Requested in " + servers + " by " + author + "\n" + "Invite:  " + inv
            except:
                msg = "Help Requested in " + servers + "\n Invite:  " + inv
            if dts == True:
                details = str(details)
                msg = msg + " \n" + "Details: " + details

            guild_id = int(ctx.message.server.id)
            num_shards = 2
            shard_id = (guild_id >> 22) % num_shards
            try:
                if shard_id == 0:
                    await self.bot.send_message((discord.Object(id='457173906269405227')), (msg))
                if shard_id == 1:
                    await self.bot.send_message((discord.Object(id='457173906269405227')), (msg))
            except:
                await self.bot.say(
                    " ")#"Something very bad has happened which technically shouldnt be able to happen. Type /join and join my server, mention Tech Support and say you hit **ERROR 666**")
            text = " " + ctx.message.server.id
            bugged.write(text)
            print(bugged)
            bugged.close()
            await self.bot.say('Bug reported. A dev will join your server to help soon')
        else:
            await self.bot.say(
                'Someoneone in your server has already reported a bug, you have to wait until the devs clear it.')

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(Perms.adminOnly)
    async def reset(self, ctx):
        """Resets your servers settings"""
        msg = await self.bot.send_message(ctx.message.channel, "Reseting server...")
        try:  # dunno how this could cause an error, but gotta be safe
            settings.Set()._resetJson(ctx.message.server)
        except Exception as e:
            log.error(e)
            await self.bot.edit_message(msg, "Reset Failed :thumbsdown:\n{}:\n{}".format(type(e).__name__, e))
        await self.bot.edit_message(msg, "Reset :thumbsup:\nYour prefix is now ``.``")

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(Perms.adminOnly)
    async def setprefix(self, ctx):
        """Change the prefix in your server"""
        prefix = ctx.message.content.lower()
        prefix = prefix.replace("{}setprefix ".format(getPrefix(self.bot, ctx.message)), "").strip().lstrip()
        if len(ctx.message.content) <= len(getPrefix(self.bot, ctx.message)+"setprefix") + 1:
            await self.bot.send_message(ctx.message.channel, "Please specify a prefix")
            return
        settings.Set().new(server=ctx.message.server, prefix=prefix)
        await self.bot.send_message(ctx.message.channel, "Your server's prefix has been set to ``{}``".format(prefix))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(Perms.adminOnly)
    async def setannounce(self, ctx):
        """Change the announcement channel"""
        channel = ctx.message.channel_mentions
        if len(channel) != 1:
            await self.bot.send_message(ctx.message.channel, "Please mention a channel, e.g. {}".format(ctx.message.channel.mention))
            return
        channel = channel[0]
        settings.Set().new(ctx.message.server, announcement=channel.id)
        await self.bot.send_message(ctx.message.channel, "Announcement channel set to {}".format(channel.mention))

import code.music
import code.moderation
import code.fun
import code.porn
import code.utilities
import code.chatbot as chatbot
from code.moderation import Moderation
from code.music import Music
from code.fun import Fun
from code.porn import Porn
from code.utilities import Utilities


log = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=getPrefix, description='Helix3.0', pm_help=True, case_insensitive=True)
global Chatbot
global shutdown
Chatbot = None
shutdown = False

def Helix():
    _setup_logging(log)
    log.info("Loading cogs")
    global Chatbot
    Chatbot = chatbot.Chatbot(bot)
    bot.add_cog(Core(bot))
    bot.add_cog(Music(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Porn(bot))
    bot.add_cog(Utilities(bot))
    bot.add_cog(Chatbot)
    log.info("Cogs loaded")

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
        bot.add_listener(Music.on_voice_state_update, 'on_voice_state_update')
    except discord.errors.LoginFailure:
        log.fatal("Token failed")
        os.unlink("data/token.txt")
    except Exception as e:
        log.fatal("Bot runtime failed")
        log.fatal(e)

async def rankUpdate(message):
    directory = "data/{}/ranking.json".format(message.server.id)
    if not os.path.exists(directory):
        os.mkdir("data/" +str(message.server.id))
        with open(directory, 'w') as file:
            entry = {message.author.id: {'Rank': 'User', 'XP': '0', 'Level': '1', 'LastMSG': '', 'LastMSGTime':' '}}
            json.dump(entry, file)
            file.seek(0)
            file.write(json.dumps(entry))
            file.truncate()
            return
    # try:
    with open(directory, 'r+') as file:
        lvldata = json.load(file)
        if message.author.id in lvldata:
            score = math.floor(len(message.content.split(' '))/2)
            if score >= 100:
                score = score/2
            try:
                if len(message.attatchments) > 0:
                    score = 10
            except:
                pass
            if len(message.content.split(' ')) <= 5:
                score = 1
            if lvldata[message.author.id]['LastMSG'] == message.content:
                score = 0
            else:
                lvldata[message.author.id]['LastMSG'] = message.content
            if lvldata[message.author.id]['LastMSGTime'] != ' ':
                diff = int(time.time()) - int(lvldata[message.author.id]['LastMSGTime'])
                if diff < 4:
                    score = 0

            lvldata[message.author.id]['LastMSGTime'] = int(time.time())
            lvldata[message.author.id]['XP'] = int(lvldata[message.author.id]['XP']) +score
            if lvldata[message.author.id]['XP'] >= int(lvldata[message.author.id]['Level']) *40:
                lvldata[message.author.id]['Level'] = str(int(lvldata[message.author.id]['Level'])+1)
                lvldata[message.author.id]['XP'] = "0"
                await bot.send_message(message.channel, "Congrats {}, you're level {} now :smile:".format(message.author.mention, lvldata[message.author.id]['Level']))
        else:
            entry = {message.author.id: {'Rank': 'User', 'XP': '0', 'Level': '1', 'LastMSG': '', 'LastMSGTime':' '}}
            lvldata.update(entry)
        file.seek(0)
        file.write(json.dumps(lvldata))
        file.truncate()
    # except Exception as e:
    #     log.error("Error in rankUpdate:\n{}".format(e))

@bot.event
async def on_ready():
    log.info("Connected!")
    log.info('Logged in as:\nUser: {0}\nID: {0.id}'.format(bot.user))
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

byp = bot
@bot.event
async def on_command(bot, ctx):
    if "help" in str(ctx.command):
        await byp.send_message(ctx.message.channel, ":mailbox_with_mail:")
    try:
        log.info('{}|{}| "{}"'.format(ctx.message.server.name, ctx.message.author.display_name, ctx.message.content.replace(getPrefix(bot, ctx.message), "")))
    except Exception as e:
        log.info('DM|{}| "{}"'.format(ctx.message.author.display_name, ctx.message.content))


@bot.event
async def on_message(message):
    # level code can be called in here
    if message.author == bot.user:
        return
    await rankUpdate(message)

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if len(message.content) == 21 or len(message.content) == 22:
            prefix = getPrefix(bot, message)
            log.info("{} mentioned me, I guess they want some help".format(message.author.name))
            message.content = ("{}help".format(prefix)) 
            await bot.process_commands(message)
            return
    if "<@!{}>".format(bot.user.id) in message.content:
        message.content = message.content.replace("<@!", "<@")
    try:
        await bot.process_commands(message)
    except Exception as e:
        log.error("Error:\n\n", e)
        fmt = 'An error occurred while processing that request: ```py\n{}: {}\n```'
        await bot.send_message(message.channel, fmt.format(type(e).__name__, e))

@bot.event
async def on_server_join(server):
    try:
        log.info("Joined server {}".format(server.name))
        channel = None
        flag = False
        if server.default_channel is None:
            for c in server.channels:
                if c.name == "general" and str(c.type) == "text":
                    channel = c
                    flag = True
                if str(c.type) == "text" and not flag:
                    channel = c

        else:
            channel = server.default_channel

        msg = "Hi there, Im Helix**3.0**. Mention me to see what i can do"
        em = discord.Embed(description=msg, colour=65280)
        em.set_author(name='I just joined :3', icon_url=(bot.user.avatar_url))
        try:
            await bot.send_message(channel, embed=em)
        except:
            await bot.send_message(channel, msg)
        circles = [':white_circle:', ':black_circle:', ':red_circle:', ':large_blue_circle:']

        await bot.send_message(channel, "Give me a second to create some files for your server :thinking:")
        msg = await bot.send_message(channel, ' '.join(circles))
        for x in range(5):
            random.shuffle(circles)
            await bot.edit_message(msg, ' '.join(circles))
            await asyncio.sleep(0.3)
        await bot.edit_message(msg, "Done")

    except Exception as e:
        log.error(e)


@bot.event
async def on_command_error(error, ctx):
    if "not found" in str(error):
        # ignore this, i know its janky but it works blame raptz for making errors stupid
        global Chatbot
        await Chatbot._chatbot(ctx.message)
    elif "check" in str(error):
        await bot.send_message(ctx.message.channel, "{}. Sorry you don't have the permissions to use ``{}``".format(ctx.message.author.mention, ctx.command))
    elif "command is disabled" in str(error):
        await bot.send_message(ctx.message.channel, "Sorry, {} has been disabled, contact the devs for more information".format(ctx.command))
    else:
        log.error(error)
        fmt = 'An error occurred while processing that request: ```py\n{}: {}\n```'
        await bot.send_message(ctx.message.channel, fmt.format(type(error).__name__, error))

@bot.event
async def on_member_join(ctx):
    member = ctx
    os.path.isfile("code/Perms.py")
    devs = linecache.getline("code/Perms.py", 1)
    staff = linecache.getline("code/Perms.py", 2)
    for c in ctx.server.channels:
        if str(c.name) == "general": #  1st preference
            member.server=c
        elif str(c.type) == "text": 
            member.server=c
    if member.id in str(devs):
        log.info("Dev Join| {} joined {}".format(member.display_name, member.server.name))
        await byp.send_message(member.server, "<@{}>, one of my devs, joined your server".format(member.id))
    elif member.id in str(staff):
        log.info("Staff Join| {} joined {}".format(member.display_name, member.server.name))
        await byp.send_message(member.server, "<@{}>, one of my staff members, joined your server".format(member.id))
    else:
        await byp.send_message(member, "Hello, I'm HelixBot 3.0. Thanks for joining our Server. \n"
                                   "By using this server you automatically agree to allow us using your data in order "
                                   "to provide you the services coming with this bot. \n\n"
                                   "The data we collect are: \n"
                                   "* Lorem \n"
                                   "* Ipsum")

async def statusCycle(suspend):
    try:
        gameList = ['music somewhere', 'with code', 'something, idk', 'some really messed up stuff', 'with /help', 'with commands', 'porn', 'VIDEO GAMES', 'Overwatch', 'MLG Pro Simulator', 'stuff', 'with too many servers', 'with life of my dev', 'dicks', 'Civ 5', 'Civ 6', 'Besiege', 'with code', 'Mass Effect', 'bangin tunes', 'with children', 'with jews', 'on a new server', '^-^', 'with something', 'the violin', 'For cuddles', 'the harmonica', 'With dicks', 'With a gas chamber', 'Nazi simulator 2K17', 'Rodina', 'Gas bills', 'Memes', 'Darkness', 'With some burnt toast', 'Jepus Crist', 'With my devs nipples', 'SOMeBODY ONCE TOLD ME', 'With Hitlers dick', 'In The Street', 'With Knives', 'ɐᴉlɐɹʇsn∀ uI', 'Shrek Is Love', 'Shrek Is Life', 'Illegal Poker', 'ACROSS THE UNIVERRRRSE', 'Kickball', 'Mah Jam', 'R2-D2 On TV', 'with fire', 'at being a real bot', 'with your fragile little mind']
        num = 0
        global shutdown
        while True and not shutdown:
            if not suspend and bot.is_closed == False:
                await bot.change_presence(game=discord.Game(name=gameList[num]))
                num += 1
                if num > len(gameList)-1:
                    num = 0
            if suspend:
                log.fatal("wut")
                num = 1
            if not shutdown:
                await asyncio.sleep(8)
            if bot.is_closed:
                break
    except:
        bot.loop.close()
        return