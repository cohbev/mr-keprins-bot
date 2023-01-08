def ox_get_board_view(board_values):
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


def ox_change_board(board, change_pos, change_char):
    new_board = board
    all_squares = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
    new_board[all_squares.index(change_pos)] = change_char
    return new_board


def ox_check_for_win(board, pos1, pos2, pos3, check):
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


def ox_has_won(board, xo):
    return board[0] == xo and board[1] == xo and board[2] == xo \
           or board[3] == xo and board[4] == xo and board[5] == xo \
           or board[6] == xo and board[7] == xo and board[8] == xo \
           or board[0] == xo and board[3] == xo and board[6] == xo \
           or board[1] == xo and board[4] == xo and board[7] == xo \
           or board[2] == xo and board[5] == xo and board[8] == xo \
           or board[0] == xo and board[4] == xo and board[8] == xo \
           or board[2] == xo and board[4] == xo and board[6] == xo


def ox_turn(board):
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


async def noughts_and_crosses(message):
    acceptable = ["o&x", "0&x", "x&o", "x&0", "o+x", "0+x", "x+o", "x+0", "onx"]
    if message.content.lower() in acceptable:
        all_squares = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
        board = ["☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐", "☐"]
        output = await message.channel.send("Noughts and Crosses", components=ox_get_board_view(board))
        finished_game = False
        while not finished_game:
            def check(res):
                return res.message == output and res.author == message.author

            interaction = await client.wait_for("button_click", check=check)

            illegal = False

            for square in all_squares:
                if interaction.component.custom_id == square:
                    if board[all_squares.index(square)] == "☐":
                        board = ox_change_board(board, square, "✚")
                    else:
                        illegal = True
                        break
                    await output.edit(content="Noughts and Crosses", components=ox_get_board_view(board))
                    try:
                        await interaction.respond()
                    except discord.errors.HTTPException:
                        pass
                    break
            if illegal:
                continue
            if ox_has_won(board, "✚"):
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
                        if ox_check_for_win(board, sequence[0], sequence[1], sequence[2], "◉") is not None:
                            changed = True
                            break
                    if not changed:
                        for sequence in sequences:
                            if ox_check_for_win(board, sequence[0], sequence[1], sequence[2], "✚") is not None:
                                changed = True
                                break
                        if not changed:
                            vacant = []
                            for i in range(len(board)):
                                if board[i] == "☐":
                                    vacant.append(i)
                            board[vacant[randint(0, len(vacant) - 1)]] = "◉"
                await output.edit(content="Noughts and Crosses", components=ox_get_board_view(board))

                if ox_has_won(board, "◉"):
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
                top_of_msg + players[1].mention + " VS " + players[2].mention, components=ox_get_board_view(board))
            finished_game = False

            def check(res):
                return res.message == output and res.author == players[turn]

            while not finished_game:

                turn, play_symbol = ox_turn(board)

                interaction = await client.wait_for("button_click", check=check)

                pass

                illegal = False

                for square in all_squares:
                    if interaction.component.custom_id == square:
                        if board[all_squares.index(square)] == "☐":
                            board = ox_change_board(board, square, play_symbol)
                        else:
                            illegal = True
                            break
                        top_of_msg = client.get_user(opponent).mention + \
                            " **accepted** the match!\n" + players[ox_turn(board)[0]].mention + \
                            " __It's your turn now!__\n\n\n"

                        await output.edit(
                            top_of_msg + players[1].mention + " VS " + players[2].mention, components=ox_get_board_view(board))
                        try:
                            await interaction.respond()
                        except discord.errors.HTTPException:
                            pass
                        break
                if illegal:
                    continue
                if ox_has_won(board, "✚"):
                    await output.edit(
                        "🥳__" + players[1].mention + "__🥳 VS 😢" + players[2].mention + "😢",
                        components=ox_get_board_view(board)
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
                elif ox_has_won(board, "◉"):
                    await output.edit(
                        "😢" + players[1].mention + "😢 VS 🥳__" + players[2].mention + "__🥳",
                        components=ox_get_board_view(board)
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