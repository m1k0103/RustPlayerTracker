import yaml
import requests
from bs4 import BeautifulSoup
import re

# Fetches the currently online players and returns an array
def getOnlinePlayers():
    r = requests.get(getBattlemetricsUrl())
    soup = BeautifulSoup(r.content, "html.parser")

    # finds the names of all players using a regex pattern on all anchor tags
    allPlayerNamesClassRegex = re.compile(r".*css-fj458c.*")
    allPlayerNames = [el.text for el in soup.find_all("a", {"class": allPlayerNamesClassRegex})]
    return allPlayerNames

# Returns the player names that are in the config
def getPlayersToWatch():
    with open("config.yml", "r", encoding="utf-8") as yml:
        data = yaml.safe_load(yml)
        players = [i[0] for i in data["players"]]
        return players

# Returns the battlemetrics url saved in the config
def getBattlemetricsUrl():
    with open("config.yml", "r", encoding="utf-8") as yml:
        url = yaml.safe_load(yml)["battlemetricsUrl"]
    return url

# Toggles if a user is shown as online or offline in the config 
def setOnlineInConfig(playerName, value):
    # Loads current config
    with open("config.yml", "r", encoding="utf-8") as yml:
        raw_data = yaml.safe_load(yml)
    # Finds the player in config, then sets their online status to the set value
    for p in raw_data["players"]:
        if p[0] == playerName:
            p[1] = value
        else:
            print(f"{playerName} not found in config.")
            break
    # Dumps the newly edited config
    with open("config.yml", "w", encoding="utf-8") as newYml:
        yaml.safe_dump(newYml)    
    return
    

# Gets the total amount of players that are online
def getTotalOnlineFromConfig():
    # Opens config, loads into variable
    with open("config.yml", "r", encoding="utf-8") as yml:
        data = yaml.safe_load(yml)
    # Goes through each player and adds 1 to the final count
    count = 0
    for p in data["players"]:
        if int(p[1]) == 1:
            count += 1
    return count


# Goes through the players that are being watched, and checks if they are online.
def initialPlayerCheck():
    to_watch = getPlayersToWatch()
    for p in to_watch:
        
        pass




# Sends message to a telegram channel
def sendTelegramNotification():
    pass
