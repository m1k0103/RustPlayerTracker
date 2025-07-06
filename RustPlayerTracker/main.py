from RustPlayerTracker.func import *
from bs4 import BeautifulSoup 
import requests
import time
import re
import yaml
import os

# sets the players that will be monitored

def main():
    
    playersToTrack = getPlayersToWatch()

    # main loop
    while True:
        os.system("cls")
        # finds the names of all players using a regex pattern on all anchor tags
        allPlayerNames = getOnlinePlayers()

        #goes through each player in the list and checks if they are online
        for player in playersToTrack:
            if player in allPlayerNames:
                print(f"{player} is still in game.")
                setOnlineInConfig(player,1)
            else:
                print(f"{player} IS OFFLINE")
                setOnlineInConfig(player,0)

        print(f"Currently online: {getTotalOnlineFromConfig()}/{len(getPlayersToWatch())}")
        time.sleep(60)