# Mr Keprins Discord Bot

# Version: 2.0
# Originally created: 23 September 2021, 4:31:55 PM
# Creator: Cohen Beveridge


# Key for User data values:
# [points, gn, gm, daily streak, last daily, memes, trivia, xp, last weekly, last monthly, 0, 0]
# [  0     1   2        3            4         5      6     7        8            9       10 11]


import random
from os import system

from math import inf, fabs
from random import randint
import asyncio
import discord.ext
from discord.ui import Button, View
from datetime import datetime, timedelta
from pytrivia import Trivia
from requests import get, request
from json import loads
from nltk.corpus import cmudict
from nltk import download as nltk_download
from quote import quote
from randfacts import get_fact
from github import Github
from forex_python.bitcoin import BtcConverter
from weathercom import getCityWeatherDetails
from bing_image_urls import bing_image_urls
from youtubesearchpython import VideosSearch
# noinspection
from spellchecker import SpellChecker


data = {
    "servers": {},
    "server_temp": {},
    "channels": {},
    "users": {},
    "user_temp": {},
    "events": {},
    "channel-activity": {}
}


# XP buffer is the dictionary of XP gained in the current 30-second interval
xp_buffer = {}
uploaded = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
if int(uploaded[17:]) >= 30:
    uploaded = uploaded[:17] + "30"
else:
    uploaded = uploaded[:17] + "00"

# Download nltk packages
nltk_download('cmudict', quiet=True)


# Initialise this_second variable, for use in updating the server message rate every second
this_second = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Discord intents and client setup. Do not touch.
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# DiscordComponents(client)

# Connect to keprins-file-storage on GitHub
github_object = Github("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")
repository = github_object.get_user().get_repo('keprins-file-storage')
print('Connected to GitHub\\keprins-file-storage')

# Message content will contain the message registered including the kp prefix
message_content = ""

# Retrieve data from the user data file, called points.txt
points_file_content = repository.get_contents('points.txt').decoded_content.decode()
lines_in_points_file = points_file_content.split('\n')
for line in lines_in_points_file:
    current_user = line[:line.find('::')]
    current_values = line[line.find('::') + 2:].split(':')
    data["users"][current_user] = current_values

# Retrieve data from the server data file
servers_file_content = repository.get_contents('servers.txt').decoded_content.decode()
lines_in_servers_file = servers_file_content.split('\n')
for line in lines_in_servers_file:
    current_server = line[:line.find('::')]
    current_values = line[line.find('::') + 2:].split(':')
    data["servers"][current_server] = current_values


# function to get current time, UTC+08:00
def now():
    utc_time = datetime.utcnow()
    hours_added = timedelta(hours=8)
    our_time = utc_time + hours_added
    return our_time


async def log(text, message=None):
    logline = "\n" + now().strftime("%d/%m/%Y|%H:%M:%S|")
    if message is None:
        logline += " ~ " + text
    else:
        logline += message.guild.name + "|#" + message.channel.name + "|" + str(message.channel.id) + "| ~ " + text
    logfile = open("logs.txt", "a")
    logfile.write(logline)
    logfile.close()


async def alert(text, critical=False):
    if critical:
        await client.get_channel(964143206860197908).send("@&938428589009944616" * 10 + "\n" + text)
    else:
        await client.get_channel(964143206860197908).send("@&938428589009944616\n" + text)


def one_button_view(button):
    view = View()
    view.add_item(button)
    return view


@client.event
async def on_ready():
    await client.get_channel(966962503198310421).send('Mr Keprins is back online!')
    print('We have logged in as {0.user}'.format(client))
    await log('Mr Keprins is back online')
    await client.change_presence(activity=discord.Game('kp help'))


async def keprins_help(message):
    if message.content.lower() == 'help':
        await message.author.send("```"
                                  'Mr Keprins Commands: (prefix "kp " can be replaced with "mr ")```\n\n```'
                                  "kp news <anything> == search for a news headline from around the world\n"
                                  "kp img <anything> == get an image of anything!\n"
                                  "kp weather == get current weather (in Willetton)\n"
                                  "kp hangman == play hangman!\n"
                                  "kp trivia == get a trivia question to earn points!\n"
                                  "kp o&x == play noughts and crosses against Mr Keprins\n"
                                  "kp o&x <@user> <points> == play noughts and crosses multiplayer and bet points!\n"
                                  "kp meme == get a random meme\n"
                                  "kp lb == display points leaderboard\n"
                                  "kp xp == see your xp (max 1xp per 30 seconds)\n"
                                  "kp xp lb == see the xp leaderboard\n"
                                  "kp covid == get daily covid summary\n"
                                  "kp events == see upcoming events and due dates\n"
                                  "kp next event == see next event/due date\n"
                                  "kp bitcoin == get bitcoin prices in AUD\n"
                                  "kp bitcoin <USD> == get bitcoin prices in any currency\n"
                                  "kp spam <amount> <text> == get Mr Keprins to spam\n"
                                  "kp say <text> == get Mr Keprins to say something for you\n"
                                  "kp daily == collect your daily points\n"
                                  "kp server rate == see the message rate for that server\n"
                                  "kp meme lb == display meme leaderboard\n"
                                  "kp trivia lb == display trivia leaderboard\n"
                                  "kp add event, <name>, <date>, [time (24h)], [who to ping] == add a server event\n"
                                  "kp due date, <name>, <date>, [time (24h)], [who to ping] == add a server due date\n"
                                  "kp joke == get a random joke\n"
                                  "kp donate <points> <user> == donate your points\n"
                                  "kp fact == get a random fact\n"
                                  "kp unsafe fact == get a random unsafe fact\n"
                                  "kp guess <number> == play a guessing game to earn points!\n"
                                  "kp quote <anything> == get a quote related to something\n"
                                  "kp wiki <anything> == get a summary for a wikipedia page\n"
                                  "kp def <anything> == define a word\n"
                                  "kp gn == say goodnight to mr keprins\n"
                                  "kp gm == say good morning to mr keprins\n"
                                  "Plus much more to come...\n"
                                  "```")


async def spam(message):
    if message.content.lower().startswith('spam '):
        if '@' in message.content:
            await message.channel.send("I can't allow spam pings!")
            return
        if bad_word(message):
            await message.channel.send(message.author.mention + " I won't spam any bad words!")
            return
        times_to_spam = message.content[5:message.content.find(' ', 5)]
        word = message.content[message.content.find(' ', 5) + 1:]
        if "spam" not in message.channel.name:
            await message.channel.send("I'll only spam in the designated spam channel")
        elif not times_to_spam.isdigit():
            await message.channel.send('Invalid Number. Syntax is `kp spam <number> <word>`')
        elif int(times_to_spam) > 100:
            await message.channel.send('The maximum spam is 100')
        else:
            await message.delete()
            await log(str(message.author) +
                      " (" + str(message.author.id) + ') spammed the word "' + word + '" ' + times_to_spam + ' times')
            for i in range(int(times_to_spam)):
                await message.channel.send(word)


async def cheat_collude(message, mode):
    await \
        message.channel.send(message.author.mention + '\n' + ':warning:' * 5 + '\n**!!! STOP TALKING ABOUT ' +
                             'CHEATING' if mode == 'cheat' else 'COLLUDING' + ' !!!**', delete_after=2)
    await message.add_reaction('⚠')
    time_now = now().strftime("%H:%M:%S")
    date_today = now().strftime("%d/%m/%Y")
    incident_description = '**' + str(message.author.mention) + '** was seen ' + \
                           'CHEATING' if mode == 'cheat' else 'COLLUDING' + ' at ' + time_now + ' on ' + date_today
    embed = discord.Embed(
        description=incident_description,
        url=message.jump_url,
        color=discord.Color.dark_blue()
    )
    await client.get_channel(937143598892331018).send(embed=embed)
    await log(incident_description)


async def cheat_alert(message):
    if message.author == client.user:
        return
    for word in ['cheat', 'cheet', 'cheeat', 'cheeet']:
        if word in message_content.lower():
            await cheat_collude(message, 'cheat')


async def collude_alert(message):
    if message.author == client.user:
        return
    collude_words = ['collude', 'collusion', 'colluding', 'colluded', 'colude', 'colusion', 'coluding', 'coluded',
                     'colluse', 'collud', 'colld', 'colud', 'colllude', 'colludde', 'colludee', 'coluude', 'cllude',
                     'colluude', 'cullution', 'colluzion', 'kolood']
    content_to_check = message_content.lower().replace(" ", "").replace("k", "c")
    for word in collude_words:
        if word in content_to_check:
            await cheat_collude(message, 'collude')


def get_joke():
    jokes = get("https://v2.jokeapi.dev/joke/Any").json()
    if jokes["type"] == "twopart":
        output = jokes["setup"] + "\n" + jokes["delivery"]
    else:
        output = jokes["joke"]
    # if jokes["flags"]["nsfw"] or jokes["flags"]["racist"] or jokes["flags"]["sexist"] or jokes["flags"]["explicit"]:
    #     output = "||" + output + "||"
    return output


async def joke(message):
    if message.content.lower() == "joke":
        button = Button(label="New Joke", style=discord.ButtonStyle.green, custom_id="new")

        async def button_callback(interaction):
            await interaction.response.edit_message(content=get_joke(), view=one_button_view(button))

        button.callback = button_callback

        await message.channel.send(get_joke(), view=one_button_view(button))


async def trivia_q(message):
    channel_answer = data["channels"][message.channel.id]["answer"]
    channel_question = data["channels"][message.channel.id]["question"]
    channel_boolean = data["channels"][message.channel.id]["boolean"]
    if message.content.lower() == 'trivia':
        if channel_answer is None:
            question = 'which of the following 000000'
            answer = None

            while 'which' in question.lower() or 'the following' in question.lower():
                result = Trivia(True).request(1).get('results')
                question = result[0].get('question')
                answer = result[0].get('correct_answer')

                boolean = result[0].get('type') == 'boolean'
                if boolean:
                    question = 'True or False: ' + question
                data["channels"][message.channel.id]["boolean"] = boolean

            data["channels"][message.channel.id]["question"] = question
            data["channels"][message.channel.id]["answer"] = answer
            await message.channel.send(question)
        else:
            await message.channel.send('You have to answer this question first:\n' + channel_question +
                                       '\n(You can say "give up" if you want)')
    elif (message_content.lower() == 'give up' or message_content.lower() == 'idk' or
          message_content.lower() == "i don't know") and channel_answer is not None:
        await message.channel.send('The answer was: ' + channel_answer)
        data["channels"][message.channel.id]["question"] = None
        data["channels"][message.channel.id]["answer"] = None
    else:
        if message_content is None or channel_answer is None:
            return
        if message_content.lower() == channel_answer.lower():
            data["channels"][message.channel.id]["answer"] = None
            data["channels"][message.channel.id]["question"] = None
            if channel_boolean:
                await give_points(message.author.id, 5, "TRUE/FALSE")
                await message.channel.send(
                    '**CORRECT!**\n' + message.author.name + ", you get 5 points for that True/False!")
            else:
                await give_points(message.author.id, 25, "TRIVIA")
                await message.channel.send('**CORRECT!**\n' + message.author.name + ", you get 25 points!")
                data["users"][str(message.author.id)][6] = str(int(data["users"][str(message.author.id)][6]) + 1)
                await update_points("+1 trivia point to " + str(message.author) + " (" + str(message.author.id) + ")")


