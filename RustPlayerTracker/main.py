from RustPlayerTracker.func import *
import time
import os

# sets the players that will be monitored

def main():
    
    playersToTrack = getPlayersToWatch()

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

        # Attempt to find friends of current targets that are also in the server.
        
        
        time.sleep(60)