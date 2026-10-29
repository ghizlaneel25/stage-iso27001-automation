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

def verifier_reutilisation(client):
    stdin, stdout, stderr = client.exec_command("ls -la /tmp/ 2>/dev/null | wc -l")
    nb_tmp = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("df -h | grep -E '/dev/sd|/dev/vd' | awk '{print $1, $5}'")
    disques = stdout2.read().decode().strip()
    return nb_tmp, disques

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
    nb_tmp, disques = verifier_reutilisation(client)
    print(f"Fichiers dans /tmp : {nb_tmp}")
    print(f"Disques : {disques}")

    statut = "CONFORME" if int(nb_tmp) < 100 else "A_REVOIR"
    detail = f"tmp: {nb_tmp}, disques: {disques[:50]}"
    enregistrer_resultat("A.8.6", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
