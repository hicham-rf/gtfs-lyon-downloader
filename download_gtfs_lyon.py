import requests
import hashlib
import os
from datetime import datetime

# --- Configuration ---
URL_GTFS = "https://download.data.grandlyon.com/files/rdata/tcl_sytral.tcltheorique/GTFS_TCL.ZIP"
USER = "hichambelafquih@gmail.com"       
PASSWORD = "BAB@Maths123"         
DOSSIER_GTFS = "gtfs_data"
FICHIER_HASH = "last_hash.txt"

# --- Création du dossier si besoin ---
os.makedirs(DOSSIER_GTFS, exist_ok=True)

# --- Téléchargement authentifié ---
print("Connexion au portail Grand Lyon...")
resp = requests.get(URL_GTFS, auth=(USER, PASSWORD))
if resp.status_code == 401:
    raise Exception("Erreur d'authentification : vérifie ton identifiant ou mot de passe.")
resp.raise_for_status()

data = resp.content

# --- Calcul du hash ---
new_hash = hashlib.md5(data).hexdigest()
old_hash = None
if os.path.exists(FICHIER_HASH):
    with open(FICHIER_HASH, "r") as f:
        old_hash = f.read().strip()

# --- Comparaison et sauvegarde ---
if new_hash != old_hash:
    print("✅ Nouveau GTFS détecté, sauvegarde en cours...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(DOSSIER_GTFS, f"gtfs_{date_str}.zip")

    with open(filename, "wb") as f:
        f.write(data)

    with open(FICHIER_HASH, "w") as f:
        f.write(new_hash)

    print(f"GTFS sauvegardé sous {filename}")
else:
    print("Aucun changement détecté, rien à faire.")
