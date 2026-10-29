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

def verifier_crypto_renforce(client):
    stdin, stdout, stderr = client.exec_command("grep -E 'Ciphers|MACs|KexAlgorithms' /etc/ssh/sshd_config 2>/dev/null | grep -v '#'")
    config = stdout.read().decode().strip()
    return config

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
    config = verifier_crypto_renforce(client)
    print(f"Configuration SSH crypto :\n{config}")

    statut = "CONFORME" if config else "A_REVOIR"
    detail = f"Crypto config: {config[:100]}..."
    enregistrer_resultat("A.8.14", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
