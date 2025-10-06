version = 1.0


logo = f"""
      .o.       ooooo        oooooooooo.    .oooooo.   ooooooooooooo 
     .888.      `888'        `888'   `Y8b  d8P'  `Y8b  8'   888   `8 
    .8"888.      888          888     888 888      888      888      
   .8' `888.     888 v{version}     888oooo888' 888      888      888      
  .88ooo8888.    888          888    `88b 888      888      888      
 .8'     `888.   888       o  888    .88P `88b    d88'      888      
o88o     o8888o o888ooooood8 o888bood8P'   `Y8bood8P'      o888o     
                                                                 
"""
# Dépendances : { "module": "package pip" }
DEPENDANCES = {
    "pyautogui": "pyautogui",
    "PIL": "pillow"
    #"":""
}




import os
import importlib.util
import subprocess
import sys
from src.menus.dependances import menu_dependances
menu_dependances(DEPENDANCES)
from src.menus.menu_settings import config_menu
from src.menus.menu_credits_dependances import credits_dep__menu, show_settings
from src.menus.menu_farm import farm_menu
from src.start_bot import start_menu
import json


base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "config.json")
with open(config_path, "r+", encoding="utf-8") as f:
    config = json.load(f)

base_dir = os.path.dirname(__file__)
detection_config_path = os.path.join(base_dir, "detection_config.json")
with open(detection_config_path, "r+", encoding="utf-8") as f:
    detection_config = json.load(f)















max_opt = 4
def bot_menu(max_opt):
    os.system("cls" if os.name == "nt" else "clear")
    os.system(f"color {config["menu_color"]}")
    os.system("title ALBOT")
    print(logo)

    print("===== MENU PRINCIPAL =====")
    print("[1] - Parametres du BOT")
    print("[2] - Parametres de FARM")
    print("[3] - Credits & Dependances")
    print("[4] - LANCER LE BOT")
    print("==========================")
    print('\n')
    while True:
        choice = input("Entre ton choix : ")
        try:
            choice = int(choice)
            if 1 <= choice <= max_opt:
                break 
            else:
                print(f"Veuillez entrer un nombre entre 1 et {max_opt} !")
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier ! ")

    print(f"Vous avez choisi : {choice}")
    return choice



def enter_choice():

    choix = bot_menu(max_opt)
    if choix == 1:
        config_menu(config,config_path,logo)

    if choix == 2:
        farm_menu(detection_config, detection_config_path, logo)

    if choix == 3:
        credits_dep__menu(DEPENDANCES, logo, version)

    if choix==4:
        start_menu(detection_config, logo)
    else:
        return

















os.system("cls" if os.name == "nt" else "clear")
while True:
    enter_choice()
#bot_menu()



