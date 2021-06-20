import random
import asyncio
import discord
import trivia_api
import datetime
import time
import csv
from Players import Players
#numberemojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
#player1 = player2 = None
member_list=[]
olm = []
#point1 = point2 = 0

async def get_members_list(channel, author, bot):
  global member_list

  member_list=channel.members

  olm = [m for m in member_list if (str(m.status) == 'online' and m.display_name != author.display_name and m.display_name != "DishaGame")]
  for chan in bot.guilds[0].text_channels:
    if chan.name != "general":
      alrdy_play = chan.members
      for i in alrdy_play:
        try:
          olm.remove(i)
        except:
          pass
  print(olm)
  if len(olm)!=0:
    await find_random(olm, author, bot)
  else:
    await display(bot,'No online user present.Try again later!')

async def find_random(member_list, author, bot):
  #global player1, player2
  random_player=random.choice(member_list)
  print(random_player)
  player1 = Players(author)
  player2 = Players(random_player)
  await match(bot, player1, player2)

async def display(bot,msg):
   channel=bot.get_channel(840989883510161422) #member.guild.get_channel
   msg_obj = await channel.send(msg)
   return msg_obj#msg object returns complete delail of msg
   
async def match(bot, player1, player2):
  #global player1, player2
  msg_obj=await display(bot,player1.player.display_name+' challenged <@'+str(player2.player.id)+'>. Do you want to Play a Trivia Game ?')
  await msg_obj.add_reaction('👍')
  await msg_obj.add_reaction('👎')

  await asyncio.sleep(0.2)

  def check(reaction,user):
    #print(str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')
    return reaction.message.id == msg_obj.id and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎') and user.id==player2.player.id
    
  try:
    reaction, user = await bot.wait_for('reaction_add', check=check, timeout=25.0)
  except asyncio.TimeoutError:
    await bot.get_channel(840989883510161422).send(player2.player.display_name+' has not responded to your challenge!')
  else:
    if user.display_name == player2.player.display_name and str(reaction.emoji) == '👎':
      await bot.get_channel(840989883510161422).send(player2.player.display_name+' has declined your challenge!')
    elif user.display_name == player2.player.display_name and str(reaction.emoji) == '👍':
      await bot.get_channel(840989883510161422).send(player2.player.display_name+' has accepted your challenge!')
    
      await asyncio.sleep(0.1)

      channel1=await bot.get_guild(840989883510161418).create_text_channel(player1.player.display_name+"_vs_"+player2.player.display_name)

      await asyncio.sleep(0.5)

     # perms = discord.Permissions(view_channel=False)
      role = await bot.get_guild(840989883510161418).create_role(name = player1.player.display_name+"_vs_"+player2.player.display_name)

      await channel1.set_permissions(role, view_channel=False)

      await asyncio.sleep(0.5)

      await add_role1(msg_obj, bot, player1, player2)

      player1.setChannel(channel1)

      quiz = await trivia_api.data()

      await start_match(bot, quiz, player1, player2)

      #await asyncio.sleep(60)

      await channel1.delete()
      await role.delete()
      await bot.get_channel(840989883510161422).send("Score: - \n"+player1.player.display_name+": "+str(player1.getScore())+"\n"+player2.player.display_name+": "+str(player2.getScore()))

      if player1.getScore() > player2.getScore():
        await bot.get_channel(840989883510161422).send("Congratulations <@"+str(player1.player.id)+">! You won the match!")
      elif player1.getScore() == player2.getScore():
        await bot.get_channel(840989883510161422).send("Draw Match!")
      else:
        await bot.get_channel(840989883510161422).send("Congratulations <@"+str(player2.player.id)+">! You have won the match!")

      with open('score.csv', mode='a') as score_file:
        score_writer = csv.writer(score_file, delimiter=',')
        t = time.time()
        score_writer.writerow([t, player1.player.id,player1.player.display_name, player1.getScore(), 'win' if player1.getScore()>player2.getScore() else 'lose'])
        score_writer.writerow([t, player2.player.id,player2.player.display_name, player2.getScore(), 'lose' if player1.getScore()>player2.getScore() else 'win'])
  
async def add_role1(msg_obj, bot, player1, player2):
  #global member_list
  try:
    member_list.remove(player1.player)
  except:
    pass
  try:
    member_list.remove(player2.player)
  except:
    pass
  try:
    member_list.remove(bot.user)
  except:
    pass
  print(member_list)
  var = discord.utils.get(msg_obj.guild.roles, name = player1.player.display_name+"_vs_"+player2.player.display_name)
  #await player2.add_roles(var)
  for member in member_list:
    await member.add_roles(var)
    await asyncio.sleep(0.5)

async def start_match(bot, quiz, player1, player2):
  #global point1,point2
  for que,opt in quiz.items():
    await asyncio.sleep(2)
    await player1.getChannel().send(que)
    await asyncio.sleep(0.5)
    for o in range(len(opt)-1):
      oo = await player1.getChannel().send(opt[o])
      await oo.add_reaction('✅')
      await asyncio.sleep(0.1)
    print(opt[-1])

    def check(reaction,user):
      return  str(reaction.emoji) == '✅' and user.display_name != "DishaGame" and reaction.message.channel.id == player1.getChannel().id
    start = datetime.datetime.now()
    try:
      reaction1, user1 = await bot.wait_for('reaction_add', check=check, timeout=30.0)
    except asyncio.TimeoutError:
      await player1.getChannel().send("No one responded to this question")
    else:
      if reaction1.message.content==opt[-1]:
        await player1.getChannel().send("Correct answer. Well played "+user1.display_name+". You scored 4 Points.")
        if str(user1.id) == str(player1.player.id):
          player1.setScore(player1.getScore() + 4)
        else:
          player2.setScore(player2.getScore() + 4)
      else:
          await reaction1.remove(user1)
          if str(user1.id) == str(player1.player.id):
            player1.setScore(player1.getScore() - 1)
          else:
            player2.setScore(player2.getScore() - 1)
          await player1.getChannel().send("Sorry, It's Incorrect. "+user1.display_name+". lose 1 Point.")

          def check1(reaction,user2):
            return  str(reaction.emoji) == '✅' and user1.id!=user2.id and user2.display_name != "DishaGame" and reaction.message.channel.id == player1.getChannel().id

          try:
            end=datetime.datetime.now()
            a=(end-start).total_seconds()
            reaction2, user2 = await bot.wait_for('reaction_add', check=check1, timeout=30.0-a)
          except asyncio.TimeoutError:
            await player1.getChannel().send("No one responded correct for this question")
          else:
              if reaction2.message.content==opt[-1]:
                await player1.getChannel().send("Correct answer. Well played "+user2.display_name+". You scored 4 Points.")
                if str(user2.id) == str(player1.player.id):
                  player1.setScore(player1.getScore() + 4)
                else:
                  player2.setScore(player2.getScore() + 4)
              else:
                await reaction2.remove(user2)
                await player1.getChannel().send("Sorry, It's Incorrect. "+user2.display_name+". lose 1 Point.")
                if str(user2.id) == str(player1.player.id):
                  player1.setScore(player1.getScore() - 1)
                else:
                  player2.setScore(player2.getScore() - 1)
                await player1.getChannel().send("Nobody gave the correct answer!")