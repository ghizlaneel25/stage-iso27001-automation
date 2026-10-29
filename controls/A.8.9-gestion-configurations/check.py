import paramiko
import sqlite3
import re
from datetime import datetime

HOTE = "192.168.119.142"
UTILISATEUR = "ghiz"
CLE_PRIVEE = "/home/kali/.ssh/id_ed25519"

def se_connecter():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOTE, username=UTILISATEUR, key_filename=CLE_PRIVEE)
    return client

def extraire_score_openscap(client):
    # Lire le rapport HTML et extraire le score
    stdin, stdout, stderr = client.exec_command("grep -oP 'Score.*?([0-9.]+)%' ~/scan_openscap_report.html | head -1")
    resultat = stdout.read().decode().strip()
    if resultat:
        score = re.findall(r"([0-9.]+)%", resultat)
        return score[0] if score else "Non trouvé"
    return "Rapport non trouvé"

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
    score = extraire_score_openscap(client)
    print(f"Score OpenSCAP : {score}")

    statut = "CONFORME" if score and float(score) >= 70 else "A_REVOIR"

    enregistrer_resultat("A.8.9", statut, f"Score OpenSCAP: {score}")
    print(f"Résultat enregistré : {statut}")
    client.close()
