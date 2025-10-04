import json
import os
import time

def config_menu(config, config_path, logo):
    """
    Menu interactif pour modifier les paramètres du bot.
    Args:
        config (dict): dictionnaire contenant la configuration actuelle.
        config_path (str): chemin vers le fichier config.json pour sauvegarde.
    """
    couleurs_disponibles = ["vert", "bleu", "rouge", "blanc", "jaune", "violet"]
    code_to_name = {
        "a": "vert",
        "b": "bleu",
        "c": "rouge",
        "7": "blanc",
        "6": "jaune",
        "5": "violet"
    }
    name_to_code = {v:k for k,v in code_to_name.items()}

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print("=== CONFIGURATION DU BOT ===")
        couleur_humaine = code_to_name.get(config.get('menu_color', 'a'), 'vert')
        print(f"[1] Couleur des menus: {couleur_humaine}")
        print(f"[2] Mode DEBUG : {config['DEBUG']}")
        print(f"[3] Taux de confiance TAG : {config['tag_conf']}")
        print(f"[4] Taux de confiance NORMAL : {config['normal_conf']}")
        print(f"[5] Temps d'attente collecte : {config['time_to_collect']}")
        print("[6] Quitter le sous-menu")
        print("==========================\n")

        choice = input("Choisissez un paramètre à modifier (1-6) : ")

        if choice == "1":
            while True:
                couleur = input(f"Entrez la couleur du menu ({', '.join(couleurs_disponibles)}) : ").lower()
                if couleur in couleurs_disponibles:
                    config["menu_color"] = name_to_code[couleur]
                    os.system(f"color {config["menu_color"]}")
                    break
                else:
                    print("Couleur invalide, réessayez.")

        elif choice == "2":
            while True:
                debug = input("Mode DEBUG (True/False) : ").strip().lower()
                if debug in ["true", "false"]:
                    config["DEBUG"] = debug == "true"
                    break
                else:
                    print("Entrée invalide, tapez True ou False.")

        elif choice == "3":
            while True:
                try:
                    tag_conf = float(input("Taux de confiance TAG (0.0 à 1.0) : "))
                    if 0.0 <= tag_conf <= 1.0:
                        config["tag_conf"] = tag_conf
                        break
                    else:
                        print("Doit être entre 0.0 et 1.0")
                except ValueError:
                    print("Entrée invalide, un nombre flottant est attendu.")

        elif choice == "4":
            while True:
                try:
                    normal_conf = float(input("Taux de confiance NORMAL (0.0 à 1.0) : "))
                    if 0.0 <= normal_conf <= 1.0:
                        config["normal_conf"] = normal_conf
                        break
                    else:
                        print("Doit être entre 0.0 et 1.0")
                except ValueError:
                    print("Entrée invalide, un nombre flottant est attendu.")

        elif choice == "5":
            while True:
                try:
                    ttc = int(input("Temps d'attente collecte (1 à 9999) : "))
                    if 1 <= ttc <= 9999:
                        config["time_to_collect"] = ttc
                        break
                    else:
                        print("Doit être entre 1 et 9999")
                except ValueError:
                    print("Entrée invalide, un entier est attendu.")

        elif choice == "6":
            # Sauvegarde automatique du config.json
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4)
                print("Configuration sauvegardée.")
            except Exception as e:
                print(f"Impossible de sauvegarder la configuration : {e}")

            print("Menu configuration quitté.")
            time.sleep(1)
            os.system("cls")
            break
        else:
            print("Choix invalide, entrez un nombre entre 1 et 6.")
            return None

        
