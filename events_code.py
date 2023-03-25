async def due_alert(until, event_name, event_channel, event_date, event_time, event_members):
    if until == "ten":
        title_part = "**10 Minutes Remaining** until"
    elif until == "now":
        title_part = "**Due Date is NOW for **"
    else:
        title_part = "**One " + until[0].upper() + until[1:] + " Remaining** until"
    e_channel = client.get_channel(int(event_channel))
    embed = discord.Embed(
        title=title_part + " __" + event_name + "__!",
        description="This is an important due date for __" + e_channel.name + "__ in __" +
                    e_channel.guild.name + "__\n",
        color=discord.Color.random())
    embed.set_author(name="Upcoming Event")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/app-icons/890512432135557141/296de1168a83a3cfe100a8307a445bce.png?size=512")
    embed.add_field(name="Date", value="*" + event_date + "*\n", inline=True)
    embed.add_field(name="Time", value="*" + event_time + "*\n", inline=True)
    embed.set_footer(text="See upcoming events with the `events` command")
    await e_channel.send(">>> Attention " + event_members + "!", embed=embed)
    await log("Due Date Alert sent to " + e_channel.name + " (" + str(event_channel) +
              ") in " + e_channel.guild.name + " (" +
              e_channel.guild.id + ")")


async def wait_for(event_channel, event_name, event_date, event_time, event_members, mode):
    fmt = "%d/%m/%Y %H:%M"
    event_datetime = event_date + " " + event_time
    tdelta = datetime.strptime(event_datetime, fmt) - now()
    seconds_until = int(tdelta.total_seconds())
    if seconds_until <= 5:
        return
    e_channel = client.get_channel(int(event_channel))
    if mode == "event":
        await asyncio.sleep(seconds_until)
        embed = discord.Embed(
            title="It is now: __**" + event_name + "**__!",
            description="An event for __" + e_channel.name + "__ in __" +
                        e_channel.guild.name + "__\n",
            color=discord.Color.random())
        embed.set_author(name="EVENT ALERT!")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/app-icons/890512432135557141/296de1168a83a3cfe100a8307a445bce.png?size=512")
        embed.add_field(name="Date", value="*" + event_date + "*\n", inline=True)
        embed.add_field(name="Time", value="*" + event_time + "*\n", inline=True)
        embed.set_footer(text="See upcoming events with the `events` command")
        await e_channel.send(
            ">>> Attention " + event_members + "!", embed=embed
        )
        await log("Event Alert sent to " + e_channel.name + " (" + str(event_channel) +
                  ") in " + e_channel.guild.name + " (" +
                  e_channel.guild.id + ")")
        temp_members = event_members
        mentions = []
        while "<@!" in event_members:
            mentions.append(int(temp_members[temp_members.find("<@!") + 3:temp_members.find("<@!") + 21]))
            temp_members.replace("<@!", "000", 1)
        if "@everyone" in event_members:
            for member in e_channel.guild.members:
                mentions.append(member.id)
        if mentions:
            for user_id in mentions:
                the_user = client.get_user(user_id)
                await the_user.send(
                    ">>> Attention " + the_user.mention + "!", embed=embed)
            await log("Sent Event Alert (" + event_name + ") to:\n" + str(mentions))
    elif mode == "due_date":
        week = int((datetime.strptime(event_datetime, fmt) - timedelta(weeks=1) - now()).total_seconds())
        day = int((datetime.strptime(event_datetime, fmt) - timedelta(days=1) - now()).total_seconds())
        hour = int((datetime.strptime(event_datetime, fmt) - timedelta(hours=1) - now()).total_seconds())
        ten = int((datetime.strptime(event_datetime, fmt) - timedelta(minutes=10) - now()).total_seconds())
        if week > 5:
            await asyncio.sleep(week)
            await due_alert("week", event_name, event_channel, event_date, event_time, event_members)
            day = int((datetime.strptime(event_datetime, fmt) - timedelta(days=1) - now()).total_seconds())
            await asyncio.sleep(day)
            await due_alert("day", event_name, event_channel, event_date, event_time, event_members)
            hour = int((datetime.strptime(event_datetime, fmt) - timedelta(hours=1) - now()).total_seconds())
            await asyncio.sleep(hour)
            await due_alert("hour", event_name, event_channel, event_date, event_time, event_members)
            ten = int((datetime.strptime(event_datetime, fmt) - timedelta(minutes=10) - now()).total_seconds())
            await asyncio.sleep(ten)
            await due_alert("ten", event_name, event_channel, event_date, event_time, event_members)
            seconds_until = int((datetime.strptime(event_datetime, fmt) - now()).total_seconds())
            await asyncio.sleep(seconds_until)
            await due_alert("now", event_name, event_channel, event_date, event_time, event_members)
        elif day > 5:
            await asyncio.sleep(day)
            await due_alert("day", event_name, event_channel, event_date, event_time, event_members)
            hour = int((datetime.strptime(event_datetime, fmt) - timedelta(hours=1) - now()).total_seconds())
            await asyncio.sleep(hour)
            await due_alert("hour", event_name, event_channel, event_date, event_time, event_members)
            ten = int((datetime.strptime(event_datetime, fmt) - timedelta(minutes=10) - now()).total_seconds())
            await asyncio.sleep(ten)
            await due_alert("ten", event_name, event_channel, event_date, event_time, event_members)
            seconds_until = int((datetime.strptime(event_datetime, fmt) - now()).total_seconds())
            await asyncio.sleep(seconds_until)
            await due_alert("now", event_name, event_channel, event_date, event_time, event_members)
        elif hour > 5:
            await asyncio.sleep(hour)
            await due_alert("hour", event_name, event_channel, event_date, event_time, event_members)
            ten = int((datetime.strptime(event_datetime, fmt) - timedelta(minutes=10) - now()).total_seconds())
            await asyncio.sleep(ten)
            await due_alert("ten", event_name, event_channel, event_date, event_time, event_members)
            seconds_until = int((datetime.strptime(event_datetime, fmt) - now()).total_seconds())
            await asyncio.sleep(seconds_until)
            await due_alert("now", event_name, event_channel, event_date, event_time, event_members)
        elif ten > 5:
            await asyncio.sleep(ten)
            await due_alert("ten", event_name, event_channel, event_date, event_time, event_members)
            seconds_until = int((datetime.strptime(event_datetime, fmt) - now()).total_seconds())
            await asyncio.sleep(seconds_until)
            await due_alert("now", event_name, event_channel, event_date, event_time, event_members)
        else:
            seconds_until = int((datetime.strptime(event_datetime, fmt) - now()).total_seconds())
            await asyncio.sleep(seconds_until)
            await due_alert("now", event_name, event_channel, event_date, event_time, event_members)


