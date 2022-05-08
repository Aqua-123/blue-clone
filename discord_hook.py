
import asyncio
import discord

TOKEN = "OTY4NTYzOTU0NDMzNTQ4Mjk4.YmgreQ.iPeYzl0sYEvfEuZKq1or4LdPSJI"
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    return message.content

client.run(TOKEN)
client.on_message(on_message)

