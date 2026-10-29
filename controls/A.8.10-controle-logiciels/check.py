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

def verifier_logiciels(client):
    stdin, stdout, stderr = client.exec_command("dpkg -l | grep -E '(telnet|ftp|nmap|netcat)' || echo 'Aucun'")
    non_autorises = stdout.read().decode().strip()
    return non_autorises

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
    non_autorises = verifier_logiciels(client)
    print(f"Logiciels non autorisés : {non_autorises}")
    statut = "CONFORME" if non_autorises == "Aucun" else "A_REVOIR"
    detail = f"Non autorisés: {non_autorises}"
    enregistrer_resultat("A.8.10", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
