import discord, os, random
from pytrivia import Category, Diffculty, Type, Trivia
from discord.ext import commands

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")


HANGMAN_PICS =['''
 +---+
    |
    |
    |
    ===''','''
 +---+
 O   |
    |
    |
    ===''','''
 +---+
 O   |
 |  |
    |
    ===''','''
 +---+
 O   |
/|  |
    |
    ===''','''
 +---+
 O   |
/|\ |
    |
    ===''','''
 +---+
 O   |
/|\ |
/   |
    ===''','''
 +---+
 O   |
/|\ |
/ \ |
    ===''','''
 +---+
 [O  |
/|\ |
/ \ |
    ===''','''
 +---+
 [O] |
/|\ |
/ \ |
    ===''']

def difficulty():
    difficulty = 'X'
    while difficulty not in ['E', 'M', 'H']:
        print('Enter difficulty: E - Easy, M - Medium, H - Hard')
        difficulty = input().upper()
    if difficulty == 'M':
        del HANGMAN_PICS[8]
        del HANGMAN_PICS[7]
    if difficulty == 'H':
        del HANGMAN_PICS[8]
        del HANGMAN_PICS[7]
        del HANGMAN_PICS[5]
        del HANGMAN_PICS[3]

def hangmanreact(option):
    var = None
    if str(option.emoji) == ":E_icon:":
        var = "Easy"
    if str(option.emoji) == ":M_icon:":
        var = "Medium"
    if str(option.emoji) == ":H_icon:":
        var = "Hard"

def rpsreact(payload):
    var = None
    if str(payload.emoji) == "<:rock:835217380619190329>":
        var = "rock"
    if str(payload.emoji) == "📄":
        var = "paper"
    if str(payload.emoji) == "✂️":
        var = "scissors"

    return var

def rpsscore(choice1, choice2):
    score = None

    if choice1 == "rock":
        if choice2 == "rock":
            score = "Tie"
        elif choice2 == "paper":
            score = "P2"
        elif choice2 == "scissors":
            score = "P1"
    if choice1 == "paper":
        if choice2 == "rock":
            score = "P1"
        elif choice2 == "paper":
            score = "Tie"
        elif choice2 == "scissors":
            score = "P2"
    if choice1 == "scissors":
        if choice2 == "rock":
            score = "P2"
        elif choice2 == "paper":
            score = "P1"
        elif choice2 == "scissors":
            score = "Tie"

    return score

def triviareact(selection):
    var = None
    if str(selection.emoji) == "👋": # general
        var = Category.General
    if str(selection.emoji) == "📖": # books
        var = random.choice([Category.Books, Category.Comics, Category.Anime_Manga])
    if str(selection.emoji) == "🎭": # entertainment
        var = random.choice([Category.Cartoon, Category.Film, Category.Tv])
    if str(selection.emoji) == "🎮": # games
        var = random.choice([Category.Video_Games, Category.Board_Games])
    if str(selection.emoji) == "🎵": # music
        var = random.choice([Category.Music, Category.Musicals_Theatres])
    if str(selection.emoji) == "🌲": # nature
        var = random.choice([Category.Nature, Category.Animals])
    if str(selection.emoji) == "🌐": # social studies
        var = random.choice([Category.Geography, Category.History, Category.Politics])
    if str(selection.emoji) == "🧠": # nerdy stuff
        var = random.choice([Category.Gadgets, Category.Maths, Category.Computers, Category.Vehicles])
    if str(selection.emoji) == "➕": # extra
        var = random.choice([Category.Art, Category.Celebrities, Category.Mythology, Category.Sports])

    return var


@bot.event
async def on_ready():
    print("The Bot is Ready To Go!")
    await bot.change_presence(activity=discord.Game("Lounging in unboredom"))

# only 6 commands, at most, can be done

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help Info", description="A list of commands that can be used.")
    embed.add_field(name="`$help`", value="The bot respond with a list of commands that can be done.")
    embed.add_field(name="`$rps [@member]`", value="The bot will start a game of rock paper scissors.\nMention another user to play against a live player.")
    embed.add_field(name="`$trivia`", value="Start a trivia.")
    embed.set_footer(text="<required> [optional]")
    await ctx.send(embed=embed)

