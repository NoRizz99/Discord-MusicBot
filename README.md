Discord Music Bot
A simple Discord music bot built with Python that plays audio from YouTube.

Features
🎵 Play music from YouTube URLs

📋 Queue system for multiple songs

⏸️ Pause, resume, and skip functionality

🔄 Auto-leave when voice channel is empty

🔊 Volume control

Commands
!join - Join your voice channel

!leave - Leave the voice channel

!play <url> - Play a song from YouTube

!pause - Pause current song

!resume - Resume paused song

!skip - Skip current song

!stop - Stop playing and clear queue

Setup
Install required packages:

bash
pip install discord.py yt-dlp
Replace 'KEY_HERE' with your Discord bot token

Run the bot:

bash
python bot.py
Requirements
Python 3.7+

FFmpeg installed on your system

Discord bot token

Required Python packages (see above)

Note: Make sure FFmpeg is installed and accessible in your system PATH for audio playback to work properly.
