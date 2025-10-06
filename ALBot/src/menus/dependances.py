import subprocess
import sys
def est_installe(module):
    """Teste l'import du module directement"""
    try:
        __import__(module)
        return True
    except ImportError:
        return False

def installer(package):
    """Installe un package pip"""
    print(f"Installation de {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def menu_dependances(DEPENDANCES):
    print("\n=== Verification des dépendances ===")
    manquants = [mod for mod, pkg in DEPENDANCES.items() if not est_installe(mod)]

    if not manquants:
        print("Toutes les dépendances sont déjà installées.")
        return

    print("Dependances manquantes :", ", ".join(manquants))
    choix = input("Voulez-vous les installer ? (o/n) : ").lower()

    if choix == "o":
        for mod in manquants:
            try:
                installer(DEPENDANCES[mod])
            except Exception as e:
                print(f"Erreur lors de l’installation de {mod} :", e)
        print("Installation terminee.")
    else:
        print("Installation annulée.")

        return