@bot.command()
async def demo(ctx):
    await random.choice([rps(ctx), trivia(ctx)])

@bot.command()
async def rps(ctx, member:discord.Member=None):
    member = ctx.guild.me if not member else member

    await ctx.send("Rock paper scissors starts now!")

    choice1 = None
    choice2 = None

    if member != ctx.guild.me:
        # Player 1
        await member.send("Please wait till the first player chooses")

        embed = discord.Embed(
            title="Choose Reaction",
            colour=discord.Colour.random()
        )
        embed.add_field(name="Rock", value="<:rock:835217380619190329>")
        embed.add_field(name="Paper", value="📄")
        embed.add_field(name="Scissors", value="✂️")
        msg = await ctx.author.send(embed=embed)

        await msg.add_reaction("<:rock:835217380619190329>")
        await msg.add_reaction("📄")
        await msg.add_reaction("✂️")
        
        payload = await bot.wait_for("raw_reaction_add", check=lambda payload: payload.user_id == ctx.author.id and payload.message_id == msg.id)

        choice1 = rpsreact(payload)


        # Player 2
        await ctx.author.send("Please wait till the second player chooses")

        msg = await member.send(embed=embed)

        await msg.add_reaction("<:rock:835217380619190329>")
        await msg.add_reaction("📄")
        await msg.add_reaction("✂️")
        
        payload = await bot.wait_for("raw_reaction_add", check=lambda payload: payload.user_id == member.id and payload.message_id == msg.id)

        choice2 = rpsreact(payload)

        await ctx.author.send("Check the server for scores")
        await member.send("Check the server for scores")
    else:
        # Player 1
        embed = discord.Embed(
            title="Choose Reaction",
            colour=discord.Colour.random()
        )
        embed.add_field(name="Rock", value="<:rock:835217380619190329>")
        embed.add_field(name="Paper", value="📄")
        embed.add_field(name="Scissors", value="✂️")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("<:rock:835217380619190329>")
        await msg.add_reaction("📄")
        await msg.add_reaction("✂️")
        
        payload = await bot.wait_for("raw_reaction_add", check=lambda payload: payload.member == ctx.author and payload.message_id == msg.id)

        choice1 = rpsreact(payload)


        # Bot
        choice2 = random.choice(["rock", "paper", "scissors"])
    
    score = rpsscore(choice1, choice2)

    embed = discord.Embed(
        title="Results",
        description=f"{ctx.author.name} chose: {choice1}\n{member.name} chose: {choice2}",
        colour=discord.Colour.random()
    )
    if score == "Tie":
        embed.description += "\n\nIt's a tie!"
    elif score == "P1":
        embed.description += f"\n\n{ctx.author.name} won!"
    elif score == "P2":
        embed.description += f"\n\n{member.name} won!"

    await ctx.send(embed=embed)

    return

