#basic:
'''basic SpyAgent settings'''
Token = ""
history_size = 50 # default == 50
notification = False # default == False
allow_private_messages = True # default == True
display_users_avatars_urls = False # default == False it may break the display of messages if the user does not have his own avatar
allow_reference_display = False # default == False Displays replies to messages. It can greatly slow down the receipt of messages and message history
#event detector:
'''it serves to indicate that an event has occurred'''
detector = True # default == True
on_reaction_add = True # default == True it only works if it happened in the channel you selected
on_reaction_remove = True # default == True it only works if it happened in the channel you selected
on_message_delete = True  # default == True it only works if it happened in the channel you selected
on_message_edit = True # default == True it only works if it happened in the channel you selected
on_guild_remove = True # default == True