async def send_to_user(message):
    if message.content.lower().startswith('send '):
        target_user_id = message.content[5:message.content.find(" ", 5)]
        target_user_id = target_user_id[2:-1].replace("!", "", 1)
        send_content = message.content[message.content.find(" ", 5) + 1:]
        target_user = client.get_user(int(target_user_id))
        await target_user.send(send_content)
        await message.author.send("Sent message to `" + target_user.name + "` with content:\n\n`" + send_content + "`")


def meme_embed():
    memes = get("https://meme-api.herokuapp.com/gimme").json()
    embed = discord.Embed(
        title=memes["title"],
        url=memes["postLink"]
    )
    embed.set_image(url=memes["url"])
    return embed


async def get_meme(message):
    if message.content.lower() == 'meme':
        button = Button(label="New Meme", style=discord.ButtonStyle.green, custom_id="new")

        async def button_callback(interaction):
            try:
                await interaction.response.edit_message(embed=meme_embed(), view=one_button_view(button))
            except discord.errors.NotFound:
                try:
                    await interaction.response.edit_message(embed=meme_embed(), view=one_button_view(button))
                except discord.errors.NotFound:
                    pass
            data["users"][str(message.author.id)][5] = str(int(data["users"][str(message.author.id)][5]) + 1)
            await update_points("+1 Meme Point")

        button.callback = button_callback

        await message.channel.send(embed=meme_embed(), view=one_button_view(button))


async def book_quote(message):
    if message.content.startswith('quote '):
        if bad_word(message):
            await message.channel.send(message.author.mention + " That's a bad word! No quotes for you!")
            return
        search = message.content[6:]
        result = quote(search)
        try:
            send = result[randint(0, len(result) - 1)]['quote']
            if len(str(send)) > 2000:
                send = send[:1997] + '...'
            await message.channel.send(send)
        except TypeError:
            await message.channel.send('No quotes found which relate to ' + search)


async def keprins_say(message):
    if message.content.startswith('say '):
        if "@" in message.content:
            await message.reply("If you want to ping someone, do it yourself!")
            return
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass
        await message.channel.send(censor_and_replace(message.content[4:]))
        await log("Mr Keprins 'said' " + censor_and_replace(message.content[4:]) + " (" + str(message.author) + ")")


async def special_events(message):
    xmas = ["merry christmas", "merry xmas", "happy christmas", "happy xmas", "merry christmas!", "merry xmas!",
            "happy christmas!", "happy xmas!"]
    if message.content.lower().strip() in xmas:
        if now().strftime("%d/%m") == "25/12":
            await message.channel.send("**Merry Christmas " + message.author.mention + "!**")
    ny = ["happy new year", "happy ny", "happy 2022", "hny", "happy new year!", "happy ny!", "happy 2022!", "hny!"]
    if message.content.lower().strip() in ny:
        if now().strftime("%d/%m") == "01/01":
            await message.channel.send("**Happy New Year " + message.author.mention + "!**")


async def fact(message):
    if message.content.lower() == 'fact':
        await message.channel.send(get_fact(False))
    if message.content.lower() == 'unsafe fact':
        await message.channel.send(get_fact(False, True))


async def update_points(message):
    new_content = ""
    x = -1
    for a_user in data["users"]:
        if a_user != "":
            x += 1
            user_values = data["users"][a_user]
            new_content += str(a_user) + ":"
            string_values = ""
            for value in user_values:
                string_values += ":" + value
            new_content += string_values + "\n"
    new_content = new_content[:len(new_content) - 1]
    repository.update_file(repository.get_contents('points.txt').path, message, new_content,
                           repository.get_contents('points.txt').sha, branch="main")
    if message not in ["gave xp", "+1 Meme Point"]:
        await log(message)


def make_ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


async def manage_points(message):
    user_id = str(message.author.id)
    if user_id not in data["users"]:
        data["users"][user_id] = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        await update_points('Add ' + user_id + " (" + str(message.author) + ") to data")
    if message.content.lower() == "points":
        mode = "points"
        num = 0
    elif message.content.lower() == "memes":
        mode = "memes"
        num = 5
    elif message.content.lower() == "trivia points":
        mode = "trivia"
        num = 6
    elif message.content.lower() == "xp":
        mode = "xp"
        num = 7
    else:
        mode = None
        num = None
    if mode is not None:
        points = data["users"][user_id][num]
        place = 1
        trail = inf
        next_best = ""
        for member in message.guild.members:
            if str(member.id) in data["users"]:
                member_points = int(data["users"][str(member.id)][num])
                if member_points > int(points):
                    place += 1
                    if 0 < member_points - int(points) < trail:
                        trail = member_points - int(points)
                        next_best = member.display_name
        place = make_ordinal(place)
        trail = str(trail)
        if trail == 'inf':
            if mode == "points":
                await message.reply(
                    embed=discord.Embed(
                        title="You have " + points + " points!",
                        colour=discord.Colour.brand_green(),
                        description="You're in `" + place + "` place and **you're the best in this server!**"))
            elif mode == "memes":
                await message.reply(
                    embed=discord.Embed(
                        title="You've viewed " + points + " memes!",
                        colour=discord.Colour.purple(),
                        description="You're in `" + place + "` place and **you're the best in this server!**"))
            elif mode == "xp":
                await message.reply(
                    embed=discord.Embed(
                        title="You have " + points + " xp, and __you're the best in this server!__",
                        colour=discord.Colour.dark_theme(),
                        description="You can earn a maximum of 1 xp per 30 seconds."))
            else:
                await message.reply(
                    embed=discord.Embed(
                        title="You've answered " + points + " trivia questions!",
                        colour=discord.Colour.brand_red(),
                        description="You're in `" + place + "` place and **you're the best in this server!**"))
        else:
            if mode == "points":
                await message.reply(
                    embed=discord.Embed(
                        title="You have " + points + " points!",
                        colour=discord.Colour.brand_green(),
                        description="You're in `" + place + "` place and you're `" +
                                    trail + "` points behind **" + next_best + "**"))
            elif mode == "memes":
                await message.reply(
                    embed=discord.Embed(
                        title="You've viewed " + points + " memes!",
                        colour=discord.Colour.purple(),
                        description="You're in `" + place + "` place and you're `" +
                                    trail + "` memes behind **" + next_best + "**"))
            elif mode == "xp":
                await message.reply(
                    embed=discord.Embed(
                        title="You have " + points + " xp, and you're ranked " + place + " in this server!",
                        colour=discord.Colour.dark_theme(),
                        description="You can earn a maximum of 1 xp per 30 seconds."))
            else:
                await message.reply(
                    embed=discord.Embed(
                        title="You've answered " + points + " trivia questions!",
                        colour=discord.Colour.brand_red(),
                        description="You're in `" + place + "` place and you're `" +
                                    trail + "` questions behind **" + next_best + "**"))
    if message.content.lower()[:7] == "points ":
        mode = "points"
        num = 0
    elif message.content.lower()[:6] == "memes ":
        mode = "memes"
        num = 5
    elif message.content.lower()[:7] == "trivia " and not (message.content.lower()[7:].startswith("lb") or
                                                           message.content.lower()[7:].startswith("leaderboard")):
        mode = "trivia"
        num = 6
    elif message.content.lower()[:3] == "xp " and not (message.content.lower()[3:].startswith("lb") or
                                                       message.content.lower()[3:].startswith("leaderboard")):
        mode = "xp"
        num = 7
    else:
        mode = None
        num = None
    if mode is not None:
        target_user_raw_id = message.content[message.content.find(" ") + 1:].strip()
        target_user_id = target_user_raw_id[2:-1].replace("!", "", 1)
        target_user_name = client.get_user(int(target_user_id)).display_name
        user_points = data["users"][target_user_id][num]
        if mode == "points":
            await message.reply(
                embed=discord.Embed(
                    title=target_user_name + " has " + user_points + " points",
                    colour=discord.Colour.brand_green()))
        elif mode == "memes":
            await message.reply(
                embed=discord.Embed(
                    title=target_user_name + " has viewed " + user_points + " memes",
                    colour=discord.Colour.purple()))
        elif mode == "trivia":
            await message.reply(
                embed=discord.Embed(
                    title=target_user_name + " has answered " + user_points + " trivia questions",
                    colour=discord.Colour.brand_red()))
        elif mode == "xp":
            await message.reply(
                embed=discord.Embed(
                    title=target_user_name + " currently has " + user_points + " xp",
                    colour=discord.Colour.dark_theme()))
    if message.content.lower() == "lb" or message.content.lower() == "leaderboard" or \
            message.content.lower()[:3] == "lb " or message.content.lower()[:12] == "leaderboard ":
        mode = "points"
        num = 0
    elif message.content.lower() == "meme lb" or message.content.lower() == "memes lb" or \
            message.content.lower()[:8] == "meme lb " or message.content.lower()[:9] == "memes lb ":
        mode = "memes"
        num = 5
    elif message.content.lower() == "trivia lb" or message.content.lower() == "trivia leaderboard" or \
            message.content.lower()[:10] == "trivia lb " or message.content.lower()[:19] == "trivia leaderboard ":
        mode = "trivia"
        num = 6
    elif message.content.lower() == "xp lb" or message.content.lower() == "xp leaderboard" or \
            message.content.lower()[:6] == "xp lb " or message.content.lower()[:15] == "xp leaderboard ":
        mode = "xp"
        num = 7
    else:
        mode = None
        num = None
    if mode is not None:
        if mode == "points":
            if " " in message.content:
                page = message.content.lower()[message.content.find(" ") + 1:]
                if (not page.isdigit()) and page != "all":
                    page = 1
            else:
                page = 1
        else:
            if " " in message.content[message.content.find(" ") + 1:]:
                page = message.content.lower()[message.content.find(" ", message.content.find(" ") + 1) + 1:]
                if (not page.isdigit()) and page != "all":
                    page = 1
            else:
                page = 1
        if page != "all":
            page = int(page)
        points_dictionary = {}
        for current_id in data["users"]:
            try:
                points_dictionary[client.get_user(int(current_id))] = int(data["users"][current_id][num])
            except ValueError:
                pass
        list_of_users = list(points_dictionary.keys())
        list_of_points = list(points_dictionary.values())
        points_sorted = []
        users_sorted = []
        for current_point in range(len(list_of_points)):
            inserted = False
            if len(points_sorted) == 0:
                points_sorted = [list_of_points[current_point]]
                users_sorted = [list_of_users[current_point]]
            else:
                for check_point in range(len(points_sorted)):
                    if list_of_points[current_point] >= points_sorted[check_point]:
                        points_sorted.insert(check_point, list_of_points[current_point])
                        users_sorted.insert(check_point, list_of_users[current_point])
                        inserted = True
                        break
                if not inserted:
                    points_sorted.append(list_of_points[current_point])
                    users_sorted.append(list_of_users[current_point])
        if page == "all":
            start = 0
            end = len(users_sorted) - 1
        else:
            if mode != "xp":
                start = (page - 1) * 8
                end = (page * 8) - 1
            else:
                start = (page - 1) * 10
                end = (page * 10) - 1
        max_itr = len(users_sorted)
        for num1 in range(len(users_sorted)):
            if num1 >= max_itr:
                break
            if users_sorted[num1] is None:
                users_sorted.remove(users_sorted[num1])
                points_sorted.remove(points_sorted[num1])
                max_itr -= 1
        if mode == "points":
            embed = discord.Embed(title="Points Leaderboard", colour=discord.Colour.brand_green(), description="")
        elif mode == "memes":
            embed = discord.Embed(title="Meme Leaderboard", colour=discord.Colour.purple(), description="")
        elif mode == "xp":
            embed = discord.Embed(title="XP Leaderboard", colour=discord.Colour.dark_theme(), description="")
        else:
            embed = discord.Embed(title="Trivia Leaderboard", colour=discord.Colour.brand_red(), description="")
        guild = client.get_guild(message.guild.id)
        itr = -1
        for iteration in range(len(users_sorted)):
            this_name = users_sorted[iteration].display_name
            this_id = users_sorted[iteration].id
            if guild.get_member(this_id) is not None:
                itr += 1
                this_points = str(points_sorted[iteration])
                if itr >= start:
                    embed.description += \
                        str(itr + 1) + ") `" + this_points + "` - " + this_name + "\n"
                if itr == end:
                    break
        if embed.description == '':
            await alert("Error with command: " + message.content)
            return
        await message.channel.send(embed=embed)


