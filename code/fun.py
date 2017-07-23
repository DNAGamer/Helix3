import asyncio
import discord
import timeit
import code.get as get
import urllib
import urllib.request as urllib2
import bs4
import random
import requests

from bs4 import BeautifulSoup
from discord.ext import commands

from code.savage import savage
from code.compliment import compliment
from code.pickup import pickup
from code.shitpost import shitpost



class Fun:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def echo(self, ctx, *args):
        """echos whatever you say"""
        await self.bot.say('{}'.format(' '.join(args)))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context = True)
    async def savage(self, ctx):
        """Savage insults"""
        await self.bot.send_typing(ctx.message.channel)
        message = savage()
        mention = ""
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            mention += "<@{}>  ".format(user.id)
            
        message = (("%s {}").format(mention) % (message))

        await self.bot.say(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context = True)
    async def fakekick(self, ctx):
        """Fake kicks a user"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.delete_message(ctx.message)
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            await self.bot.say("<@{}>, i kicked <@{}>.".format(ctx.message.author.id, user.id))

    @commands.command(pass_context = True)
    async def dog(self):
        """Sends a dog pic"""
        def findDog():
            page = BeautifulSoup(urllib2.urlopen("https://random.dog/"), "lxml")
            img = page.findAll('img')
            image = str(img)
            image = image.replace('[<img id="dog-img" src="', "")
            image = image.replace('"/>]', "")
            image = "https://random.dog/{}".format(image)

        while "https://random.dog/[]" in image:
            findDog()

        await self.bot.say(image)

    @commands.command(pass_context = True)
    async def cat(self):
        """Sends a cat pic"""
        global image
        def findCat():
            global image
            page = BeautifulSoup(urllib2.urlopen("https://random.cat/view?i={}".format(random.randint(0, 1283))), "lxml")
            img = page.findAll('img')
            image = str(img)
        findCat()
        image = image.replace('[<img alt="" id="cat" src="', "")
        image = image.replace("'", "")
        image = image.replace('" title=""/>, <img alt="veure un altre gat a latzar" id="logo" src="random.cat-logo.png" title="veure un altre gat a latzar"/>, <img alt="like us on facebook!" border="0" src="http://random.cat/facebook.jpg" title="like us on facebook!"/>]', "")
        image = image.replace(" ", "%20")
        image = "https://random.cat/{}".format(image)
        while ("http://random.cat/random.cat-logo.png" or "http://random.cat/facebook.jpg") in image:
            findCat()   
                      
        await self.bot.say(image)

    @commands.command(pass_context = True)
    async def compliment(self, ctx):
        """Sends compliments"""
        await self.bot.send_typing(ctx.message.channel)
        message = compliment()
        mention = ""
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            mention += "<@{}>  ".format(user.id)
            
        message = (("%s {}").format(mention) % (message))

        await self.bot.say(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context = True)
    async def pickup(self, ctx):
        """Pickup lines"""
        await self.bot.send_typing(ctx.message.channel)
        message = pickup()
        mention = ""
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            mention += "<@{}>  ".format(user.id)
            
        message = (("%s {}").format(mention) % (message))

        await self.bot.say(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context = True)
    async def shitpost(self, ctx):
        """Shitposts"""
        await self.bot.send_typing(ctx.message.channel)
        message = shitpost()
        mention = ""
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            mention += "<@{}>  ".format(user.id)
            
        message = (("%s {}").format(mention) % (message))

        await self.bot.say(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context = True)
    async def vicky(self, ctx, *args):
        """Victorian insults"""
        await self.bot.send_typing(ctx.message.channel)
        mention = ""
        user_mentions = list(map(ctx.message.server.get_member, ctx.message.raw_mentions))
        for user in user_mentions:
            mention += "<@{}>  ".format(user.id)

        if "326819697381212160" in mention:
            mention.replace("326819697381212160", ctx.message.author.id)

        words1 = ['Artless', 'Bawdy', 'Beslubbering', 'Bootless', 'Churlish', 'Cockered', 'Clouted', 'Craven', 'Currish',
             'Dankish', 'Dissembling', 'Droning', 'Errant', 'Fawning', 'Fobbing', 'Froward', 'Frothy', 'Gleeking',
             'Goatish', 'Gorbellied', 'Impertinent', 'Infectious', 'Jarring', 'Loggerheaded', 'Lumpish', 'Mammering',
             'Mangled', 'Mewling', 'Paunchy', 'Pribbling', 'Puking', 'Puny', 'Quailing', 'Rank', 'Reeky', 'Roguish',
             'Ruttish', 'Saucy', 'Spleeny', 'Spongy', 'Surly', 'Tottering', 'Unmuzzled', 'Vain', 'Venomed',
             'Villainous', 'Warped', 'Wayward', 'Weedy', 'Yeasty','Base-court', 'Bat-fowling', 'Beef-witted', 'Beetle-headed', 'Boil-brained', 'Clapper-clawed','Clay-brained', 'Common-kissing', 'Crook-pated', 'Dismal-dreaming', 'Dizzy-eyed', 'Dog-hearted',
             'Dread-bolted', 'Earth-vexing', 'Elf-skinned', 'Fat-kidneyed', 'Fen-sucked', 'Flap-mouthed', 'Fly-bitten',
             'Folly-fallen', 'Fool-born', 'Full-gorged', 'Guts-griping', 'Half-faced', 'Hasty-witted', 'Hedge-born',
             'Hell-hated', 'Idle-headed', 'Ill-breeding', 'Ill-nurtured', 'Knotty-pated', 'Milk-livered',
             'Motley-minded', 'Onion-eyed', 'Plume-plucked', 'Pottle-deep', 'Pox-marked', 'Reeling-ripe', 'Rough-hewn',
             'Rude-growing', 'Rump-fed', 'Shard-borne', 'Sheep-biting', 'Spur-galled', 'Swag-bellied', 'Tardy-gaited',
             'Tickle-brained', 'Toad-spotted', 'Unchin-snouted', 'Weather-bitten']
        words2 = ['Apple-john', 'Baggage', 'Barnacle', 'Bladder', 'Boar-pig', 'Bugbear', 'Bum-bailey', 'Canker-blossom',
             'Clack-dish', 'Clot-pole', 'Coxcomb', 'Codpiece', 'Death-token', 'Dewberry', 'Flap-dragon', 'Flax-wench',
             'Flirt-gill', 'Foot-licker', 'Fustilarian', 'Giglet', 'Gudgeon', 'Haggard', 'Harpy', 'Hedge-pig',
             'Horn-beast', 'Huggermugger', 'Jolt-head', 'Lewdster', 'Lout', 'Maggot-pie', 'Malt-worm', 'Mammet',
             'Measle', 'Minnow', 'Miscreant', 'Mold-warp', 'Mumble-news', 'Nut-hook', 'Pigeon-egg', 'Pignut', 'Puttock',
             'Pumpion', 'Rats-bane', 'Scut', 'Skains-mate', 'Strumpet', 'Varlot', 'Vassal', 'Whey-face', 'Wagtail']

        adjective1 = random.choice(words1)
        if adjective1.startswith(("A" or "E" or "I" or "O" or "U")):
            article = "an"
        else:
            article = "a"
        adjective2 = random.choice(words1)
        while adjective2 == adjective1:
            adjective2 = random.choice(words1)
        noun = random.choice(words2)
        if mention == "":
            insult = (("Thou art %s %s, %s %s") % (article, adjective1, adjective2, noun))
        else:
            insult = (("%s, thou art %s %s, %s %s") % (mention, article, adjective1, adjective2, noun))
        await self.bot.say(insult)

    @commands.command(pass_context = True)
    async def doge(self, ctx, *args):
        text = '{}'.format(' '.join(args))
        text = str(text)
        text = text.replace(",", "/")
        text = text.replace(" ", "_")
        url = ("http://romtypo.com/helix/doge/{}".format(text))
        await self.bot.say(url)

    @commands.command(pass_context = True)
    async def eightball(self, ctx, *args):
        await self.bot.send_typing(ctx.message.channel)
        randomint = random.randint(1, 20)
        answer = (("http://www.indra.com/8ball/animatedgifs/c%s.gif") % (randomint))
        await self.bot.say(answer)