import discord
from discord.ext import commands
import json
#Telegram @harmfulCat05

bot=commands.Bot(command_prefix="!", intents=discord.Intents.all()) # создание клиента Discord

# Создание команды embed, которая позволяет отправлять эмбеды в чат
@bot.command(name='embed')
@commands.has_permissions(administrator=True)
async def send_embed(ctx, *, json_string: str):
    await ctx.message.delete()
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

bot.run('token')