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

def verifier_infos_confidentielles(client):
    # Vérifier les permissions des fichiers sensibles
    stdin, stdout, stderr = client.exec_command("ls -la /etc/shadow /etc/passwd /etc/sudoers 2>/dev/null")
    permissions = stdout.read().decode().strip()
    
    return permissions

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
    permissions = verifier_infos_confidentielles(client)
    print(f"Permissions des fichiers sensibles :\n{permissions}")

    statut = "CONFORME" if "shadow" in permissions else "A_REVOIR"
    detail = f"Permissions: {permissions[:100]}..."

    enregistrer_resultat("A.8.11", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
