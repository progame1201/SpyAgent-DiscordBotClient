![GitHub all releases](https://img.shields.io/github/downloads/progame1201/SpyAgent-DiscordBot/total)

# SpyAgent-DiscordBotClient description
SpyAgent is a console application written in Python that is a client for the Discord bot.<br>
the program is designed for Windows OS<br>
I recommend using Windows Terminal: https://www.microsoft.com/store/productId/9N0DX20HK701?ocid=pdpshare
# How to use it?
To use this program, you need python, preferably version 3.12 or 3.11<br>
To install all the necessary modules download requirements.txt and enter the <br>`pip install -r  path/to/requirements.txt`<br>command in the console<br>
you have to go to the website: https://discord.com/developers/applications then create your own discord bot <br>
Next, turn on the switches under the Privileged Gateway Intents category located in the bot settings.
![screenshot](https://i.ibb.co/N2tdQBj/13213113.png)<br><br>
Next, generate your link and invite your bot to your server.<br>
Next, you need to get your bot's token and insert it into the config.<br>
Then select the server and channel and you can now use it.<br>
to find out all the commands and their functionality, you can type ***help<br>
<br>

# Command list
 You can open a window for entering commands by pressing F12 (**only in 2.0 version**) or by typing as a message. Example: ***help<br>
__All commands work with the prefix `***`__ *(by default)*<br>

### **Command list** <br>
+ help - help.
+ reset change the channel and guild<br>
+ file `<message>` - send file with message<br>
+ mute <guild aliases:`["g", "2", "guild"]`; channel aliases: `["ch", "c", "1", "channel"]`> - select a channel or guild for mute<br>
+ unmute <guild aliases:`["g", "2", "guild"]`; channel aliases: `["ch", "c", "1", "channel"]`> - remove the channel or guild from mute <br>
+ reaction `<mode: 1 - choose the emoji yourself; 2 - Select an emoji from the list of all emojis>` - Put a reaction under the message<br>
+ history `<channel id>` - Get the history of the channel you are on. Or from channel by id.<br>
+ delete - delete a message<br>
+ edit `<message>` - Edit the message<br>
+ set `<channel id>` - set the channel by id.<br>
+ reply `<message>` - reply to a message<br>
+ ~~vcplay - turns on music<br>~~
+ ~~vcstop - turns off the music<br>~~
+ ~~vcconnect - connect to any voice channel<br>~~
+ ~~vcdisconnect - disconnect from voice channel~~
+ ~~vctts - use tts in voice chat<br>~~
+ guildleave - choose a guild to exit it<br>
