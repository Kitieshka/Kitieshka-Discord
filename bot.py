import discord
from discord.ext import commands
import json

bot=commands.Bot(command_prefix="!", intents=discord.Intents.all()) # создание клиента Discord
with open('data.json') as f:
    data=json.loads(f.read())

@bot.event
async def on_message(msg:discord.Message):
    global data
    if msg.author.bot:return
    await bot.process_commands(msg)
    if msg.channel.id == data[0]:
        channel=bot.get_channel(data[0])
        msgd=await channel.fetch_message(data[1])
        await msgd.delete()
        msg_id=await channel.send('hi')
        data=[msg.channel.id, msg_id.id]
        with open('data.json', 'w') as f:
            f.write(json.dumps([msg.channel.id, msg_id.id]))
@bot.command(name='start')
@commands.has_permissions(administrator=True)
async def start(ctx):
    global data
    print('changed data')
    with open('data.json', 'w') as f:
        msg_id=await ctx.send('hi')
        f.write(json.dumps([ctx.message.channel.id, msg_id.id]))
    data=[ctx.channel.id, msg_id.id]

# Создание команды embed, которая позволяет отправлять эмбеды в чат
@bot.command(name='embed')
@commands.has_permissions(administrator=True)
async def send_embed(ctx, *, json_string: str):
    print(json_string)
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        await ctx.send(f"Error parsing JSON: {e}")
        return

    if '"embeds": [' in json_string:
        for a in data['embeds']:
            embed = discord.Embed.from_dict(a)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed.from_dict(data)
        await ctx.send(embed=embed)

bot.run('')