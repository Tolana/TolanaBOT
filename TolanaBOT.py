import disnake
from tokens import tokens

BOT_TOKEN = tokens['bot_token']
ints = disnake.Intents.default()
ints.message_content = True
client = disnake.Client(intents=ints)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(BOT_TOKEN)