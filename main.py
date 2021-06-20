import discord
from discord.ext import commands
import initiate_match
import os


from game import game
game()


intents = discord.Intents.all()

bot=commands.Bot(command_prefix='!',intents=intents)

@bot.event  #annotation-it detect the event
async def on_ready():
  print("I am",bot.user)
  #await bot.get_channel(840989883510161422).send(str(bot.user)+" got activated")#channel id(get from url)
  msg = await bot.get_channel(840989883510161422).send('''How To Play:-
    1.To play the Trivia Game, Please send "$match" without quotes.
    2.An online player will be selected Randomly.
    3.To accept a challange, Please react with a 👍 within 25secs.
    4.To decline the challange, Please react with a 👎.
    5.When a player accepts your challange, A seperate private channel is created with the name of <player1>\_vs\_<player2>.
    6.Kindly visit that private channel and play the Game.
    7.This game consist of 3 Questions having 4 Options each.
    8.Right option has 4 points and wrong option has -1 point.
    9.You have to react with ✅ against the right option to respond to a question.
    10.Once an user has selected an option he will be blocked for selecting other options again.
    11.If the selected option is right then, Another question will appear.
    12.You have 30secs to select an option.''')
  await msg.pin(reason="How To Play Manual!")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith("$match"):
    await initiate_match.get_members_list(bot.get_channel(840989883510161422), message.author, bot)

@bot.event
async def on_member_join(member):
  channel=bot.get_channel(840989883510161422) #member.guild.get_channel
  await channel.send("Welcome <@"+member.id+'>! Kindly check pinned rules to follow for the game.')

bot.run(os.environ['TOKEN'])