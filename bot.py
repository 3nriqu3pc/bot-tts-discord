import os
import discord
from discord.ext import commands
from gtts import gTTS
import asyncio
import shutil

# ========= CONFIG =========
PREFIX = "!"
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

# ========= READY =========
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ========= TTS =========
@bot.command(name="tts")
async def tts(ctx, *, texto: str):
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz.")
        return

    canal_voz = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await canal_voz.connect()
    else:
        vc = ctx.voice_client

    archivo = "tts.mp3"
    gTTS(text=texto, lang="es").save(archivo)

    # 🔑 RUTA REAL DE FFMPEG (CLAVE)
    ffmpeg_path = shutil.which("ffmpeg")

    if not ffmpeg_path:
        await ctx.send("❌ FFmpeg no encontrado en el sistema.")
        return

    while vc.is_playing():
        await asyncio.sleep(0.5)

    vc.play(
        discord.FFmpegPCMAudio(
            archivo,
            executable=ffmpeg_path,
            options="-loglevel panic"
        )
    )

    while vc.is_playing():
        await asyncio.sleep(0.5)

    try:
        os.remove(archivo)
    except:
        pass

# ========= START =========
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("ERROR: DISCORD_TOKEN no está definido en Railway")

bot.run(TOKEN)
