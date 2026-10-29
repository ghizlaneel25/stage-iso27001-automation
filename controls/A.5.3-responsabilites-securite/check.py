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

def verifier_responsabilites(client):
    stdin, stdout, stderr = client.exec_command("getent group sudo | cut -d: -f4")
    admins = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("getent group admin 2>/dev/null | cut -d: -f4")
    admins2 = stdout2.read().decode().strip()
    return admins, admins2

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
    admins, admins2 = verifier_responsabilites(client)
    print(f"Administrateurs sudo : {admins}")
    print(f"Administrateurs admin : {admins2}")

    tous_admins = f"{admins},{admins2}".strip(",")
    statut = "CONFORME" if len(tous_admins) > 0 else "A_REVOIR"
    detail = f"Admins: {tous_admins}"
    enregistrer_resultat("A.5.3", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
