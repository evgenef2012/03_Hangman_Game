import random
import json
import pprint
from colorama import init

# Initialize colorama to enable ANSI escape sequences on Windows
init()
# Word bank
words = [
    # General IT Terms
    "algorithm",
    "api",
    "bandwidth",
    "bit",
    "byte",
    "cache",
    "cloud computing",
    "compression",
    "data",
    "database",
    "debugging",
    "encryption",
    "firewall",
    "firmware",
    "gigabyte",
    "http",
    "ip address",
    "kernel",
    "latency",
    "load balancing",
    "malware",
    "network",
    "packet",
    "protocol",
    "proxy",
    "router",
    "server",
    "software",
    "terabyte",
    "url",
    "user interface",
    "virtual machine",
    "vpn",
    "wan",
    
    # Programming and Development
    "agile",
    "branch",
    "bug",
    "class",
    "compiler",
    "framework",
    "function",
    "git",
    "javascript",
    "library",
    "loop",
    "method",
    "repository",
    "script",
    "sprint",
    "syntax",
    "testing",
    "version control",
    "web development",

    # Security
    "authentication",
    "authorization",
    "backdoor",
    "botnet",
    "brute force attack",
    "cryptography",
    "cybersecurity",
    "exploit",
    "hacker",
    "intrusion detection system",
    "keylogger",
    "phishing",
    "ransomware",
    "social engineering",
    "spyware",
    "trojan",
    "virus",
    
    # Data and Analytics
    "big data",
    "business intelligence",
    "data mining",
    "data warehouse",
    "machine learning",
    "predictive analytics",
    "statistics",

    # Networking
    "ethernet",
    "gateway",
    "local area network",
    "mac address",
    
    # Cloud and Virtualization
    "azure",
    "docker",
    "hypervisor",
    "kubernetes",
    "serverless computing",

    # Hardware
    "cpu",
    "gpu",
    "hard drive",
    "motherboard",
    "random access memory",
    "solid state drive",
    "peripheral",
    "power supply unit"
]
 
# Text formatting variables
bold = "\033[1m"
red = "\033[31m"
yellow = "\033[33m"
blue = "\033[94m"
green = "\033[32m"
reset = "\033[0m"   
    
def welcome():
  
    print(f"""
{bold}{yellow}Welcome to the Hangman Game!{reset}
\n{blue}You will be tested with terminology from the IT sphere.
Try to guess a letter or the entire word.{reset}
\n{bold}{green}Good Luck!{reset}
        """)    

def players():
    
    print(f"{bold}How many players will play?{reset}\nYou may choose {bold}1-5{reset} players!")
    while True:
        try:
            no_of_players = int(input(f"\nEnter number of players ({bold}1-5{reset}): "))
            if 1 <= no_of_players <= 5:
                return no_of_players
            else:
                print(f"{bold}{red}Please enter a number between 1-5!{reset}")    
        except ValueError:
            print(f"{bold}{red}Invalid input, Please enter a number between 1-5!{reset}")

def create_player(no_of_try):
    
    no_of_players = players()
    no_of_try = no_of_try
    title_list = []
    player_list = []
    game_players = {}
    
    for player in range(int(no_of_players)):
        title = "player" + "_" + str(player + 1)
        title_list.append(title)
        
    for title in title_list:
        player = str(input(f"\n{bold}{green}{title.capitalize()}{reset} {bold}please enter your name: {reset}").lower())
        player_list.append(player)
    
    for title in range(len(title_list)):
        key = title_list[title]
        value = dict(name = player_list[title], p_try = no_of_try, turn = True, score = 0)
        game_players[key] = value
        
    with open("players.json", "w") as file:
        json.dump(game_players, file, indent=4)
        
    return game_players    
    
def save_game_players (game_players, file):
    with open(file, "w") as file:
        json.dump(game_players, file, indent=4)
    
def load_game_players (file):
    with open(file, "r") as file:
        game_players = json.load(file)
    return game_players

def make_secret_word (words):
    
    secret_word = random.choice(words)
    display_word = []
    for letter in secret_word:
        if letter == " ":
            display_word += " "
        else:
            display_word += "_"
    return secret_word, display_word       

