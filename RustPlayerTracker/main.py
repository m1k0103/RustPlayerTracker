from RustPlayerTracker.func import *
import time
import os



def main():
    
    playersToTrack = getPlayersToWatch()

    # If not players in config.
    if playersToTrack == "":
        sid = input("Please enter a username into the config file, or enter a steamID here (type 'c' to cancel): ")
        if sid == "c":
            quit()
        name = resolveF7ID(sid)
        addPlayerToConfig(name)
        friends = getFriends(sid)
        for f in friends:
            addPlayerToConfig(f)
        print(f"All of {name}({sid}) friends added to config.")

       

    # main loop
    while True:
        os.system("cls")
        
        # finds the names of all players using a regex pattern on all anchor tags
        allPlayerNames = getOnlinePlayers()

        telegramMessageText = ""
        # Goes through each player in the list and checks if they are online
        # and then builds a message to be sent to the telegram webhook.
        for player in playersToTrack:
            if player in allPlayerNames:
                print(f"{player} is still in game.")
                telegramMessageText += f"{player} is in game.\n"
                setOnlineInConfig(player,1)
            else:
                print(f"{player} IS OFFLINE")
                telegramMessageText += f"{player} IS OFFLINE\n"
                setOnlineInConfig(player,0)

        print(f"Currently online: {getTotalOnlineFromConfig()}/{len(getPlayersToWatch())}")
        telegramMessageText += f"\nCurrently online: {getTotalOnlineFromConfig()}/{len(getPlayersToWatch())}"
        sendTelegramNotification(telegramMessageText)

        # Waits 5 minutes to avoid rate limits.
        # Can be adjusted.
        time.sleep(300)