# Retrieve data from events file
events_file_content_raw = repository.get_contents('events.txt')
events_file_content = events_file_content_raw.decoded_content.decode()
lines = events_file_content.split('\n')
for line in lines:
    double_colon = line.find(',,')
    event = line[:double_colon]
    current_values = line[double_colon + 2:]
    values = current_values.split(',')
    if event != "":
        data["events"][event] = values








put in @client.event:

    for this_event in data["events"]:
        await wait_for(int(data["events"][this_event][0]), this_event, data["events"][this_event][1],
                       data["events"][this_event][2], data["events"][this_event][3], data["events"][this_event][4])




async def manage_events(message):
    event_managers = {
        844491934382817280: [  # Gate server
            598843878363365387, 749926934586327080, 679825168784556073, 943773108819619850
        ],
        876358617568276500: [  # unofficial gate
            755328076363333673
        ],
        883637798081540116: [  # mastersneeza
            403122229396635649, 379951076343939072,
        ],
        857931413755920394: [  # smp server
            698701695592431676, 749926934586327080
        ],
        724527366377832479: [  # 9s server
            757746372144267284, 724247824857825331, 624028852561248288, 599927962103578624, 712585245446373418,
            872045917237309490, 751223885395132436, 706774445569605662, 680682053443911680, 750647870419501157,
            767572634061111316, 713293646530871332, 637632965672697866, 551173840995352579, 859042886292996108,
            897777798150782997, 606783276618612736
        ],
        942611622097211412: [  # Valo official
            637632965672697866, 600195443434979338, 694740430247428097
        ],
        878230885453938718: [  # everyting's axolotl
            637632965672697866, 403122229396635649, 639652781933723648, 943773108819619850, 727817830459899944,
            669900571771404288
        ],
        890201312677998622: []  # shs official
    }
    universal_eventeers = [
        761124349809524746, 721334601376727121, 783967717140332594, 852158639917891624, 676774613514190868,
        445498176007438337, 535610553347997716
    ]
    mode = None
    if message.content.lower()[:10] == "add_event," or message.content.lower()[:10] == "add event,":
        mode = "event"
        if ((message.guild.id in event_managers) and (message.author.id not in event_managers[message.guild.id])) \
                and message.author.id not in universal_eventeers:
            await message.channel.send(message.author.mention + "! You aren't allowed to use that command!")
            return
    elif message.content.lower()[:9] == "due_date," or message.content.lower()[:9] == "due date,":
        mode = "due_date"
        if ((message.guild.id in event_managers) and (message.author.id not in event_managers[message.guild.id])) \
                and message.author.id != 761124349809524746:
            await message.channel.send(message.author.mention + "! You aren't allowed to use that command!")
            return
    if mode == "event" or mode == "due_date":
        parts = message.content.split(",")
        for part in range(len(parts)):
            parts[part] = parts[part].strip()
        if len(parts) < 3:
            await message.channel.send("The command you gave was wrong! The syntax is:\n`kp add_event,"
                                       " <name>, <date>, [time], [who to ping]`")
            return
        elif len(parts) == 3:
            parts.append("00:00")
            parts.append("everyone")
        elif len(parts) == 4:
            parts.append("everyone")
        elif len(parts) > 5:
            await message.channel.send("The command you gave was wrong! The syntax is:\n`kp add_event,"
                                       " <name>, <date>, [time], [who to ping]`")
            return
        event_name = parts[1]
        event_date = parts[2]
        event_time = parts[3]
        event_members = parts[4]
        if event_name in data["events"]:
            await message.channel.send("An event called " + event_name + " already exists!")
            return
        if bad_word(message):
            await message.channel.send("The event cannot be named using a bad word!")
            return
        if event_date == "today":
            event_date = now().strftime("%d/%m/%Y")
        if event_date == "tomorrow" or event_date == "tmw" or event_date == "tmr" or event_date == "tommorow":
            event_date = (now() + timedelta(days=1)).strftime("%d/%m/%Y")
        try:
            datetime.strptime(event_date, "%d/%m/%Y")
        except ValueError:
            await message.channel.send("The date is invalid! Remember to use format dd/mm/yyyy")
            return
        try:
            datetime.strptime(event_time, "%H:%M")
        except ValueError:
            await message.channel.send("The time is invalid! Remember to use format HH:MM with __24-hour time__!")
            return
        if int((datetime.strptime(event_date + event_time, "%d/%m/%Y%H:%M") - now()).total_seconds()) < 0:
            await message.channel.send("The event must be in the future, not the past!")
            return
        data["events"][event_name] = [str(message.channel.id), event_date, event_time, event_members, mode]
        await update_events("Add event: " + event_name)
        if mode == "event":
            await message.channel.send(
                "*Event Added:*\nname=`" + event_name + "`\ndate=`" + event_date + "`\ntime=`" +
                event_time + "`\nmembers=`" + event_members + "`\nchannel=`" + message.channel.name + "`")
            await log("Event Added| name=" + event_name + "| date=" + event_date + "| time=" + event_time +
                      "| members=" + event_members + "| channel=#" + message.channel.name + " in " +
                      message.guild.name + " (" + str(message.channel.id) + ")")
            await wait_for(message.channel.id, event_name, event_date, event_time, event_members, "event")
        elif mode == "due_date":
            await message.channel.send(
                "*Due Date Added:*\nname=`" + event_name + "`\ndate=`" + event_date + "`\ntime=`" +
                event_time + "`\nmembers=`" + event_members + "`\nchannel=`" + message.channel.name + "`")
            await log("Due Date Added| name=" + event_name + "| date=" + event_date + "| time=" + event_time +
                      "| members=" + event_members + "| channel=#" + message.channel.name + " in " +
                      message.guild.name + " (" + str(message.channel.id) + ")")
            await wait_for(message.channel.id, event_name, event_date, event_time, event_members, "due_date")
    if message.content.lower() == "next event" or message.content.lower() == "next_event":
        refined = False
        while not refined:
            i = 0
            for x in data["events"]:
                i += 1
                if int((datetime.strptime(
                        data["events"][x][1] + data["events"][x][2], "%d/%m/%Y%H:%M") - now()).total_seconds()) < 0:
                    data["events"].pop(x)
                    break
                if i == len(data["events"]):
                    refined = True
        await update_events("Removed overdue events (if they exist)")
        if len(data["events"]) == 0:
            await message.channel.send("**No Upcoming Events!**")
            return
        next_event = None
        for v in data["events"]:
            if client.get_channel(int(data["events"][v][0])).guild == message.guild:
                next_event = v
        if next_event is None:
            await message.channel.send("**No Upcoming Events!**")
            return
        for e in data["events"]:
            tdelta = datetime.strptime(data["events"][e][1] + data["events"][e][2], "%d/%m/%Y%H:%M") - now()
            until = tdelta.total_seconds()
            next_delta = datetime.strptime(data["events"][next_event][1] +
                                           data["events"][next_event][2], "%d/%m/%Y%H:%M") - now()
            next_until = next_delta.total_seconds()
            if until < next_until and message.guild == client.get_channel(int(data["events"][next_event][0])).guild:
                next_event = e
        date = data["events"][next_event][1]
        time = data["events"][next_event][2]
        embed = discord.Embed(
            title=next_event,
            description="At __" + time + "__ on __" + date + "__",
            color=discord.Color.random())
        embed.set_author(name="Next Event:")
        await message.channel.send(embed=embed)
    if message.content.lower() == "events" or message.content.lower() == "show events":
        refined = False
        while not refined:
            i = 0
            for x in data["events"]:
                i += 1
                if int((datetime.strptime(
                        data["events"][x][1] + data["events"][x][2], "%d/%m/%Y%H:%M") - now()).total_seconds()) < 0:
                    data["events"].pop(x)
                    break
                if i == len(data["events"]):
                    refined = True
        await update_events("Removed overdue events (if they exist)")
        if len(data["events"]) == 0:
            await message.channel.send("**No Upcoming Events!**")
            return
        in_order = [list(data["events"].keys())[0]]
        for old in list(data["events"].keys())[1:]:
            is_in = False
            for new in range(len(in_order)):
                old_seconds = (datetime.strptime(data["events"][old][1] + data["events"][old][2],
                                                 "%d/%m/%Y%H:%M") - now()).total_seconds()
                new_seconds = \
                    (datetime.strptime(data["events"][in_order[new]][1] + data["events"][in_order[new]][2],
                                       "%d/%m/%Y%H:%M") - now()).total_seconds()
                if old_seconds < new_seconds and message.guild == client.get_channel(int(data["events"][old][0])).guild:
                    in_order.insert(0, old)
                    is_in = True
                if len(in_order) > 5:
                    in_order.pop()
            if not is_in:
                in_order.append(old)
            if len(in_order) > 5:
                in_order.pop()
        embed = discord.Embed(
            title="**Upcoming Events**",
            description="\n",
            color=discord.Color.random())
        embed.set_author(name="__" + message.channel.name + "__")
        embed.set_footer(text="Add an event with the `add_event` command")
        for this_one in in_order:
            date = data["events"][this_one][1]
            time = data["events"][this_one][2]
            if data["events"][this_one][4] == "due_date":
                embed.add_field(name=this_one + " (Due Date)", value="*" + date + " " + time + "*\n", inline=False)
            else:
                embed.add_field(name=this_one, value="*" + date + " " + time + "*\n", inline=False)
        await message.channel.send(embed=embed)










