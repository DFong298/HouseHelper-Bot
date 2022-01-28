import discord
import os
import random
import calendar
import datetime
from discord.ext import commands, tasks

token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
client.run(token)

#bot initialization
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with fire"))
    rent_reminder.start()
    print('Bot is running')

#.help command
@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title = 'LIST OF COMMANDS',
        description = 'Feel free to give suggestions for bot functions',
        colour = discord.Colour.blue()
    )

    help_embed.set_footer(text='More to come soon')
    help_embed.set_author(name='Bot made by Dennis', 
    icon_url='https://www.streamscheme.com/wp-content/uploads/2020/07/kekw-emote.jpg')
    help_embed.add_field(name='.yn [Question]', value='Replies with an answer to a yes/no question', inline=False)
    help_embed.add_field(name='.wp', value='Generates random image of anime girl (or girls) from small selection (WIP)', inline=False)
    help_embed.add_field(name='.ac [Chore]', value='Adds [Chore] into the list of chores, if not already in (Please only add your own chores)', inline=False)
    help_embed.add_field(name='.rc [Chore]', value='Removes [Chore] from the list of chores if it is in the list', inline=False)
    help_embed.add_field(name='.chores', value='Displays the chores that are in the list with the name of the person who added it', inline=False)
    help_embed.set_thumbnail(url='https://i.imgur.com/rdj6qyu.png')

    await ctx.send(embed=help_embed)

#monthly rent reminder
@tasks.loop(hours=24)
async def rent_reminder():
    current_time = datetime.datetime.now()
    current_day = current_time.day
    current_month = current_time.month
    current_hour = current_time.hour
    channel = client.get_channel(process.env.announce_channel_id) #announcements channel
    if current_hour == 10:
        if current_month == 1:
            if current_day == 30:
                 await channel.send("Rent for February is due soon!")
        elif current_month == 2:
            if current_day == 27:
                await channel.send("Rent for March is due soon!")
        elif current_month == 3:
            if current_day == 30:
                await channel.send("Rent for April is due soon!")
        elif current_month == 4:
            if current_day == 29:
                await channel.send("Rent for May is due soon!")
        elif current_month == 5:
            if current_day == 30:
                await channel.send("Rent for June is due soon!")
        elif current_month == 6:
            if current_day == 29:
                await channel.send("Rent for July is due soon!")
        elif current_month == 7:
            if current_day == 30:
                await channel.send("Rent for August is due soon!")
        elif current_month == 8:
            if current_day == 30:
                await channel.send("Rent for September is due soon!")
        elif current_month == 9:
            if current_day == 29:
                await channel.send("Rent for October is due soon!")
        elif current_month == 10:
            if current_day == 30:
                await channel.send("Rent for November is due soon!")
        elif current_month == 11:
            if current_day == 29:
                await channel.send("Rent for December is due soon!")
        elif current_month == 12:
            if current_day == 30:
                await channel.send("Rent for January is due soon!")
 
#yes/no question answer
@client.command(aliases = ['yn'])
async def YesNo(ctx, *, question):
    responses = ['Yes','Perhaps', 'No', 'Probably not', "Can't say, try again later."]
    await ctx.send(random.choice(responses))

#yes/no question error
@YesNo.error
async def YNquestion_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        YNresponses =['Ask a question, dumbass',
                      'Awkward silence',
                      '???',
                      'Were you asking something?']
        await ctx.send(f'{random.choice(YNresponses)}')

#assign chore
chore_list = []
chore_dict = {}
@client.command(aliases = ['ac'])
async def assign_chores(ctx, *, chore_input):
    chore = chore_input
    if chore not in chore_list:
        chore_user = ctx.message.author.nick
        chore_dict.update({chore_input: chore_user})
        chore_list.append(chore_input)
        await ctx.send(f'"{chore_input}" has been added to the list of chores.')
    else:
        await ctx.send(f'That chore has already been added.')
    
#assign chore error
@assign_chores.error
async def assign_chore_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        ac_error_response = ["You're not trying to skip out on chores, are you?",
                             "Please enter a chore with the command.",
                             "Pssst, you're missing the chore you want to add"]
        await ctx.send(f'{random.choice(ac_error_response)}')
        
#remove chore
@client.command(aliases = ['rc'])
async def remove_chores(ctx, *, chore_input):
    chore = chore_input
    if chore in chore_list:
        chore_dict.pop(chore_input)
        await ctx.send(f'"{chore}" has been removed from the list of chores.')
    elif chore not in chore_list:
        await ctx.send(f'That chore has not been added to the list yet.')

#remove chore error
@remove_chores.error
async def remove_chore_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        rc_error_response = ["You're not trying to skip out- oh wait, wrong command.",
                             "Which chore are you trying to remove?",
                             "You have to enter a chore with that command amigo"]
        await ctx.send(f'{random.choice(rc_error_response)}')

#display chores
@client.command(aliases = ['chores'])
async def display_chores(ctx):
    if len(chore_dict) == 0:
        await ctx.send(f'There are no chores yet.')
    else:
        await ctx.send(f'Here are the chores that are currently listed.')
        chore_output = []
        for key, value in chore_dict.items():
            chore_output.append(f'{key} : {value}')
        await ctx.send("\n".join(chore_output))

#waifu image generator (work in progress)
@client.command(aliases = ['waifu', 'waifupic', 'wp'])
async def WaifuPicture(ctx):
    img_index = random.randint(0,44)
    waifu = open('waifu_pic_links.txt', 'r')
    lines = waifu.readlines()
    image = lines[img_index]
    await ctx.send(f"Here is a random image of an anime girl (or girls)")
    await ctx.send(image)


    

#invalid command error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('What is that command even supposed to do?')


    