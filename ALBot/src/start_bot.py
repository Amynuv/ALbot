import os
import time
import json
from .detection.detect_bot import detecter_material


def start_menu(config, logo):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print("=== MENU LANCEMENT ===")
        print("[1] Lancer un farm fini (durée en secondes)")
        print("[2] Lancer un farm infini")
        print("[3] Quitter le sous-menu")
        print("=================\n")

        choix = input("Votre choix (1-3) : ")

        # Vérification : au moins un minerai doit être actif
        actifs = [m for m, v in config.items() if v]
        if choix in ["1", "2"] and not actifs:
            print("\nERREUR : Aucun element active dans la configuration de farm !")
            print("Veuillez activer au moins un element avant de lancer le farm.\n")
            input("Appuyez sur Entree pour revenir au menu...")
            os.system("cls" if os.name == "nt" else "clear")

            return None  # <-- renvoie None si aucun minerai actif

        if choix == "1":
            try:
                duree = int(input("Entrez la durée du farm (en secondes) : "))
                if duree <= 0:
                    print("Entrez une valeur positive.")
                    time.sleep(1)
                    continue

                print(f"\nLancement d’un farm de {duree} secondes...\n")
                print("Veuillez mettre la fenetre Albion en plein ecran..\n")
                print("Le farm commencera dans 5 secondes...")
                time.sleep(5)  # <-- Pause de 5 secondes avant le lancement

                debut = time.time()

                while time.time() - debut < duree:
                    for minerai in actifs:
                        detecter_material(minerai,2,6)
                    time.sleep(0.1)  # pause entre cycles

                print("\nFarm termine !")
                input("\nAppuyez sur Entree pour revenir au menu...")

            except ValueError:
                print("Entrez un nombre entier valide.")
                time.sleep(1)


        elif choix == "2":
            print("\nLancement d’un farm infini... Appuyez sur Ctrl + C pour arrêter.\n")
            print("Veuillez mettre la fenetre Albion en plein ecran..\n")
            print("Le farm commencera dans 5 secondes...")
            time.sleep(5)  # <-- Pause de 5 secondes avant le lancement

            try:
                while True:
                    for minerai in actifs:
                        detecter_material(minerai,2,6)
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nFarm infini interrompu par l’utilisateur.")
                input("\nAppuyez sur Entree pour revenir au menu...")


        elif choix == "3":
            print("Fermeture du menu de farm...")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            break

        else:
            print("Choix invalide, entrez 1, 2 ou 3.")
            time.sleep(1)