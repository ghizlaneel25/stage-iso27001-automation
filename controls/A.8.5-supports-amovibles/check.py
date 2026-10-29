import paramiko
import sqlite3
from datetime import datetime

HOTE = "192.168.119.142"
UTILISATEUR = "ghiz"
CLE_PRIVEE = "/home/kali/.ssh/id_ed25519"

def se_connecter():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOTE, username=UTILISATEUR, key_filename=CLE_PRIVEE)
    return client

def verifier_supports(client):
    stdin, stdout, stderr = client.exec_command("lsmod | grep usb_storage || echo 'usb_storage non chargé'")
    usb = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("mount | grep -E '/media|/mnt' || echo 'Aucun média monté'")
    mounts = stdout2.read().decode().strip()
    return usb, mounts

def enregistrer_resultat(controle, statut, detail):
    conn = sqlite3.connect("db/conformite.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            controle TEXT,
            date_scan TEXT,
            statut TEXT,
            detail TEXT
        )
    """)
    cur.execute(
        "INSERT INTO resultats (controle, date_scan, statut, detail) VALUES (?, ?, ?, ?)",
        (controle, datetime.now().isoformat(), statut, detail)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    client = se_connecter()
    usb, mounts = verifier_supports(client)
    print(f"USB Storage : {usb}")
    print(f"Médias montés : {mounts}")

    statut = "CONFORME" if "usb_storage non chargé" in usb else "A_REVOIR"
    detail = f"USB: {usb}, Mounts: {mounts[:50]}"
    enregistrer_resultat("A.8.5", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
