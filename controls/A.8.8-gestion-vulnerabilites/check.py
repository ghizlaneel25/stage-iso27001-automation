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

def verifier_vulnerabilites(client):
    stdin, stdout, stderr = client.exec_command("apt list --upgradable 2>/dev/null | wc -l")
    updates = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("systemctl is-active unattended-upgrades")
    auto_updates = stdout2.read().decode().strip()
    return updates, auto_updates

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
    updates, auto_updates = verifier_vulnerabilites(client)
    print(f"Mises à jour disponibles : {updates}")
    print(f"Automatic updates : {auto_updates}")
    statut = "CONFORME" if auto_updates == "active" else "A_REVOIR"
    detail = f"Updates: {updates}, Auto-updates: {auto_updates}"
    enregistrer_resultat("A.8.8", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