@bot.command()
async def trivia(ctx):
    embed = discord.Embed(
        title="Choose a category:",
        colour=discord.Colour.random()
    )
    embed.add_field(name="General", value="👋")
    embed.add_field(name="Books", value="📖")
    embed.add_field(name="Entertainment", value="🎭")
    embed.add_field(name="Music", value="🎵")
    embed.add_field(name="Games", value="🎮")
    embed.add_field(name="Nature", value="🌲")
    embed.add_field(name="Social Studies", value="🌐")
    embed.add_field(name="Nerdy Stuff", value="🧠")
    embed.add_field(name="Extra", value="➕")
    msg = await ctx.send(embed=embed)

    await msg.add_reaction("👋") # general
    await msg.add_reaction("📖") # books
    await msg.add_reaction("🎭") # entertainment
    await msg.add_reaction("🎵") # music
    await msg.add_reaction("🎮") # games
    await msg.add_reaction("🌲") # nature
    await msg.add_reaction("🌐") # social studies
    await msg.add_reaction("🧠") # nerdy stuff
    await msg.add_reaction("➕") # extra

    selection = await bot.wait_for("raw_reaction_add", check=lambda selection: selection.member == ctx.author and selection.message_id == msg.id)
    my_api = Trivia(True)
    choice = my_api.request(1, triviareact(selection), random.choice([Diffculty.Easy, Diffculty.Medium, Diffculty.Hard]), random.choice([Type.Multiple_Choice, Type.True_False]))

    embed = discord.Embed(
        title=f"Category: {choice['results'][0]['category']}",
        description=f"**Question:**\n{choice['results'][0]['question']}\n\n**Answers:**\n",
        colour=discord.Colour.random()
    )
    embed.set_footer(text=f"Difficulty: {choice['results'][0]['difficulty'].capitalize()}")

    answers = list(choice['results'][0]['incorrect_answers'])
    answers.append(choice['results'][0]['correct_answer'])

    if choice['results'][0]['type'] == "multiple":
        choice1 = random.choice(answers)
        del answers[answers.index(choice1)]
        choice2 = random.choice(answers)
        del answers[answers.index(choice2)]
        choice3 = random.choice(answers)
        del answers[answers.index(choice3)]
        choice4 = random.choice(answers)
        del answers[answers.index(choice4)]

        embed.description += f":one: **{choice1}**\n:two: **{choice2}**\n:three: **{choice3}**\n:four: **{choice4}**"
    else:
        embed.description += ":white_check_mark: **True**\n:x: **False**"

    msg = await ctx.send(embed=embed)
        
    if choice['results'][0]['type'] == "multiple":
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        await msg.add_reaction("4️⃣")
    else:
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

    payload = await bot.wait_for("raw_reaction_add", check=lambda payload: payload.member == ctx.author and payload.message_id == msg.id)

    if choice['results'][0]['type'] == "multiple":
        if str(payload.emoji) == "1️⃣":
            if choice1 in choice['results'][0]['incorrect_answers']:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")
            else:
                await ctx.send("✅ Nice job!")
        if str(payload.emoji) == "2️⃣":
            if choice2 in choice['results'][0]['incorrect_answers']:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")
            else:
                await ctx.send("✅ Nice job!")
        if str(payload.emoji) == "3️⃣":
            if choice3 in choice['results'][0]['incorrect_answers']:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")
            else:
                await ctx.send("✅ Nice job!")
        if str(payload.emoji) == "4️⃣":
            if choice4 in choice['results'][0]['incorrect_answers']:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")
            else:
                await ctx.send("✅ Nice job!")

    else:
        if str(payload.emoji) == "✅":
            if choice['results'][0]['correct_answer'] == "True":
                await ctx.send("✅ Nice job!")
            else:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")
        if str(payload.emoji) == "❌":
            if choice['results'][0]['correct_answer'] == "False":
                await ctx.send("✅ Nice job!")
            else:
                await ctx.send(f"❌ Incorrect answer, the correct answer is {choice['results'][0]['correct_answer']}")


    # await ctx.send(choice["results"][0]["question"])


@bot.command()
async def hangman(ctx):
    pass
    words = {'Colors':'red orange yellow green blue indigo violet white black brown'.split(),
             'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
             'Fruits':'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
             'Animals':'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()
             }
    
    embed = discord.Embed(
        title="Hangman",
        colour=discord.Colour.random()
    )
    embed.add_field(name="Easy", value=":E_icon:")
    embed.add_field(name="Medium", value=":M_icon:")
    embed.add_field(name="Hard", value=":H_icon:")
    msg = await ctx.send(embed=embed)
    
    await msg.add_reaction(":E_icon:")
    await msg.add_reaction(":M_icon:")
    await msg.add_reaction(":H_icon:")
    
    option = await bot.wait_for("raw_reaction_add", check=lambda option: option.member == ctx.author and option.message_id == msg.id)

bot.run("ODM1MDcxODUxNjM3Mzc0OTc2.YIKHRA.78T4D389pmBxH7WjjeOAJ9bRCx4")