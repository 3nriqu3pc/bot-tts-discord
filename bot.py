import os
import discord
from discord.ext import commands
from gtts import gTTS
import asyncio

# ========= CONFIGURACIÓN =========
PREFIX = "!"
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

# ========= EVENTOS =========
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ========= COMANDO TTS =========
@bot.command(name="tts")
async def tts(ctx, *, texto: str):
    # Verificar que el usuario esté en un canal de voz
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz.")
        return

    canal_voz = ctx.author.voice.channel

    # Conectarse al canal de voz
    if ctx.voice_client is None:
        vc = await canal_voz.connect()
    else:
        vc = ctx.voice_client

    # Crear audio TTS
    archivo = "tts.mp3"
    tts = gTTS(text=texto, lang="es")
    tts.save(archivo)

    # Esperar si ya está reproduciendo algo
    while vc.is_playing():
        await asyncio.sleep(0.5)

    # Reproducir audio (FFmpeg EXPLÍCITO)
    vc.play(
        discord.FFmpegPCMAudio(
            archivo,
            executable="ffmpeg",
            options="-loglevel panic"
        )
    )

    # Esperar a que termine
    while vc.is_playing():
        await asyncio.sleep(0.5)

    # Limpiar archivo
    try:
        os.remove(archivo)
    except:
        pass

# ========= INICIO =========
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("ERROR: DISCORD_TOKEN no está definido en Railway")

bot.run(TOKEN)
