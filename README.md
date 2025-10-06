# Discord Music Bot

A simple Discord music bot built with Python that plays audio from YouTube.

## Features

- 🎵 Play music from YouTube URLs
- 📋 Queue system for multiple songs
- ⏸️ Pause, resume, and skip functionality
- 🔄 Auto-leave when voice channel is empty
- 🔊 Volume control

## Commands

| Command | Description |
|---------|-------------|
| `!join` | Join your voice channel |
| `!leave` | Leave the voice channel |
| `!play <url>` | Play a song from YouTube |
| `!pause` | Pause current song |
| `!resume` | Resume paused song |
| `!skip` | Skip current song |
| `!stop` | Stop playing and clear queue |

## Setup

1. **Install required packages:**
   ```bash
   pip install discord.py yt-dlp

2.  Install FFmpeg:

-Windows: Download from FFmpeg website

-Linux: sudo apt install ffmpeg

-macOS: brew install ffmpeg

3. Configure the bot:

-Replace 'KEY_HERE' with your Discord bot token

-Ensure FFmpeg is in your system PATH

4. **Run the bot:**
   ```bash
   python bot.py

 
Requirements
-Python 3.7+

-FFmpeg

-discord.py

-yt-dlp

Note
Make sure your bot has the necessary permissions:

-Send Messages

-Connect to Voice Channels

-Speak in Voice Channels
