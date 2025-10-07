import pyautogui
import time
import os
import json
from PIL import Image
import io

base_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
config_path = os.path.join(project_root, "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

material_name_folder = "mineraietain"
DEBUG = config["DEBUG"]
tag_conf = config["tag_conf"]
normal_conf = config["normal_conf"]
time_to_collect = config["time_to_collect"]

# Échelles de recherche (réduit pour plus de rapidité)
SCALES = [0.8, 0.9, 1.0, 1.1, 1.2]


def redimensionner_image(image_path, scale):
    """Redimensionne une image selon une échelle donnée"""
    try:
        img = Image.open(image_path)
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        
        if new_width < 10 or new_height < 10:
            return None
            
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        return img_resized
    except Exception as e:
        if DEBUG:
            print(f"⚠️ Erreur redimensionnement: {e}")
        return None


def detecter_image_simple(image_path, confidence):
    """Détection simple sans multi-échelle"""
    try:
        pos = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        return pos
    except Exception:
        return None


def detecter_multi_echelle(image_path, confidence):
    """Détecte une image à différentes échelles"""
    # D'abord essayer l'échelle normale (plus rapide)
    pos = detecter_image_simple(image_path, confidence)
    if pos:
        return pos, 1.0
    
    # Si pas trouvé, essayer les autres échelles
    for scale in [0.9, 1.1, 0.8, 1.2]:  # Ordre optimisé
        try:
            img_resized = redimensionner_image(image_path, scale)
            if img_resized is None:
                continue
            
            pos = pyautogui.locateCenterOnScreen(img_resized, confidence=confidence)
            if pos:
                if DEBUG:
                    print(f"  📏 Détecté à échelle {scale}")
                return pos, scale
        except Exception:
            continue
    
    return None, None


def verif_tag(images_tag, confiance):
    """Vérification simple du tag"""
    for img in images_tag:
        # Essayer détection normale
        pos = detecter_image_simple(img, confiance)
        if pos:
            if DEBUG:
                print(f"  ✓ Tag trouvé: {os.path.basename(img)}")
            return True
        
        # Essayer avec échelles réduites
        for scale in [0.9, 1.1]:
            try:
                img_resized = redimensionner_image(img, scale)
                if img_resized:
                    pos = pyautogui.locateCenterOnScreen(img_resized, confidence=confiance)
                    if pos:
                        if DEBUG:
                            print(f"  ✓ Tag trouvé: {os.path.basename(img)} (échelle {scale})")
                        return True
            except Exception:
                continue
    
    return False


def detecter_material(material_name_folder, tag_max, image_max):
    """
    Détecte un minerai à l'écran avec support multi-échelle amélioré
    """
    base_dir = os.path.dirname(__file__)
    
    # Charger les images de détection
    images = [
        os.path.join(base_dir, "images", material_name_folder, "images", f"{i}.png")
        for i in range(1, image_max)
    ]
    images = [img for img in images if os.path.exists(img)]
    
    if not images:
        if DEBUG:
            print("⚠️ Aucun fichier image trouvé")
        return False
    
    # Charger les images de tags
    images_tag = [
        os.path.join(base_dir, "images", material_name_folder, "tags", f"{i}.png")
        for i in range(1, tag_max)
    ]
    images_tag = [img for img in images_tag if os.path.exists(img)]
    
    if not images_tag:
        if DEBUG:
            print("⚠️ Aucun fichier tag trouvé")
        return False
    
    if DEBUG:
        print(f"🔍 Recherche: {len(images)} images | {len(images_tag)} tags | conf={normal_conf}")
    
    # Recherche du minerai
    for img in images:
        if DEBUG:
            print(f"\n🔎 {os.path.basename(img)}...", end=" ")
        
        # Détection avec multi-échelle
        pos, scale = detecter_multi_echelle(img, normal_conf)
        
        if pos:
            if DEBUG:
                scale_txt = f"échelle {scale}" if scale != 1.0 else "échelle normale"
                print(f"✅ TROUVÉ à {pos} ({scale_txt})")
            
            # ÉTAPE 1: Déplacer le curseur sur la cible
            if DEBUG:
                print(f"  🖱️  Survol de la position...")
            
            pyautogui.moveTo(pos[0], pos[1], duration=0.2)
            time.sleep(0.8)  # Temps pour que le tag apparaisse
            
            # ÉTAPE 2: Première vérification du tag
            if DEBUG:
                print(f"  🏷️  Vérification tag (conf={tag_conf})...")
            
            if verif_tag(images_tag, tag_conf):
                if DEBUG:
                    print(f"  ✅ Tag validé ! Attente 1.5s...")
                
                time.sleep(1.5)
                
                # ÉTAPE 3: Deuxième vérification
                if DEBUG:
                    print(f"  🏷️  Double-vérification...")
                
                if verif_tag(images_tag, tag_conf):
                    if DEBUG:
                        print(f"  ✅✅ CONFIRMÉ ! Clic en cours...")
                    
                    # Clic sur la position
                    pyautogui.click(pos[0], pos[1])
                    
                    if DEBUG:
                        print(f"  🎯 CLIC effectué ! Attente {time_to_collect}s")
                    
                    time.sleep(time_to_collect)
                    return True
                else:
                    if DEBUG:
                        print(f"  ⚠️  Tag disparu (2ème vérif)")
            else:
                if DEBUG:
                    print(f"  ❌ Pas de tag détecté")
        else:
            if DEBUG:
                print("❌")
    
    if DEBUG:
        print("\n❌ Aucun minerai valide trouvé dans cette passe")
    return False


# Test avec confidence plus basse si besoin
def detecter_material_mode_agressif(material_name_folder, tag_max, image_max):
    """
    Mode avec détection plus permissive (à utiliser si le mode normal échoue)
    """
    global normal_conf, tag_conf
    
    # Sauvegarder les valeurs originales
    orig_normal = normal_conf
    orig_tag = tag_conf
    
    # Réduire les seuils de confiance
    normal_conf = max(0.6, normal_conf - 0.1)
    tag_conf = max(0.6, tag_conf - 0.1)
    
    if DEBUG:
        print(f"🔥 MODE AGRESSIF: conf_normale={normal_conf}, conf_tag={tag_conf}")
    
    result = detecter_material(material_name_folder, tag_max, image_max)
    
    # Restaurer les valeurs
    normal_conf = orig_normal
    tag_conf = orig_tag
    
    return result


# Exemple d'utilisation
if __name__ == "__main__":
    # Essayer détection normale
    succes = detecter_material(material_name_folder, tag_max=5, image_max=10)
    
    # Si échec, essayer mode agressif
    if not succes:
        print("\n" + "="*50)
        print("Tentative avec mode agressif...")
        print("="*50)
        detecter_material_mode_agressif(material_name_folder, tag_max=5, image_max=10)
