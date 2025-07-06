from RustPlayerTracker.main import main
import os


# The starting script that runs before running the main code.
# It ensures the config exists
def start():
    if "config.yml" not in os.listdir():
        with open("config.yml", "w+") as cfg:
            cfg.write("""#FORMAT:
# ["player name" , online?] 
players: [
  ["", 0]
]
battlemetricsUrl: ""

#Telegram Info
tgBotToken: a
tgChannelID: 1""")
        print("Please enter information into the config.\nREQUIRED:\n - At least one player\n - Battlemetrics URL.\n - Telegram bot token\n - Telegram channel ID")
        quit()

    # Runs actual program
    main()