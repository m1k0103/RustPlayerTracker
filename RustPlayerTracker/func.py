#import yaml
import requests
from bs4 import BeautifulSoup
import re
from ruamel.yaml import YAML

# Sets the YAML object to be global, so it doesnt need to be redeclared with each function that uses it.
# Might be a bit inefficient but oh well, it works and its 1am.
global yaml
yaml = YAML()
yaml.preserve_quotes = True  # Optional, keeps quotes
yaml.indent(mapping=2, sequence=4, offset=2)



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
        data = yaml.load(yml)
        players = [i[0] for i in data["players"]]
        return players

# Returns the battlemetrics url saved in the config
def getBattlemetricsUrl():
    with open("config.yml", "r", encoding="utf-8") as yml:
        url = yaml.load(yml)["battlemetricsUrl"]
    return url

# Toggles if a user is shown as online or offline in the config 
def setOnlineInConfig(playerName, value):
    # Loads current config
    with open("config.yml", "r", encoding="utf-8") as yml:
        raw_data = yaml.load(yml)
    # Finds the player in config, then sets their online status to the set value
    for p in raw_data["players"]:
        if p[0] == playerName:
            p[1] = value
            break
            
    # Dumps the newly edited config
    with open("config.yml", "w", encoding="utf-8") as newYml:
        yaml.dump(raw_data, newYml)    
    return
    

# Gets the total amount of players that are online
def getTotalOnlineFromConfig():
    # Opens config, loads into variable
    with open("config.yml", "r", encoding="utf-8") as yml:
        data = yaml.load(yml)
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
        contents = yaml.load(cfg)

    # If the values in the config are empty
    if (contents["tgBotToken"] == "") and (contents["tgChannelID"] == ""):
        return False

    return [contents["tgBotToken"], contents["tgChannelID"]]


# Sends message to a telegram channel
def sendTelegramNotification(message):
    creds = getTGConfig() # index0 = token, index1 = channelID
    if creds == False: # this means there are no tg creds, so message isnt sent.
        return
    data = {"chat_id":creds[1], "text":{message}}
    r = requests.post(f"https://api.telegram.org/bot{creds[0]}/sendMessage", data=data)
    if r.status_code == 200:
        print("Send message successfully.")
    else:
        print(r.status_code, r.text)

# Gets the steam friends of a user's steamID that can be found in Rust's F7 report menu.
def getFriends(steamid):
    soup = BeautifulSoup(
        requests.get(f"https://steamcommunity.com/profiles/{steamid}/friends/").text,
        "html.parser"
        )

    friendsregex = re.compile(r".*selectable friend_block_v2 persona in-game")
    all_friends = soup.find_all("div", {"class":friendsregex})
    potential_people = []
    for f in all_friends:
        f_soup = BeautifulSoup(str(f), "html.parser")
        name = f_soup.find("div", {"class":"friend_block_content"}).text.split("\n")[0]
        current_game = f_soup.find("span", {"class":"friend_game_link"}).text
        if current_game == "Rust":
            potential_people.append([name,checkIfPlayerOnServer(name)])
    
    return potential_people