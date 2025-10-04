import os
import time
import importlib

def credits_dep__menu(dependances, logo, version):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print("=== MENU CREDITS & DEPENDANCES ===")
        print("[1] - Afficher les credits et informations")
        print("[2] - Verifier les dependances")
        print("[3] - Quitter le sous-menu")
        print("======================\n")

        choix = input("Votre choix (1-3) : ")

        if choix == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print(logo)
            print("=== CREDITS ===")
            print("Developpe par : @Amynuv")
            print("Avec l'aide de :\n")
            print("@mercurylemc_")
            print("@ricozadsky\n")
            print(f"Version : {version}")
            print("================")
            input("\nAppuyez sur Entree pour revenir au menu...")

        elif choix == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print(logo)
            print("=== VERIFICATION DES DEPENDANCES ===")

            for module_name, package_name in dependances.items():
                try:
                    importlib.import_module(module_name)
                    print(f"[OK] {package_name} est installe.")
                except ImportError:
                    print(f"[MANQUANT] {package_name} n'est pas installe.")
            print("=================================")
            input("\nAppuyez sur Entree pour revenir au menu...")

        elif choix == "3":
            print("Fermeture du menu...")
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            return None

        else:
            print("Choix invalide, veuillez entrer 1, 2 ou 3.")
            time.sleep(1)


def show_settings(config,logo):
    os.system("cls" if os.name == "nt" else "clear")
    print(logo)
    print("=== CONFIGURATIONS ACTUELLES MENU ===")

    for conf_name, conf_state in config.items():
            print(f"- {conf_name} : {conf_state}")

    print("\n===============================")
    input("\nAppuyez sur Entrée pour revenir au menu...")



# Lancer le menu

