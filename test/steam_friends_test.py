from RustPlayerTracker.func import checkIfPlayerOnServer
from bs4 import BeautifulSoup
import requests
import re


steamid = "76561198846204323"

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


print(potential_people)

