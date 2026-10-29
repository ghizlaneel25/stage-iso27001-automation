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

def verifier_comptes_sudo(client):
    stdin, stdout, stderr = client.exec_command("getent group sudo | cut -d: -f4")
    membres = stdout.read().decode().strip()
    return membres

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
    membres_sudo = verifier_comptes_sudo(client)
    print(f"Comptes avec droits sudo : {membres_sudo}")

    nb_comptes = len(membres_sudo.split(",")) if membres_sudo else 0
    statut = "CONFORME" if nb_comptes <= 2 else "A_REVOIR"

    enregistrer_resultat("A.8.2", statut, f"{nb_comptes} comptes sudo: {membres_sudo}")
    print(f"Résultat enregistré : {statut}")
    client.close()
