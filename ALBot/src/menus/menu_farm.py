import json
import os
import time

def farm_menu(config, config_path, logo):
    """
    Menu interactif pour activer ou desactiver les minerais.
    Args:
        config (dict): Dictionnaire contenant les minerais actives/desactives.
        config_path (str): Chemin vers le fichier JSON a sauvegarder.
        logo (str): ASCII logo a afficher.
    """

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print("=== CONFIGURATION DE FARM ===\n")

        # Afficher les états actuels (Oui / Non)
        for i, (minerai, actif) in enumerate(config.items(), start=1):
            etat = "Oui" if actif else "Non"
            print(f"[{i}] {minerai.replace('_', ' ').capitalize()} : {etat}")

        print(f"[{len(config)+1}] Sauvegarder et quitter le sous-menu")
        print("===============================\n")

        choix = input(f"Choisissez un element a modifier (1-{len(config)+1}) : ")

        # Vérifie si c’est un nombre
        if not choix.isdigit():
            print("Entree invalide, entrez un nombre.")
            time.sleep(1)
            continue

        choix = int(choix)

        # Si l'utilisateur veut quitter
        if choix == len(config) + 1:
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                print("\nConfiguration sauvegardee avec succes.")
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {e}")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            break

        # Si le choix correspond à un minerai
        elif 1 <= choix <= len(config):
            minerai = list(config.keys())[choix - 1]
            os.system("cls" if os.name == "nt" else "clear")
            print(logo)
            print(f"=== MODIFIER : {minerai.replace('_', ' ').capitalize()} ===")
            print("Souhaitez-vous activer ce minerai ? (o/n)\n")
            reponse = input("Votre choix : ").strip().lower()

            if reponse in ["o", "oui"]:
                config[minerai] = True
            elif reponse in ["n", "non"]:
                config[minerai] = False
            else:
                print("Reponse invalide, entrez 'o' ou 'n'.")
                time.sleep(1)
        else:
            print("Choix invalide.")
            time.sleep(1)