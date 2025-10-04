import pyautogui
import time
import os
import random
import json


base_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(base_dir, "..",".."))
config_path = os.path.join(project_root, "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)


material_name_folder = "mineraietain"

DEBUG = config["DEBUG"]
tag_conf = config["tag_conf"]
normal_conf = config["normal_conf"]
time_to_collect = config["time_to_collect"]


def detecter_material(material_name_folder,tag_max,image_max):
    """
    Détecte un minerai à l'écran et interagit automatiquement :
    - Déplace le curseur et clique si trouvé
    - Déplace le curseur aléatoirement si rien trouvé
    - 1 fois sur 10 : clic droit en haut de l’écran
    """

    # ------------------------
    # Config des images
    # ------------------------
    base_dir = os.path.dirname(__file__)

    # Images pour la détection
    images = [
        os.path.join(base_dir, "images", material_name_folder, "images", f"{i}.png")
        for i in range(1, image_max)
    ]
    images = [img for img in images if os.path.exists(img)]
    if not images:
        if DEBUG:
            print("⚠️ Aucun fichier image trouvé")
        return

    # Images pour vérification TAG
    images_tag = [
        os.path.join(base_dir, "images", material_name_folder, "tags", f"{i}.png")
        for i in range(1, tag_max)
    ]
    images_tag = [img for img in images_tag if os.path.exists(img)]
    if not images_tag:
        if DEBUG:

            print("⚠️ Aucun fichier tag trouvé")
        return

    # ------------------------
    # Fonction de vérification
    # ------------------------
    def verif_tag(confiance=tag_conf, majorite=False):
        detections = 0
        for img in images_tag:
            try:
                pos = pyautogui.locateCenterOnScreen(img, confidence=confiance)
                if pos:
                    detections += 1
            except pyautogui.ImageNotFoundException:
                pass

        if majorite:
            return detections >= (len(images_tag) // 2 + 1)
        else:
            return detections > 0

    # ------------------------
    # Logique principale
    # ------------------------
    pos_trouvee = None

    for img in images:
        try:
            pos = pyautogui.locateCenterOnScreen(img, confidence=normal_conf)
            if pos:
                pos_trouvee = pos
                if DEBUG:

                    print(f"✅ Trouvé avec {os.path.basename(img)} à {pos}")
                break
        except pyautogui.ImageNotFoundException:
            pass

    # Rien trouvé → déplacement aléatoire
    if not pos_trouvee:
        if DEBUG:

            print("❌ Non trouvé")
        screen_width, screen_height = pyautogui.size()
        rand_x = random.randint(0, screen_width - 1)
        rand_y = random.randint(0, screen_height - 1)
        pyautogui.moveTo(rand_x, rand_y, duration=0.2)
        if DEBUG:

            print(f"🎲 Curseur déplacé aléatoirement à ({rand_x}, {rand_y})")

        # 1 fois sur 10 → clic droit en haut
        if random.randint(1, 10) == 1:
            pyautogui.moveTo(screen_width // 2, 10, duration=0.2)
            pyautogui.click(button="right")
            if DEBUG:

                print("🖱️ Clic droit en haut de l’écran (aléatoire)")

        time.sleep(1)
        return

    # Si trouvé → vérifier avant clic
    pyautogui.moveTo(pos_trouvee)
    if DEBUG:

        print(f"🎯 Curseur déplacé à {pos_trouvee}")
    time.sleep(0.2)

    if verif_tag(confiance=tag_conf, majorite=False):
        time.sleep(2)
        if verif_tag(confiance=tag_conf, majorite=False):
            pyautogui.click()
            if DEBUG:

                print("🖱️ Clic gauche effectué (pierre validée)")
            time.sleep(time_to_collect)
    else:
        #print("⚠️ Faux positif, aucun clic")
        time.sleep(1)

    # 1 fois sur 10 même si trouvé
    if random.randint(1, 10) == 1:
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, 10, duration=0.2)
        pyautogui.click(button="right")
        if DEBUG:

            print("🖱️ Clic droit en haut de l’écran (1/10 proba)")