async def guess_number(message):
    ran_num = data["channels"][message.channel.id]["ran_num"]
    maximum = data["channels"][message.channel.id]["maximum"]
    since_guess = data["channels"][message.channel.id]["since_guess"]
    if message.content.lower().startswith('guess ') and message.content[6:].isdigit():
        if maximum != -1:
            await message.channel.send("You still need to guess between 1 and " + str(maximum))
            return
        maximum = int(message.content[5:])
        if maximum < 10:
            await message.channel.send("That's too low!")
            return
        data["channels"][message.channel.id]["ran_num"] = str(randint(1, maximum))
        data["channels"][message.channel.id]["since_guess"] = -1
        data["channels"][message.channel.id]["maximum"] = maximum
        await message.channel.send("Guess the number I'm thinking of! It's between 1 and " + str(maximum))
        await log(str(message.author) + " (" + str(message.author.id) + ") started " + message.content, message)
    if message_content == ran_num:
        points = maximum - since_guess - 1
        await message.reply(
            "**YOU GUESSED IT!**\n" + message.author.mention + " will receive " + str(points) + " points!")
        data["channels"][message.channel.id]["since_guess"] = 0
        data["channels"][message.channel.id]["ran_num"] = 0
        data["channels"][message.channel.id]["maximum"] = -1
        user_id = str(message.author.id)
        await give_points(user_id, points, "GUESSED NUMBER in #" + message.channel.name + " of " +
                          message.guild.name + " (" + str(message.channel.id) + ")")
    elif message_content.isdigit():
        if 0 < int(message_content) <= maximum:
            data["channels"][message.channel.id]["since_guess"] += 1


async def give_points(user_id, amount, reason):
    current_points = int(data["users"][str(user_id)][0])
    new_points = current_points + amount
    data["users"][str(user_id)][0] = str(new_points)
    await update_points(str(amount) + " points given to " + client.get_user(int(user_id)).name + " (" + str(user_id) +
                        ")| Before=" + str(current_points) + ", Now=" + str(new_points) + "  [" + reason + "]")


async def gn(message):
    if message.content.lower() == 'gn' or message.content.lower() == 'goodnight':
        hour = int(now().strftime("%H"))
        if 20 > hour > 3:
            await message.reply("It's too early", delete_after=5)
            return
        today = now().strftime('%Y-%m-%d')
        last_gn = data["users"][str(message.author.id)][1]
        if "," in last_gn:
            last_gn = '0'
        if last_gn == today:
            await message.reply("You already said goodnight today!", delete_after=5)
            return
        data["users"][str(message.author.id)][1] = today
        await message.channel.send('**Goodnight **' + message.author.mention)
        await give_points(message.author.id, 10, "GN")


def channel(message):
    channel_id = message.channel.id
    if channel_id not in data["channels"]:
        data["channels"][channel_id] = {
            "question": None,
            "answer": None,
            "boolean": False,
            "ran_num": -1,
            "maximum": -1,
            "since_guess": 0
        }
    if message.author.id not in data["user_temp"]:
        data["user_temp"][message.author.id] = {
            "hang_word": None,
            "hang_answer": None,
            "guessed": [],
            "failures": 0,
            "hang_msg": None
        }


async def hangman(message):
    display_images = ["  +---+\n      |\n      |\n      |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
                      "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="]
    hang_word = data["user_temp"][message.author.id]["hang_word"]
    hang_answer = data["user_temp"][message.author.id]["hang_answer"]
    failures = data["user_temp"][message.author.id]["failures"]
    guessed = data["user_temp"][message.author.id]["guessed"]
    hang_msg = data["user_temp"][message.author.id]["hang_msg"]
    if message.content.lower() == 'hangman' and hang_word is None:
        hang_word = random.choice(get("https://www.mit.edu/~ecprice/wordlist.10000").content.splitlines())\
            .decode("utf-8").lower()
        guess_area = "_" + " _" * (len(hang_word) - 1)
        hang_msg = await message.channel.send('```\nGuess a letter!\n' + guess_area + '\n```')
        hang_answer = "_" * len(hang_word)
        data["user_temp"][message.author.id]["hang_word"] = hang_word
        data["user_temp"][message.author.id]["failures"] = 0
        data["user_temp"][message.author.id]["guessed"] = []
        data["user_temp"][message.author.id]["hang_answer"] = hang_answer
        data["user_temp"][message.author.id]["hang_msg"] = hang_msg
    else:
        if hang_word is not None:
            response = message_content.lower()
            if len(response) == 1 and response.isalpha():
                if response in guessed:
                    await hang_msg.edit("You already guessed that letter!\n" + hang_msg.content)
                else:
                    guessed.append(response)
                    if response in hang_word:
                        for char in range(len(hang_word)):
                            if hang_word[char] == response:
                                hang_answer = hang_answer[:char] + hang_word[char].upper() + hang_answer[char + 1:]
                    else:
                        await hang_msg.edit('No "' + response + '"s in the word!\n' + hang_msg.content)
                        failures += 1
                        if failures == 7:
                            await hang_msg.edit("Last chance!")
                        if failures == 8:
                            await hang_msg.edit("**You FAILED!**\nThe answer was: " + hang_word + "\n" + hang_msg.content)
                            hang_word = None
                    if hang_answer is not None:
                        if hang_word == hang_answer.lower():
                            await hang_msg.edit("🥳 **You guessed the word!** 🥳\n__**" + hang_word.upper() +
                                                       "**__\n" + message.author.mention + ", you get 20 points!\n"
                                                + hang_msg.content)
                            await give_points(str(message.author.id), 20, "HANGMAN")
                            hang_word = None
                        else:
                            display_answer = hang_answer[0]
                            for char in hang_answer[1:]:
                                display_answer += " " + char
                            if failures < 8:
                                display = '```\n' + display_images[failures][:15] + "          " + display_answer +\
                                          display_images[failures][15:31] + "          USED: "
                                used = ""
                                for item in guessed:
                                    if item not in hang_word:
                                        used += item.upper() + ', '
                                used = used[:-2]
                                display += used + display_images[failures][31:] + '\n```'
                                await hang_msg.edit(display)
            data["user_temp"][message.author.id]["hang_word"] = hang_word
            data["user_temp"][message.author.id]["hang_answer"] = hang_answer
            data["user_temp"][message.author.id]["failures"] = failures
            data["user_temp"][message.author.id]["guessed"] = guessed
            data["user_temp"][message.author.id]["hang_msg"] = hang_msg


async def donate(message):
    if message.content.lower().startswith("donate "):
        amount = message.content.lower()[7:message.content.find(" ", 7)]
        if not amount.isdigit():
            await message.reply("That's not a valid number! Syntax is `kp donate <number> <user>`")
            return
        amount = int(amount)
        if amount <= 0:
            await message.reply("That's not enough to give!")
            return
        target_user = message.content[message.content.find(" ", 7):]
        target_user = target_user.strip()
        target_id = target_user[2:20]
        if client.get_user(int(target_id)) is None:
            await message.reply("Mr Keprins has no idea who that user is.")
        if int(data["users"][str(message.author.id)][0]) < 0:
            data["users"][str(message.author.id)][0] = "0"
            await update_points("Reset points to 0 for " + str(message.author) + " because they had negative.")
            await message.reply("**Negative points are BAD! (no hacking allowed you bubkis)**")
            await alert(
                "Someone was found with **Negative Points!**\n> who: " + str(message.author) + "\nwhere: " +
                message.channel.name + " in " + message.guild.name)
            return
        if amount > int(data["users"][str(message.author.id)][0]):
            await message.reply("Uh... you can't donate more than you have...")
            return
        await give_points(target_id, amount, "DONATION received")
        await give_points(message.author.id, 0 - amount, "DONATION given")
        await message.channel.send("Transferred " + str(amount) + " points from " + message.author.mention +
                                   " to <@!" + str(target_id) + ">")


