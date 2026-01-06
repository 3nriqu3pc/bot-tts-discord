import discord
from discord.ext import commands
from gtts import gTTS
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CANAL_TEXTO_ID = 1455471945922641963
CANAL_VOZ_ID = 1456545015659495425

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CANAL_TEXTO_ID:
        return

    texto = message.content.strip()
    if not texto:
        return

    tts = gTTS(text=texto, lang="es")
    archivo = "tts.mp3"
    tts.save(archivo)

    canal_voz = bot.get_channel(CANAL_VOZ_ID)
    if not canal_voz:
        return

    if not message.guild.voice_client:
        vc = await canal_voz.connect()
    else:
        vc = message.guild.voice_client

    vc.play(
        discord.FFmpegPCMAudio(archivo),
        after=lambda e: os.remove(archivo)
    )

bot.run(os.getenv("DISCORD_TOKEN"))