def answer (secret_word, display_word):
    
    answer_check = False
    win = False
    counter = 0
    score = 0
    letter_score = 10
    guess_score = 100
    
    print(f"\n{bold}{yellow}{" ".join(display_word).upper()}{reset}")
    u_answer = input(f"\n{blue}Please enter a letter or guess the entire word.{reset}\n{bold}{green}Enter letter/word:{reset}\n").lower()
    
    for position, letter in enumerate(secret_word):
        if display_word[position] == u_answer:
            answer_check = False
        elif u_answer == letter:
            display_word[position] = letter 
            answer_check = True
            counter = int(secret_word.count(letter))
            
    if answer_check:
        score = score + counter * letter_score
                
    if "".join(display_word).lower() == str(secret_word).lower():
        win = True
        score = score + guess_score
    elif u_answer.lower() == secret_word.lower():
        win = True
        score = score + guess_score
        
    return answer_check, win, score
                
def player_turn (game_players, secret_word, display_word):
    # print("".join(display_word), secret_word)
    for player, details in game_players.items():
        while details["turn"]==True:
            
            print(f"\n{bold}{details["name"].capitalize()}`s turn!{reset}")
            print(f"\n{bold}{details["name"].capitalize()}`s score: {details["score"]}{reset}")
            print(f"{bold}Tries left: {details["p_try"]}{reset}")
            player_answer, win, score = answer(secret_word, display_word)
            
            if win == True:
                details["turn"]=False
                details["score"] = details["score"] + score
                print(f"\n{bold}{green}You did it {details["name"].capitalize()}!\nYou won!{reset}\n\nYou guessed: {reset}{yellow}{" ".join(secret_word).upper()}{reset}")
                # print(f"\n{bold}{green}You won!{reset}")
                # print(f"{bold}{details["name"].capitalize()}`s score: {reset}{details["score"]}")
            elif player_answer == True:
                details["turn"]=True
                details["p_try"] = details["p_try"]
                details["score"] = details["score"] + score
                print(f"{details["name"]}`s score: {details["score"]}")
            else:
                details["turn"]=False
                details["p_try"] = details["p_try"] - 1
                print(f"{bold}{red}Incorrect answer!{reset}")
            
            if details["p_try"] == 0:
                print(f"{bold}{red}Game Over {details["name"].capitalize()}!{reset}")
            
            if details["turn"]==False:
                continue
                
        for player, details in game_players.items():
            if win == True:
                details["turn"]=False
            elif details["p_try"] > 0:
                details["turn"]=True
            else:
                details["turn"]=False
                
    return game_players, win
                
def game (game_players, secret_word, display_word):
    players_lose = False
    game_on = True
    while game_on == True:
        game_players, win = player_turn(game_players, secret_word, display_word)
        
        if win == True:
            game_on = False
            for player, data in game_players.items():
                print(f"\n{bold}{blue}{data["name"].capitalize()} score: {data["score"]}{reset}")
                
        for player, data in game_players.items():
            if data["p_try"] <= 0 :
                players_lose = True
                game_on = False
                print(f"\n{bold}{blue}{data["name"].capitalize()} score: {data["score"]}{reset}")
                
        if win == False and players_lose == True:
            print(f"\n{bold}Game over!\nThe word was: {reset}{yellow}{" ".join(secret_word).upper()}{reset}")        
                    
    return game_players
        
def reset_game (game_players, file):
    print(f"""
{green}Would you like to play another round?
(Press the corresponding number!){reset}{bold}
1. Yes
2. No      
{reset}    """)
    
    while True:
        try:
            round = int(input(f"{bold}Youre choise: {reset}"))
            if round == 1:
                round = True
                for player, data in game_players.items():
                    data["turn"] = True
                    data["p_try"] = 5
                save_game_players(game_players, file)
                return round
            elif round == 2:
                round = False
                print(f"{green}{bold}Goodbye, See you next time!{reset}")
                exit()
            else:
                print(f"{bold}{red}Press the corresponding number!{reset}")
        except ValueError:
            print(f"{bold}{red}Invalid input, Press the corresponding number!{reset}")
               

# Game Welcome
welcome()   
# Define number of players and create players
create_player(5)
# Load the players file and start a round
while round:   
    game_players = load_game_players("players.json")
# Chose the secret word
    secret_word, display_word = make_secret_word(words)
# The game
    game_players = game(game_players, secret_word, display_word)   
# Ask if the players want to play another round keeping the score
    round = reset_game(game_players, "players.json")        
    
        
    
            


            


    
   
    

    
    
    
    
    
    

    
    
    
    
