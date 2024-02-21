![GitHub all releases](https://img.shields.io/github/downloads/progame1201/SpyAgent-DiscordBot/total)

# SpyAgent-DiscordBot description
a bot that allows you to track messages on connected servers and also send messages to selected channels on behalf of the bot<br>
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
__All commands work with the prefix ***<br>__

### **In the mode of communication on servers:** <br>
+ reset - Gives you the opportunity to re-select the channel and server <br>
+ file - Allows you to send any file <br>
+ mute - Allows you to select a channel for mute<br>
+ unmute - Allows you to remove the channel from mute <br>
+ reaction - Put a reaction under the message<br>
+ muteguild - Mute server<br>
+ unmuteguild - Unmute server<br>
+ status - Changes your status to the one you specified<br>
+ gethistory - Get the history of the channel you are on<br>
+ delete - delete a message<br>
+ privatemsg - Send a private message to the user<br>
+ edit - Edit the message<br>
+ into - send a message to any channel (by ID)<br>
+ set - set the channel (by ID)
+ setuser - It works as a SpyAgentPM setting the user as a channel<br>
+ reply - reply to a message<br>
+ vcplay - turns on music<br>
+ vcstop - turns off the music<br>
+ vcconnect - connect to any voice channel<br>
+ vcdisconnect - disconnect from voice channel
+ vctts - use tts in voice chat<br>
+ guildleave - allows you to exit the guild you are in<br>

### **commands in private messages:** work in SpyAgentPM<br>

+ reset - Gives you the opportunity to re-select the channel and server <br>
+ file - Allows you to send any file <br>
+ reaction - Put a reaction under the message<br>
+ status - Changes your status to the one you specified<br>
+ gethistory - Get the history of the channel you are on<br>
+ delete - delete a message<br>
+ edit - Edit the message
