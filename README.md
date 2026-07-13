![GitHub all releases](https://img.shields.io/github/downloads/progame1201/SpyAgent-DiscordBot/total)

# SpyAgent-DiscordBotClient description
SpyAgent is a console application written in Python that acts as a client for a Discord bot.<br>
The program is designed for Windows, but it can also run on Linux; however, I do not guarantee that it will work correctly there.<br>
If you're using Windows 10, I would like to recommend Windows Terminal: https://www.microsoft.com/store/productId/9N0DX20HK701?ocid=pdpshare

# How to use it?
To use this program, you need Python, preferably version 3.13 or lower.<br>
To install all the necessary modules, download `requirements.txt` and run the command `pip install -r path/to/requirements.txt` in the console.<br>
Go to the website: https://discord.com/developers/applications, then create your own Discord bot.<br>
Next, enable the switches under the **Privileged Gateway Intents** category located in the bot settings.<br>
![screenshot](https://i.ibb.co/N2tdQBj/13213113.png)<br><br>
Next, generate your link and invite your bot to your server.<br>
Then, get your bot's token and insert it into the config.<br>
After that, select the server and channel — you can now use the client.<br>
To see all commands and their functionality, type `***help`.

# Configuration
Copy `config.example.py`, rename it to `config.py` and fill in your bot token.

# Command list
*(only in SpyAgent 2.x.x) You can open a command input window by pressing F12 (default).*<br>
Use the prefix `***` before commands (default, can be changed in the config). Example: `***help`.<br>

+ help - display help.
+ reset - change the channel and guild<br>
+ file `<message>` - send a file with a message<br>
+ mute <guild aliases:`["g", "2", "guild"]`; channel aliases: `["ch", "c", "1", "channel"]`> - select a channel or guild to mute<br>
+ unmute <guild aliases:`["g", "2", "guild"]`; channel aliases: `["ch", "c", "1", "channel"]`> - remove the channel or guild from mute<br>
+ reaction `<mode: 1 - utf-8 emoji; 2 - select an emoji from the list of all emojis>` - add a reaction to a message<br>
+ history `<channel id>` - get the history of the current channel or a channel by ID<br>
+ delete - delete a message<br>
+ edit `<message>` - edit a message<br>
+ set `<channel id>` - set the channel by ID<br>
+ reply `<message>` - reply to a message<br>
+ vcplay - choose and play any file<br>
+ vcstop - stop playing a file<br>
+ vcconnect - connect to a voice channel<br>
+ vcdisconnect - disconnect from a voice channel<br>
+ ~~vctts - use TTS in voice chat<br>~~
+ guildleave - choose a guild to leave<br>