async def gm(message):
    if message.content.lower() == 'gm' or message.content.lower() == 'good morning':
        utc_time = datetime.now()
        hours_added = timedelta(hours=8)
        our_time = utc_time + hours_added
        hour = int(our_time.strftime('%H'))
        if hour > 23:
            hour -= 24
        if hour >= 10:
            await message.channel.send("It's too late to say good morning!", delete_after=5)
            return
        today = our_time.strftime('%Y-%m-%d')
        last_gm = data["users"][str(message.author.id)][2]
        if "," in last_gm:
            last_gm = '0'
        if last_gm == today:
            await message.channel.send("You already said good morning today!", delete_after=5)
            return
        data["users"][str(message.author.id)][2] = today
        await update_points(str(message.author) + " said Good Morning")
        await message.channel.send('**Good Morning **' + message.author.mention)
        await give_points(message.author.id, 10, "GM")


async def update_servers(message):
    new_content = ""
    x = -1
    for a_server in data["servers"]:
        if a_server != "":
            x += 1
            server_values = data["servers"][a_server]
            new_content += str(a_server)
            new_content += ":"
            string_values = ""
            for value in server_values:
                string_values += ":"
                string_values += value
            new_content += string_values
            new_content += "\n"
    new_content = new_content[:len(new_content) - 1]
    repository.update_file(repository.get_contents('servers.txt').path, message, new_content,
                           repository.get_contents('servers.txt').sha, branch="main")
    if message != "Update seconds":
        await log(message)


async def server_data(message):
    server_id = str(message.guild.id)
    if server_id not in data["servers"]:
        all_members = message.guild.members
        members = []
        bots = []
        for mem in all_members:
            if not mem.bot:
                members.append(mem)
            else:
                bots.append(mem)
        data["servers"][server_id] = ["0", "0", "uncensored", "0", "0", "0", "0", "0", "0", "0"]
        await update_servers('Add ' + server_id + " (" + message.guild.name + ") to data")


def add_server_to_temp_data(message):
    if message.guild is not None:
        if message.guild.id not in data["server_temp"]:
            data["server_temp"][message.guild.id] = {
                "messages": 0
            }


async def count_messages(message):
    global this_second
    data["server_temp"][message.guild.id]["messages"] += 1
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if time_now != this_second:
        fmt = "%d/%m/%Y %H:%M:%S"
        tdelta = datetime.strptime(time_now, fmt) - datetime.strptime(this_second, fmt)
        diff_in_seconds = int(tdelta.total_seconds())
        this_second = time_now
        data["servers"][str(message.guild.id)][0] = str(int(data["servers"][str(message.guild.id)][0]) +
                                                        data["server_temp"][message.guild.id]["messages"])
        for guild in data["servers"]:
            former_seconds = int(float(data["servers"][guild][1]))
            data["servers"][guild][1] = str(former_seconds + diff_in_seconds)
        data["server_temp"][message.guild.id]["messages"] = 0
        await update_servers("Update seconds")


async def rate(message):
    if message.content.lower() == 'server rate' or message.content.lower() == 'message rate':
        messages = int(float(data["servers"][str(message.guild.id)][0]))
        seconds = int(float(data["servers"][str(message.guild.id)][1]))
        per_minute = messages / (seconds / 60)
        per_hour = messages / (seconds / 3600)
        per_day = messages / (seconds / 86400)
        await message.channel.send(
            "**Message Rate for " + message.guild.name + "**\n`messages per minute:` `" +
            str(round(per_minute, 3)) + "`\n`messages per hour:` `" + str(round(per_hour, 3)) +
            "`\n`messages per day:` `" + str(round(per_day, 3)) + '`')


def monitor(message):
    if "https://streamable.com/whe3ug" in message.content:
        return False


async def update_events(message):
    new_content = ""
    x = -1
    for an_event in data["events"]:
        if an_event != "":
            x += 1
            event_values = data["events"][an_event]
            new_content += str(an_event)
            new_content += ","
            string_values = ""
            for value in event_values:
                string_values += ","
                string_values += value
            new_content += string_values
            new_content += "\n"
    new_content = new_content[:len(new_content) - 1]
    repository.update_file(repository.get_contents('events.txt').path, message, new_content,
                           repository.get_contents('events.txt').sha, branch="main")
    await log(message)


async def censor(message):
    swearers = [783967717140332594, 761124349809524746, 852158639917891624, 721334601376727121, 676774613514190868,
                445498176007438337]
    if message.content.lower() == "censor server" and \
            (message.author.id in swearers or message.author == message.guild.owner):
        data["servers"][str(message.guild.id)][2] = "censored"
        await update_servers("Censor " + message.guild.name)
    if message.content.lower() == "uncensor server" and \
            (message.author.id in swearers or message.author == message.guild.owner):
        data["servers"][str(message.guild.id)][2] = "uncensored"
        await update_servers("Uncensor " + message.guild.name)


# Returns True if the string entered contains a bad word
def bad_word(message):
    if data["servers"][str(message.guild.id)][2] != "censored":
        return False
    return get("https://www.purgomalum.com/service/json?text=" +
               message.content.lower()).json()["result"] != message.content.lower()


def censor_and_replace(text):
    return get("https://www.purgomalum.com/service/json?text=" + text).json()["result"].replace("*", "\\*")


async def test_functions(message):
    if message.content.lower() == "server owner":
        await message.channel.send(message.guild.owner)
    if message.content.lower() == "channel test":
        await message.channel.send(message.guild.text_channels[0].id)
    if message.content.lower() == "test_#1":
        print(message.channel)
        print("\n")
        print(message.channel.guild)
    if message.content.lower().startswith("reply "):
        if "@" in message.content:
            await message.channel.send(message.author.mention + " If you want to @mention, do it yourself!")
            return
        await message.reply(censor_and_replace(message.content[6:]))
    if message.content.lower() == "time_test":
        await message.channel.send(embed=discord.Embed(title="Time Test Embed: <t:1653127200:R>", description="Time"))


async def feed(message):
    if message.content.lower()[:5] == "feed ":
        if bad_word(message):
            await message.channel.send("That's a bad word! It will not be eaten!")
            return
        food = message.content[5:]
        await message.channel.send("Delicious! I love to eat a good tasty " + food)


async def dank_memer(message):
    if message.content.lower() == "hunt":
        await message.channel.send("You went hunting and you caught a bear. Good job. No one cares.")
    if message.content.lower() == "fish":
        await message.channel.send("You went fishing and you caught a fish. Wow. Amazing.")
    if message.content.lower() == "dig":
        await message.channel.send("You dug a hole. Incredible.")
    if message.content.lower() == "search":
        await message.channel.send("What are you searching for? Actually, no one cares.")


async def daily(message):
    if message.content.lower() == "daily":
        utc_time = datetime.now()
        hours_added = timedelta(hours=5)
        our_time = utc_time + hours_added
        today = our_time.strftime('%Y-%m-%d')
        last_daily = data["users"][str(message.author.id)][4]
        if last_daily == today:
            await message.channel.send("You already did `daily` today!")
            return
        yesterday = (our_time - timedelta(days=1)).strftime('%Y-%m-%d')
        lost_streak = False
        if last_daily != today and last_daily != yesterday and last_daily != 0:
            await message.channel.send(message.author.mention + "You lost your streak!")
            lost_streak = True
            await log(str(message.author) + " (" + str(message.author.id) + ") lost their Daily Streak")
        data["users"][str(message.author.id)][4] = today
        streak = int(data["users"][str(message.author.id)][3])
        if lost_streak:
            streak = 0
        reward = (streak + 1) * 10
        if reward > 100:
            reward = 100
        await message.channel.send("Good job " + message.author.mention + " You get `" + str(reward) +
                                   "` points!\nYour streak has increased to `" + str(streak + 1) + "`")
        data["users"][str(message.author.id)][3] = str(streak + 1)
        await give_points(message.author.id, reward, "DAILY (streak = " + str(streak + 1) + ")")


async def list_servers(message):
    phrases = ["server list", "servers list", "list servers", "keprins servers", "mr keprins servers"]
    if message.content.lower() in phrases:
        changed = []
        for an_id in data["servers"].keys():
            if client.get_guild(int(an_id)) is None:
                changed.append(an_id)
        if changed:
            for a_id in changed:
                data["servers"].pop(a_id)
            await update_servers("removed a server: " + str(changed))
        output = "**Mr Keprins is currently in `" + str(len(data["servers"])) + "` servers:**\n"
        for str_id in data["servers"]:
            output += "`" + client.get_guild(int(str_id)).name + "`\n"
        await message.channel.send(output)


async def invite_me(message):
    if message.content.lower() == "inviteme" and message.author.id == 761124349809524746:
        for str_id in data["servers"].keys():
            int_id = int(str_id)
            if client.get_guild(int_id).get_member(761124349809524746) is None:
                invite = await client.get_channel(client.get_guild(int_id).text_channels[0].id). \
                    create_invite(max_age=10, max_uses=1)
                await client.get_user(761124349809524746).send(f"> {invite}")


async def vote(message):
    if message.content.lower() == "vote results":

        channel_id = 914816028209463297
        message_id = 918484054595207178
        vote_name = "Censor Bot Kick Vote"

        msg = await client.get_channel(channel_id).fetch_message(message_id)
        yes = msg.reactions[0].count
        no = msg.reactions[1].count
        if yes > no:
            percent = str(round(yes / (yes + no) * 100)) + "%"
            winner = 'Yes'
        elif no > yes:
            percent = str(round(no / (yes + no) * 100)) + "%"
            winner = 'No'
        else:
            winner = 'draw'
            percent = None
        if winner == 'draw':
            await message.channel.send(">>> **" + vote_name + ":**\nYes = `" + str(yes) + "`\nNo = `" + str(no) +
                                       "`\n**Votes are currently equal**")
        else:
            await message.channel.send(">>> **" + vote_name + ":**\nYes = `" + str(yes) + "`\nNo = `" + str(no) +
                                       "`\n**" + winner + " is winning with " + percent + "**")


