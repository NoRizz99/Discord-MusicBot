import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Suppress noise about console usage from yt-dlp
youtube_dl.utils.bug_reports_message = lambda: ''

# Lightweight options for yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',  # Use best audio quality
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,  # Avoid downloading playlists
    'nocheckcertificate': True,  # Skip certificate verification
    'ignoreerrors': False,  # Do not ignore errors (for debugging)
    'quiet': True,  # Suppress unnecessary output
    'no_warnings': True,  # Suppress warnings
    'default_search': 'auto',  # Automatically handle search queries
    'source_address': '0.0.0.0',  # Bind to IPv4
    'cookiefile': 'cookies.txt',
}

# Lightweight FFmpeg options
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',  # No video, audio only
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Queue data structure
queues = {}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]  # Take first item from a playlist
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Command: Join the voice channel
@bot.command(name='join', help='Joins the voice channel')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f"{ctx.author.name} is not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

# Command: Leave the voice channel
@bot.command(name='leave', help='Leaves the voice channel')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# Command: Play music from YouTube
@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, *, url):
    if not ctx.voice_client:
        await ctx.invoke(join)  # Auto-join if not in a voice channel
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                # Add song to the queue
                if ctx.guild.id not in queues:
                    queues[ctx.guild.id] = []
                queues[ctx.guild.id].append(player)
                await ctx.send(f"Added to queue: {player.title}")
            else:
                ctx.voice_client.play(player, after=lambda e: play_next(ctx.guild.id, ctx))
                await ctx.send(f'Now playing: {player.title}')
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

# Command: Skip the current song
@bot.command(name='skip', help='Skips the current song')
async def skip(ctx):
    if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
        ctx.voice_client.stop()
        await ctx.send("Skipped the current song.")
        play_next(ctx.guild.id, ctx)  # Play the next song in the queue
    else:
        await ctx.send("No song is currently playing.")

# Command: Pause the current song
@bot.command(name='pause', help='Pauses the current song')
async def pause(ctx):
    if ctx.voice_client:
        ctx.voice_client.pause()

# Command: Resume the paused song
@bot.command(name='resume', help='Resumes the paused song')
async def resume(ctx):
    if ctx.voice_client:
        ctx.voice_client.resume()

# Command: Stop playing music
@bot.command(name='stop', help='Stops the current song')
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        queues[ctx.guild.id] = []  # Clear the queue
        await ctx.send("Stopped playing and cleared the queue.")

# Function to play the next song in the queue
def play_next(guild_id, ctx):
    if guild_id in queues and queues[guild_id]:
        player = queues[guild_id].pop(0)
        ctx.voice_client.play(player, after=lambda e: play_next(guild_id, ctx))
        asyncio.run_coroutine_threadsafe(ctx.send(f'Now playing: {player.title}'), bot.loop)
    else:
        asyncio.run_coroutine_threadsafe(ctx.send("No more songs in the queue."), bot.loop)

# Ensure the bot leaves the voice channel when it's not in use
@bot.event
async def on_voice_state_update(member, before, after):
    if not member.bot and after.channel is None:
        voice_client = member.guild.voice_client
        if voice_client and not voice_client.is_playing():
            await voice_client.disconnect()

# Run the bot
bot.run('KEY')
