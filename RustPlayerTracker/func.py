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

# Check if an indivitual player is currently playing on the set server 
def checkIfPlayerOnServer(username):
    allPlayers = getOnlinePlayers()
    if username in allPlayers:
        return True
    else:
        return False
    pass

# Gets the bot token and channel ID used for sending messages to Telegram from the config file.
def getTGConfig():
    with open("config.yml") as cfg:
        contents = yaml.safe_load(cfg)
    return [contents["tgBotToken"], contents["tgChannelID"]]


# Sends message to a telegram channel
def sendTelegramNotification(message):
    creds = getTGConfig() # index0 = token, index1 = channelID
    data = {"chat_id":creds[1], "text":{message}}
    r = requests.post(f"https://api.telegram.org/bot{creds[0]}/sendMessage", data=data)
    if r.status_code == 200:
        print("Send message successfully.")
    else:
        print(r.status_code, r.text)