async def manage_user_data_values(user_id):
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        await update_points('Add ' + str(user_id) + " (" + str(client.get_user(int(user_id))) + ") to data")
    if len(data["users"][str(user_id)]) < 12:
        while len(data["users"][str(user_id)]) != 12:
            data["users"][str(user_id)].append("0")
        await update_points("Gave " + client.get_user(user_id).name + " 12 value slots")


async def XP(message):
    global uploaded
    global xp_buffer
    if message.author.id not in xp_buffer:
        xp_buffer[message.author.id] = 1
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if int(time_now[17:]) >= 30:
        time_now = time_now[:17] + "30"
    else:
        time_now = time_now[:17] + "00"
    if time_now != uploaded:
        for i_d in xp_buffer.keys():
            data["users"][str(i_d)][7] = str(int(data["users"][str(i_d)][7]) + xp_buffer[i_d])
        xp_buffer = {}
        uploaded = time_now
        await update_points("gave xp")


def BuildBoard(board_values):
    a1, a2, a3, b1, b2, b3, c1, c2, c3 = board_values
    board = [
        [Button(a1, "a1"),
         Button(a2, "a2"),
         Button(a3, "a3")],
        [Button(b1, "b1"),
         Button(b2, "b2"),
         Button(b3, "b3")],
        [Button(c1, "c1"),
         Button(c2, "c2"),
         Button(c3, "c3")],
    ]
    return board


def ChangeBoard(board, change_pos, change_char):
    new_board = board
    all_squares = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
    new_board[all_squares.index(change_pos)] = change_char
    return new_board


def WinCheck(board, pos1, pos2, pos3, check):
    if board[pos1] == check and board[pos2] == check and board[pos3] == "☐":
        board[pos3] = "◉"
        return board
    elif board[pos1] == check and board[pos2] == "☐" and board[pos3] == check:
        board[pos2] = "◉"
        return board
    elif board[pos1] == "☐" and board[pos2] == check and board[pos3] == check:
        board[pos1] = "◉"
        return board
    else:
        # print('returning None w/' + str(pos1) + str(pos2) + str(pos3))
        return None


def HasWon(board, xo):
    return board[0] == xo and board[1] == xo and board[2] == xo \
           or board[3] == xo and board[4] == xo and board[5] == xo \
           or board[6] == xo and board[7] == xo and board[8] == xo \
           or board[0] == xo and board[3] == xo and board[6] == xo \
           or board[1] == xo and board[4] == xo and board[7] == xo \
           or board[2] == xo and board[5] == xo and board[8] == xo \
           or board[0] == xo and board[4] == xo and board[8] == xo \
           or board[2] == xo and board[4] == xo and board[6] == xo


def Turn(board):
    if board.count_to("✚") > board.count_to("◉"):
        turn = 2
        play_symbol = "◉"
    elif board.count_to("✚") == board.count_to("◉"):
        turn = 1
        play_symbol = "✚"
    else:
        turn = None
        play_symbol = None
    return turn, play_symbol


async def NoughtsAndCrosses(message):
    acceptable = ["o&x", "0&x", "x&o", "x&0", "o+x", "0+x", "x+o", "x+0", "onx"]
    if message.content.lower() in acceptable:
        all_squares = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
        board = ["☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐"]
        output = await message.channel.send("Noughts and Crosses", components=BuildBoard(board))
        finished_game = False
        while not finished_game:
            def check(res):
                return res.message == output and res.author == message.author

            interaction = await client.wait_for("button_click", check=check)

            illegal = False

            for square in all_squares:
                if interaction.component.custom_id == square:
                    if board[all_squares.index(square)] == "☐":
                        board = ChangeBoard(board, square, "✚")
                    else:
                        illegal = True
                        break
                    await output.edit(content="Noughts and Crosses", components=BuildBoard(board))
                    try:
                        await interaction.respond()
                    except discord.errors.HTTPException:
                        pass
                    break
            if illegal:
                continue
            if HasWon(board, "✚"):
                await message.channel.send(
                    ">>> __**YOU WIN!!! 🥳🥳🥳 **__\n**" + message.author.mention +
                    " You Beat Mr Keprins!!!**\n**You get 8 points!**")
                await give_points(message.author.id, 8, "O&X - Beat Keprins")
                return
            elif "☐" not in board:
                finished_game = True
                await message.channel.send(
                    ">>> __**" + message.author.mention + " Your game ended in a draw!**__")
            else:
                if board.count("☐") == 8:
                    if board[0] == "✚" or board[2] == "✚" or board[6] == "✚" or board[8] == "✚":
                        if randint(1, 5) != 5:
                            board[4] = "◉"
                        else:
                            if randint(1, 2) == 1:
                                which = randint(1, 3)
                                if which == 1:
                                    if board[0] == "✚":
                                        board[2] = "◉"
                                    else:
                                        board[0] = "◉"
                                elif which == 2:
                                    if board[2] == "✚":
                                        board[6] = "◉"
                                    else:
                                        board[2] = "◉"
                                elif which == 3:
                                    if board[6] == "✚":
                                        board[8] = "◉"
                                    else:
                                        board[6] = "◉"
                            else:
                                which = randint(1, 4)
                                if which == 1:
                                    board[1] = "◉"
                                elif which == 2:
                                    board[3] = "◉"
                                elif which == 3:
                                    board[5] = "◉"
                                elif which == 4:
                                    board[7] = "◉"
                    elif board[4] == "✚" or board[1] == "✚" or board[3] == "✚" or board[5] == "✚" or board[7] == "✚":
                        if randint(1, 4) == 4:
                            which = randint(1, 4)
                            if which == 1:
                                board[1] = "◉"
                            elif which == 2:
                                board[3] = "◉"
                            elif which == 3:
                                board[5] = "◉"
                            elif which == 4:
                                board[7] = "◉"
                        else:
                            which = randint(1, 4)
                            if which == 1:
                                board[0] = "◉"
                            elif which == 2:
                                board[2] = "◉"
                            elif which == 3:
                                board[6] = "◉"
                            elif which == 4:
                                board[8] = "◉"
                else:
                    sequences = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
                    changed = False
                    for sequence in sequences:
                        if WinCheck(board, sequence[0], sequence[1], sequence[2], "◉") is not None:
                            changed = True
                            break
                    if not changed:
                        for sequence in sequences:
                            if WinCheck(board, sequence[0], sequence[1], sequence[2], "✚") is not None:
                                changed = True
                                break
                        if not changed:
                            vacant = []
                            for i in range(len(board)):
                                if board[i] == "☐":
                                    vacant.append(i)
                            board[vacant[randint(0, len(vacant) - 1)]] = "◉"
                await output.edit(content="Noughts and Crosses", components=BuildBoard(board))

                if HasWon(board, "◉"):
                    await message.channel.send(
                        ">>> **" + message.author.mention + " __YOU LOST!!!__ 😭😭😭**\n**You lose 4 points!**")
                    await give_points(message.author.id, -4, "O&X - Lost to Keprins")
                    if int(data["users"][str(message.author.id)][0]) < 0:
                        data["users"][str(message.author.id)][0] = "0"
                        await update_points("Set " + str(message.author) + " points to 0, because were negative (o&x)")
                    return
                elif "☐" not in board:
                    await message.channel.send(
                        ">>> __**" + message.author.mention + " Your game ended in a draw!**__")
                    return
    elif message.content.lower()[:3] in acceptable and message.content[3] == " ":
        await message.channel.send("`" + message.content + "`")
        opponent = int(message.content[message.content.find(" ") + 1:
                                       message.content.find(" ", message.content.find(" ") + 1)][3:-1])
        bet = message.content[message.content.find(" ", message.content.find(" ") + 1):]
        if bet == "all":
            bet = int(data["users"][str(message.author.id)][0])
        elif not bet.strip().isdigit():
            await message.channel.send("Your bet needs to be an integer")
            return
        else:
            bet = int(bet)
        if len(str(opponent)) != 18:
            await message.channel.send("Your opponent needs to exist and be in this server")
        elif message.guild.get_member(opponent) is None:
            await message.channel.send("Your opponent needs to exist and be in this server")
        elif bet > int(data["users"][str(message.author.id)][0]):
            await message.channel.send("You can't bet more points than you have!")
        elif bet > int(data["users"][str(opponent)][0]):
            await message.channel.send("You can't bet more points than your opponent has!")
        elif bet <= 0:
            await message.channel.send("You can't bet nothing! HAHA!")
        else:
            challenge = await message.channel.send(
                client.get_user(opponent).mention + " You have been challenged to noughts and crosses by **" +
                message.author.name + "**\nBy accepting, you are risking `" + str(bet) +
                "` points...\nA win will give you `" + str(bet) + "` points from your opponent!", components=[[
                    Button("Accept", "accept"),
                    Button("Decline", "decline")]])

            def check(res):
                return res.message == challenge and res.author.id == opponent

            players = {1: None, 2: None}
            interaction = await client.wait_for("button_click", check=check)
            if interaction.component.custom_id == "decline":
                await challenge.edit(
                    client.get_user(opponent).mention + " You have been challenged to noughts and crosses by **" +
                    message.author.name + "**\nBy accepting, you are risking `" + str(bet) +
                    "` points...\nA win will give you `" + str(bet) + "` points from your opponent!", components=[[
                        Button("Accept", "accept"),
                        Button("Decline", "decline", color="red")]])
                await message.channel.send(client.get_user(opponent).mention + " **declined** the match!")
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
                return
            elif interaction.component.custom_id == "accept":
                await challenge.edit(
                    client.get_user(opponent).mention + " You have been challenged to noughts and crosses by **" +
                    message.author.name + "**\nBy accepting, you are risking `" + str(bet) +
                    "` points...\nA win will give you `" + str(bet) + "` points from your opponent!", components=[[
                        Button("Accept", "accept", color="green"),
                        Button("Decline", "decline")]])
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
                player_list = [message.author, client.get_user(opponent)]
                ran_num = randint(0, 1)
                players[1] = player_list[ran_num]
                players[2] = player_list[0]
                if players[1] == players[2]:
                    players[2] = player_list[1]
                top_of_msg = client.get_user(opponent).mention + \
                    " **accepted** the match!\n" + players[1].mention + " It's your turn first!\n\n\n"
            else:
                return
            all_squares = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
            board = ["☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐"]

            output = await message.channel.send(
                top_of_msg + players[1].mention + " VS " + players[2].mention, components=BuildBoard(board))
            finished_game = False

            def check(res):
                return res.message == output and res.author == players[turn]

            while not finished_game:

                turn, play_symbol = Turn(board)

                interaction = await client.wait_for("button_click", check=check)

                pass

                illegal = False

                for square in all_squares:
                    if interaction.component.custom_id == square:
                        if board[all_squares.index(square)] == "☐":
                            board = ChangeBoard(board, square, play_symbol)
                        else:
                            illegal = True
                            break
                        top_of_msg = client.get_user(opponent).mention + \
                            " **accepted** the match!\n" + players[Turn(board)[0]].mention + \
                            " __It's your turn now!__\n\n\n"

                        await output.edit(
                            top_of_msg + players[1].mention + " VS " + players[2].mention, components=BuildBoard(board))
                        try:
                            await interaction.respond()
                        except discord.errors.HTTPException:
                            pass
                        break
                if illegal:
                    continue
                if HasWon(board, "✚"):
                    await output.edit(
                        "🥳__" + players[1].mention + "__🥳 VS 😢" + players[2].mention + "😢",
                        components=BuildBoard(board)
                    )
                    await message.channel.send(
                        ">>> __**" + players[1].mention + "YOU WIN!!! 🥳🥳🥳 **__\n**" +
                        players[1].mention + "you get " + str(bet) + " points!**\n**" +
                        players[2].mention + "you *lose* " + str(bet) + " points!**")
                    await give_points(players[1].id, bet, "O&X - Won 1v1 against " +
                                      str(players[2]) + " (" + str(players[2].id) + ")")
                    await give_points(players[2].id, 0 - bet, "O&X - Lost 1v1 to " +
                                      str(players[1]) + " (" + str(players[1].id) + ")")
                    return
                elif HasWon(board, "◉"):
                    await output.edit(
                        "😢" + players[1].mention + "😢 VS 🥳__" + players[2].mention + "__🥳",
                        components=BuildBoard(board)
                    )
                    await message.channel.send(
                        ">>> __**" + players[2].mention + "YOU WIN!!!**__ 🥳🥳🥳\n\n\n**" +
                        players[2].mention + " you get " + str(bet) + " points!**\n**" +
                        players[1].mention + " you *lose* " + str(bet) + " points!**")
                    await give_points(players[2].id, bet, "O&X - Won 1v1 against " +
                                      str(players[1]) + " (" + str(players[1].id) + ")")
                    await give_points(players[1].id, 0 - bet, "O&X - Lost 1v1 to " +
                                      str(players[2]) + " (" + str(players[2].id) + ")")
                    return
                elif "☐" not in board:
                    finished_game = True
                    await message.channel.send(
                        ">>> __**" + players[1].mention + " and " + players[2].mention +
                        "\nYour game ended in a draw!**__\nNo points have been changed")


async def Bitcoin(message):
    if message.content.lower() == "bitcoin":
        aud = BtcConverter().get_latest_price('AUD')
        await message.channel.send("> **ONE BITCOIN:**\n> ```" + str(aud) + " AUD```")
    elif message.content.lower()[:8] == "bitcoin ":
        currency = message.content[8:].upper()
        bit = BtcConverter().get_latest_price(currency)
        await message.channel.send("> **ONE BITCOIN:**\n> ```" + str(bit) + " " + currency + "```")


async def Weather(message):
    thumbnails = {
        32: "https://findicons.com/files/icons/2607/tick_weather_icons/128/sunny.png",
        28: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy4.png",
        30: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy2.png",
        26: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy5.png",
        11: "https://findicons.com/files/icons/2607/tick_weather_icons/128/shower3.png",
        31: "https://findicons.com/files/icons/2607/tick_weather_icons/128/sunny_night.png",
        27: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy3_night.png",
        33: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy1_night.png",
        29: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy2_night.png",
        34: "https://findicons.com/files/icons/2607/tick_weather_icons/128/cloudy1.png",
        22: "https://findicons.com/files/icons/2607/tick_weather_icons/128/fog.png",
        14: "https://findicons.com/files/icons/2607/tick_weather_icons/128/snow4.png",
        12: "https://findicons.com/files/icons/2607/tick_weather_icons/128/shower3.png",
        16: "https://findicons.com/files/icons/2607/tick_weather_icons/128/snow5.png",
        20: "https://findicons.com/files/icons/2607/tick_weather_icons/128/fog_night.png"
    }
    if message.content.lower() == "weather":
        r_weather = getCityWeatherDetails(city="willetton", queryType="daily-data")
        weather = loads(r_weather)
        embed = discord.Embed(
            title="**Weather in __Willetton__**",
            description="Temperature: " + str(weather["vt1observation"]["temperature"]) + "°\nFeels like: " +
                        str(weather["vt1observation"]["feelsLike"]) + "°\nUV Index: " +
                        str(weather["vt1observation"]["uvIndex"]) + "\nHumidity: " +
                        str(weather["vt1observation"]["humidity"]) + "%\nWind Speeds: " +
                        str(weather["vt1observation"]["windSpeed"]) + "km/h",
            color=discord.Color.random())
        try:
            embed.set_thumbnail(url=thumbnails[int(weather["vt1observation"]["icon"])])
        except KeyError:
            await client.get_channel(941960628594167808).send(client.get_user(761124349809524746).mention +
                                                              "no weather icon known!!!")
        await message.channel.send(embed=embed)
    elif message.content.lower()[:11] == "weather in ":
        location = message.content.lower()[11:]
        try:
            r_weather = getCityWeatherDetails(city=location, queryType="daily-data")
        except KeyError:
            return
        weather = loads(r_weather)
        embed = discord.Embed(
            title="**Weather in __" + location[0].upper() + location[1:] + "__**",
            description="Temperature: " + str(weather["vt1observation"]["temperature"]) + "°\nFeels like: " +
                        str(weather["vt1observation"]["feelsLike"]) + "°\nUV Index: " +
                        str(weather["vt1observation"]["uvIndex"]) + "\nHumidity: " +
                        str(weather["vt1observation"]["humidity"]) + "%\nWind Speeds: " +
                        str(weather["vt1observation"]["windSpeed"]) + "km/h",
            color=discord.Color.random())
        try:
            embed.set_thumbnail(url=thumbnails[int(weather["vt1observation"]["icon"])])
        except KeyError:
            await client.get_channel(941960628594167808).send(client.get_user(761124349809524746).mention +
                                                              "no weather icon known!!!")
        await message.channel.send(embed=embed)
    elif message.content.lower() in \
            ["weekly weather", "weather weekly", "weekly forecast", "week forecast", "forecast week"]:
        r_weather = getCityWeatherDetails(city="willetton", queryType="ten-days-data")
        weather = loads(r_weather)
        embed = discord.Embed(
            title="**Weekly Weather Forecast for __Willetton__**",
            color=discord.Color.random()
        )
        for i in range(8):
            if i != 0:
                embed.add_field(name=weather["vt1dailyForecast"]["dayOfWeek"][i],
                                value=weather["vt1dailyForecast"]["day"]["narrative"][i],
                                inline=False)
        await message.channel.send(embed=embed)
    elif message.content.lower()[:18] == "weekly weather in " or message.content.lower()[:18] == "weather weekly in ":
        location = message.content.lower()[18:]
        r_weather = getCityWeatherDetails(city=location, queryType="ten-days-data")
        weather = loads(r_weather)
        embed = discord.Embed(
            title="**Weekly Weather Forecast for __" + location[0].upper() + location[1:] + "__**",
            color=discord.Color.random()
        )
        for i in range(8):
            if i != 0:
                embed.add_field(name=weather["vt1dailyForecast"]["dayOfWeek"][i],
                                value=weather["vt1dailyForecast"]["day"]["narrative"][i],
                                inline=False)
        await message.channel.send(embed=embed)
    elif message.content.lower() in ["hourly forecast", "24 hour forecast", "hourly weather", "24 hour weather"]:
        r_weather = getCityWeatherDetails(city="willetton", queryType="hourly-data")
        weather = loads(r_weather)
        print(weather)
        embed = discord.Embed(
            title="**Hourly Weather Forecast for __Willetton__**",
            color=discord.Color.random()
        )
        for i in range(24):
            embed.add_field(
                name=weather["vt1hourlyForecast"]["processTime"][i][11:16],
                value=str(weather["vt1hourlyForecast"]["temperature"][i])
                + "° and " + weather["vt1hourlyForecast"]["phrase"][i].replace("T-Storm", "Thunderstorm") + ". "
            )


def GetNewsEmbed(info):
    embed = discord.Embed(
        title=info["title"],
        url=info["url"],
        color=discord.Color.red()
    )
    if info["description"] is not None:
        embed.description = info["description"].replace("<p>", "").replace("</p>", "")
    if info["publishedAt"][19:] == "+00:00":
        embed.timestamp = datetime.strptime(info["publishedAt"][:19], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)
    else:
        if info["publishedAt"][19] == ".":
            embed.timestamp = datetime.strptime(info["publishedAt"][:19], "%Y-%m-%dT%H:%M:%S")
        else:
            embed.timestamp = datetime.strptime(info["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    if "author" in info:
        if info["author"] is not None:
            embed.set_author(name=info["author"] + " - " + info["source"]["name"])
        else:
            embed.set_author(name=info["source"]["name"])
    if "urlToImage" in info:
        if info["urlToImage"] != "none" and info["urlToImage"] is not None:
            if info["urlToImage"] == "//":
                info["urlToImage"] = "http:" + info["urlToImage"]
            embed.set_image(url=info["urlToImage"])
    return embed


def GNB(previous_on, next_on):
    buttons = [Button("Previous", "previous", "red", disabled=not previous_on),
               Button("Next", "next", "green", disabled=not next_on)]
    return buttons


async def News(message):
    if message.content.lower() == "news":
        news = get("https://newsapi.org/v2/everything?domains=news.com.au,abc.net.au,9news.com.au,perthnow.com.au,"
                   "smh.com.au,goulburnpost.com.au,foxsports.com.au,7news.com.au,afr.com&sortBy=popularity&"
                   "pageSize=100&from=" + datetime.strftime(now() - timedelta(hours=24), "%Y-%m-%dT%H:%M:%S") +
                   "&apiKey=493e94463d63480b85e1452be2116b37").json()
    elif message.content.lower().startswith("news "):
        term = message.content[message.content.find(" ") + 1:]
        news = get("https://newsapi.org/v2/top-headlines?q=" + term +
                   "&apiKey=493e94463d63480b85e1452be2116b37").json()
        if not news["articles"]:
            news = get("https://newsapi.org/v2/everything?q=" + term +
                       "&apiKey=493e94463d63480b85e1452be2116b37").json()
            if not news["articles"]:
                await message.channel.send("No recent News articles found which relate to `" + term + "`")
        else:
            news["articles"] = news["articles"] + get("https://newsapi.org/v2/everything?q=" + term +
                                                      "&apiKey=493e94463d63480b85e1452be2116b37").json()["articles"]
    else:
        return
    number = 0
    still_going = True
    maximum = len(news["articles"]) - 1
    if maximum == 0:
        output = await message.channel.send(embed=GetNewsEmbed(news["articles"][0]), components=[GNB(False, False)])
    else:
        output = await message.channel.send(embed=GetNewsEmbed(news["articles"][0]), components=[GNB(False, True)])

    def check(res):
        return res.message == output and res.author == message.author

    while still_going:
        interaction = await client.wait_for("button_click", check=check)
        if interaction.component.custom_id == "previous":
            if number - 1 >= 0:
                number -= 1
                if number == 0:
                    await output.edit(embed=GetNewsEmbed(news["articles"][number]), components=[GNB(False, True)])
                else:
                    await output.edit(embed=GetNewsEmbed(news["articles"][number]), components=[GNB(True, True)])
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
            else:
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
        elif interaction.component.custom_id == "next":
            if number + 1 <= maximum:
                number += 1
                if number == maximum:
                    await output.edit(embed=GetNewsEmbed(news["articles"][number]), components=[GNB(True, False)])
                else:
                    await output.edit(embed=GetNewsEmbed(news["articles"][number]), components=[GNB(True, True)])
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
            else:
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass


async def Covid(message):
    if message.content.lower() == "covid":
        res = get('https://api.covid19api.com/summary').json()
        gl = res["Global"]
        au = res["Countries"][9]
        embed = discord.Embed(
            title="COVID19 Tracker",
            color=discord.Color.random()
        )
        embed.add_field(
            name="Australia", value="New Cases: `" + str(au["NewConfirmed"]) + "`\nTotal Cases: `" +
                                    str(au["TotalConfirmed"]) + "`\n\nNew Deaths: `" + str(au["NewDeaths"]) +
                                    "`\nTotal Deaths: `" + str(au["TotalDeaths"]) + "`")
        embed.add_field(
            name="Global", value="New Cases: `" + str(gl["NewConfirmed"]) + "`\nTotal Cases: `" +
                                 str(gl["TotalConfirmed"]) + "`\n\nNew Deaths: `" + str(gl["NewDeaths"]) +
                                 "`\nTotal Deaths: `" + str(gl["TotalDeaths"]) + "`")
        await message.channel.send(embed=embed)


async def ButterChicken(message):
    if message.content.lower() in ["butter chicken", "bc", "whats abids favourite food", "waff"]:
        embed = discord.Embed(
            title="Butter Chicken",
            color=discord.Color.orange()
        )
        all_pics = bing_image_urls("butter chicken", limit=500)
        pic = all_pics[randint(0, len(all_pics) - 1)]
        embed.set_image(url=pic)
        await message.channel.send(embed=embed)


async def Image(message):
    if message.content.lower().startswith("img ") or message.content.lower().startswith("image "):
        term = message.content[message.content.find(" ") + 1:]
        if bad_word(message):
            await message.channel.send("That's a **Bad Word!**")
            return
        else:
            all_pics = bing_image_urls(term, limit=50)
            pic = all_pics[randint(0, len(all_pics) - 1)]
            embed = discord.Embed(
                title=term,
                color=discord.Color.random()
            )
            embed.set_image(url=pic)
            await message.channel.send(embed=embed)


async def Admin(message):
    admins = [761124349809524746]
    if message.author.id not in admins:
        return
    if message.content.startswith("admin.zero "):
        who = message.content[14:-1]
        data["users"][who][0] = "0"
        await update_points("ADMIN ZEROED " + who)
        await message.channel.send("**ADMIN ZEROED <@!" + who + ">**")
    if message.content.startswith("admin.points.set "):
        who = message.content[20:38]
        how_much = message.content[39:]
        try:
            x = int(how_much)
        except ValueError:
            return
        data["users"][who][0] = str(x)
        await update_points("ADMIN SET " + who + " POINTS TO " + how_much)
        await message.channel.send("**ADMIN SET <@!" + who + "> POINTS TO " + how_much + "**")


async def Translate(message):
    if message.content.lower().startswith("translate ") or message.content.lower().startswith("trans "):
        if message.content.lower()[message.content.lower().find(" ") + 3] == "/":
            base_lang = message.content.lower()[message.content.find(" ") + 1:message.content.find("/")]
            target_lang = message.content.lower()[message.content.find("/") + 1:message.content.find("/") + 3]
            text = message.content[message.content.find(" ", message.content.find(" ") + 1) + 1:]
        elif message.content.lower()[message.content.lower().find(" ") + 1] == "/":
            base_lang = None
            target_lang = message.content.lower()[message.content.find("/") + 1:
                                                  message.content.find(" ", message.content.find("/"))]
            text = message.content[message.content.find(" ", message.content.find("/")) + 1:]
        else:
            base_lang = None
            target_lang = "en"
            text = message.content[message.content.find(" ") + 1:]
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        payload = "q=" + text + "&target=" + target_lang + (("&source=" + base_lang) if base_lang is not None else "")
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
            "X-RapidAPI-Key": "4ebd273eefmsh8147e7afec4bf0fp1a99b3jsnabd87584985d"
        }

        response = request("POST", url, data=payload, headers=headers).json()

        if base_lang is None:
            base_lang = response["data"]["translations"][0]["detectedSourceLanguage"]
        await message.channel.send(embed=discord.Embed(
            title=response["data"]["translations"][0]["translatedText"],
            description="Translated from " + base_lang + " to " + target_lang,
            color=discord.colour.Color.gold()))


def Bin2Dec(binary):
    binary = str(binary)
    decimal = 0
    for n in range(len(binary)):
        decimal += int(binary[n]) * (2 ** (len(binary) - 1 - n))
    return decimal


def Dec2Bin(decimal):
    decimal = int(decimal)
    binary = ""
    for n in [128, 64, 32, 16, 8, 4, 2, 1]:
        if n <= decimal:
            binary += "1"
            decimal -= n
        else:
            binary += "0"
    return binary


async def IP(message):
    if message.content.lower().startswith("dec2bin "):
        term = message.content[8:]
        await message.reply(Dec2Bin(term))
    elif message.content.lower().startswith("bin2dec "):
        term = message.content[8:]
        await message.reply(Bin2Dec(term))


async def Streak(message):
    if message.content.lower() == "streak":
        streak = data["users"][str(message.author.id)][3]
        await message.channel.send("Your current daily streak is `" + streak + "`")
    elif message.content.lower().startswith("streak "):
        user = message.content[9:27]
        streak = data["users"][user][3]
        await message.channel.send(client.get_user(int(user)).display_name +
                                   "'s current daily streak is `" + streak + "`")


async def WeeklyMonthly(message):
    if message.content.lower() == "weekly":
        last_monday = (datetime.today() - timedelta(days=datetime.today().weekday())).strftime("%d/%m/%Y")
        last_weekly = data["users"][str(message.author.id)][8]
        # print(data["users"][str(message.author.id)])
        # print(last_monday)
        # print(last_weekly)
        if last_weekly == last_monday:
            await message.channel.send("You already did `weekly` this week!")
            return
        data["users"][str(message.author.id)][8] = last_monday
        await message.channel.send("Good job " + message.author.mention +
                                   " You get `100` points!\nCollect your weekly reward every week for free points!")
        await give_points(message.author.id, 100, "WEEKLY")
        await update_points("WEEKLY")
    elif message.content.lower() == "monthly":
        this_month = now().strftime("%m/%Y")
        last_monthly = data["users"][str(message.author.id)][9]
        # print(data["users"][str(message.author.id)])
        # print(this_month)
        # print(last_monthly)
        if last_monthly == this_month:
            await message.channel.send("You already did `monthly` this month!")
            return
        data["users"][str(message.author.id)][9] = this_month
        await message.channel.send("Good job " + message.author.mention +
                                   " You get `250` points!\nCollect your monthly reward every month for free points!")
        await give_points(message.author.id, 250, "MONTHLY")
        await update_points("MONTHLY")


async def Rhyme(message):
    if message.content.lower().startswith("rhyme "):
        term = message.content[6:]
        rhyme_json = get("https://www.abbreviations.com/services/v2/rhymes.php?"
                         "uid=10323&tokenid=RNREy7YFaB4Z5yiF&term=" + term + "&format=json").json()
        rhymes = rhyme_json["rhymes"].split(", ")
        embed = discord.Embed(
            title="Words that rhyme with *" + term + "* (" + str(len(rhymes)) + " results)",
            description=rhyme_json["rhymes"],
            colour=discord.Colour.blurple()
        )
        await message.channel.send(embed=embed)


async def Syllable(message):
    if message.content.lower().startswith("syl "):
        term = message.content[4:]
        try:
            syls = [len(list(y for y in x if y[-1].isdigit())) for x in cmudict.dict()[term.lower()]]
        except KeyError:
            await message.reply("Did not recognise that word")
            return
        syllables = syls[0]
        await message.channel.send("**" + term + "** has `" + str(syllables) + "` syllables")


def GetQuiz():
    res = get("https://the-trivia-api.com/api/questions?limit=1").json()
    while len(res[0]["correctAnswer"]) > 80 or len(res[0]["incorrectAnswers"][0]) > 80 or \
            len(res[0]["incorrectAnswers"][1]) > 80 or len(res[0]["incorrectAnswers"][2]) > 80:
        res = get("https://the-trivia-api.com/api/questions?limit=1").json()
    read_time = ((res[0]["question"].count_to(" ") + 1) / 200) * 60
    total_time = read_time + 5
    cutoff = (datetime.now() + timedelta(seconds=total_time))
    embed = discord.Embed(
        title=res[0]["question"],
        description="Time's up <t:" + str(int(round(cutoff.timestamp()))) + ":R>",
        colour=0x5865F2
    )
    return {"embed": embed, "correct": res[0]["correctAnswer"], "incorrect": res[0]["incorrectAnswers"],
            "cutoff": cutoff, "difficulty": res[0]["difficulty"]}


def GQB(options, next_button=False, wrong=None):
    if next_button:
        output = [[], [Button("Next Question", "next")]]
    else:
        output = [[]]
    for x in options:
        if next_button:
            if x[1] == "correct":
                output[0].append(Button(x[0], x[1], color="green", disabled=True))
            elif x[0] == wrong:
                output[0].append(Button(x[0], x[1], color="red", disabled=True))
            else:
                output[0].append(Button(x[0], x[1], color="gray", disabled=True))
        else:
            output[0].append(Button(x[0], x[1]))
    return output


async def Quiz(message):
    if message.content.lower() == "quiz":
        profit = 0
        quiz = GetQuiz()
        options = []
        correct_loc = random.randint(0, 3)
        inc = 0
        for i in range(4):
            if correct_loc == i:
                options.append([quiz["correct"], "correct"])
            else:
                options.append([quiz["incorrect"][inc], "incorrect" + str(inc)])
                inc += 1

        output = await message.channel.send(embed=quiz["embed"], components=GQB(options))

        def check(res):
            return res.message == output and res.author == message.author

        still_going = True
        first_time = True
        while still_going:
            if first_time:
                timeout = (quiz["cutoff"] - datetime.now()).total_seconds() + 0
            else:
                timeout = (quiz["cutoff"] - datetime.now()).total_seconds() + 1
            try:
                interaction = await client.wait_for("button_click", check=check, timeout=timeout)
                if interaction.component.custom_id == "correct":
                    if quiz["difficulty"] == "easy":
                        reward = random.randint(3, 7)
                    elif quiz["difficulty"] == "medium":
                        reward = random.randint(7, 14)
                    else:
                        reward = random.randint(14, 21)
                    profit += reward
                    await give_points(message.author.id, reward, "QUIZ")
                    await output.edit(embed=discord.Embed(
                        title="That's Correct! ✅",
                        description="You get `" + str(reward) +
                                    "` points!\nIn total, you have " + ("WON `" if profit >= 0 else "LOST `")
                                    + str(int(fabs(profit))) + "` from this quiz",
                        colour=0x77B255),
                        components=GQB(options, next_button=True)
                    )
                    try:
                        await interaction.respond()
                    except discord.errors.HTTPException:
                        pass
                elif interaction.component.custom_id[:-1] == "incorrect":
                    if quiz["difficulty"] == "easy":
                        loss = random.randint(5, 12)
                    elif quiz["difficulty"] == "medium":
                        loss = random.randint(4, 7)
                    else:
                        loss = random.randint(2, 4)
                    profit -= loss
                    await give_points(message.author.id, 0 - loss, "QUIZ")
                    await output.edit(embed=discord.Embed(
                        title="Incorrect! 👎",
                        description="You lose `" + str(loss)
                                    + "` points!\nIn total, you have " + ("WON `" if profit >= 0 else "LOST `")
                                    + str(int(fabs(profit))) + "` points from this quiz",
                        colour=0xDD2E44),
                        components=GQB(options, next_button=True, wrong=interaction.component.label)
                    )
                    try:
                        await interaction.respond()
                    except discord.errors.HTTPException:
                        pass
            except asyncio.TimeoutError:
                loss = random.randint(5, 15)
                profit -= loss
                await give_points(message.author.id, 0 - loss, "QUIZ")
                await output.edit(embed=discord.Embed(
                    title="You took too long!",
                    description="You lose `" + str(loss)
                                + "` points!\nIn total, you have " + ("WON `" if profit >= 0 else "LOST `")
                                + str(int(fabs(profit))) + "` points from this quiz",
                    colour=0xDD2E44),
                    components=GQB(options, next_button=True)
                )
            interaction = await client.wait_for("button_click", check=check)
            if interaction.component.custom_id == "next":
                quiz = GetQuiz()
                options = []
                correct_loc = random.randint(0, 3)
                inc = 0
                for i in range(4):
                    if correct_loc == i:
                        options.append([quiz["correct"], "correct"])
                    else:
                        options.append([quiz["incorrect"][inc], "incorrect" + str(inc)])
                        inc += 1

                await output.edit(embed=quiz["embed"], components=GQB(options))
                try:
                    await interaction.respond()
                except discord.errors.HTTPException:
                    pass
                first_time = True


async def Youtube(message):
    if message.content.lower().startswith("youtube ") or message.content.lower().startswith("yt "):
        term = message.content[message.content.find(" ") + 1:]
        search = VideosSearch(term, limit=1)
        # noinspection PyTypeChecker
        url = search.result()["result"][0]["link"]
        await message.channel.send(url)


def GWB(result):
    output = []
    colours = {"G": "green", "Y": "blurple", "_": "grey"}
    for one in range(len(result)):
        if result[one]:
            output.append([])
            for two in range(len(result[one])):
                output[one].append(Button(result[one][two][0], str(one) + "," + str(two), colours[result[one][two][1]]))
    return output


def AnswerAsButtons(word, colour):
    output = [[]]
    for char in range(len(word)):
        output[0].append(Button(word[char], "answer_char" + str(char), color=colour))
    return output


async def Wordle(message):
    if message.content.lower() == "wordle":
        word = get("https://random-word-api.herokuapp.com/word?length=5").json()[0]
        while not word == SpellChecker().correction(word):
            word = get("https://random-word-api.herokuapp.com/word?length=5").json()[0]
        word = word.upper()
        result = [[], [], [], [], [], []]
        output = await message.channel.send(
            message.author.mention + "'s game of Wordle", embed=discord.Embed(
                title="Guess the five letter word", colour=discord.Colour.gold()))
        in_play = True
        attempt = -1

        def check(res):
            return res.channel == message.channel and res.author == message.author

        while in_play:
            attempt += 1
            guess_input = await client.wait_for("message", check=check)
            guess = guess_input.content
            if guess == "give up":
                await output.edit(embed=discord.Embed(title="You gave up!", color=discord.Colour.red()),
                                  components=AnswerAsButtons(word, "red"))
                return
            # await guess_input.delete()
            while len(guess) != 5 or not guess == SpellChecker().correction(guess):
                await output.edit(
                    embed=discord.Embed(title="Invalid Guess. Guess again.", colour=discord.Colour.gold()))
                await output.edit(
                    embed=discord.Embed(title="Invalid Guess. Guess again.", colour=discord.Colour.red()))
                guess_input = await client.wait_for("message", check=check)
                guess = guess_input.content
                if guess == "give up":
                    await output.edit(embed=discord.Embed(title="You gave up!", color=discord.Colour.red()),
                                      components=AnswerAsButtons(word, "red"))
                    return
                # await guess_input.delete()
            guess = guess.upper()
            for char in range(len(guess)):
                if guess[char] in word:
                    if guess[char] == word[char]:
                        result[attempt].append((guess[char], "G"))
                    else:
                        result[attempt].append((guess[char], "Y"))
                else:
                    result[attempt].append((guess[char], "_"))
            if result[attempt][0][1] == "G" and result[attempt][1][1] == "G" and result[attempt][2][1] == "G" \
                    and result[attempt][3][1] == "G" and result[attempt][4][1] == "G":
                await give_points(message.author.id, 25, "WORDLE")
                await output.edit(embed=discord.Embed(
                    title="-------------- You Won! --------------", description="You get 25 points!",
                    colour=discord.Colour.green()), components=AnswerAsButtons(word, "green"))
                break
            elif attempt == 5:
                await output.edit(embed=discord.Embed(
                    title="You Failed! The answer was " + word, colour=discord.Colour.red()),
                    components=AnswerAsButtons(word, "red"))
                break
            else:
                await output.edit(embed=discord.Embed(title="Guess again", colour=discord.Colour.gold()),
                                  components=GWB(result))


@client.event
async def on_message(message):
    global message_content
    if message.author.bot:
        return
    if message.content == 'kp exit()' and message.author.id == 761124349809524746:
        await message.channel.send('**EXITING BOT**')
        await log('EXITING BOT')
        exit()
    if message.content == 'kp restart()' and message.author.id == 761124349809524746:
        await message.channel.send('**RESTARTING BOT**')
        await log('RESTARTING BOT')
        system("python restarter.py")
        system('kill 1')
    if monitor(message) is False:
        await message.delete()
        return
    if message.content[0:7] == 'kp del ' and message.author.id == 761124349809524746:
        m_id = int(message.content[7:])
        msg = await message.channel.fetch_message(m_id)
        await msg.delete()
    add_server_to_temp_data(message)
    await manage_user_data_values(message.author.id)
    await XP(message)
    if message.content.lower().startswith("kp ") or message.content.lower().startswith("mr ") or \
            message.content.lower().startswith("mk "):
        message.content = message.content[3:]
        message_content = ""
    else:
        message_content = message.content
        message.content = ""
    await censor(message)
    await spam(message)
    await cheat_alert(message)
    await collude_alert(message)
    await send_to_user(message)
    await keprins_say(message)
    await gn(message)
    await gm(message)
    await server_data(message)
    await keprins_help(message)
    await count_messages(message)
    await test_functions(message)
    await list_servers(message)
    await invite_me(message)
    await daily(message)
    await manage_points(message)
    await vote(message)
    await special_events(message)
    await Bitcoin(message)
    await Weather(message)
    await News(message)
    await Covid(message)
    await Admin(message)
    await Translate(message)
    await rate(message)
    await IP(message)
    await Streak(message)
    await joke(message)
    await WeeklyMonthly(message)
    await Rhyme(message)
    await Syllable(message)
    await Youtube(message)
    if message.guild.id == 844491934382817280:
        if 'meme' in message.channel.name or 'keprins' in message.channel.name or 'bot' in message.channel.name:
            await get_meme(message)
        if ('keprins' not in message.channel.name) and 'bot' not in message.channel.name:
            return
    if message.guild.id == 857931413755920394:
        if 'bot' not in message.channel.name:
            return
    else:
        await get_meme(message)
    if message.guild.id == 914869415835742228:
        if 'bot' not in message.channel.name:
            return
    channel(message)
    await trivia_q(message)
    await book_quote(message)
    await fact(message)
    await guess_number(message)
    await hangman(message)
    await donate(message)
    await feed(message)
    await dank_memer(message)
    await NoughtsAndCrosses(message)
    await ButterChicken(message)
    await Image(message)
    await Quiz(message)
    await Wordle(message)


client.run("MTAwODM2MTQ0MzY0MjU4NTEzOA.Gsohyk.Smvl80G-cAjGItfZ7p-0U-vwcCbjyu_E2s15EM")
