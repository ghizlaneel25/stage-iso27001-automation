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

def verifier_identifiants(client):
    stdin, stdout, stderr = client.exec_command("grep -E 'PASS_MAX_DAYS|PASS_MIN_DAYS' /etc/login.defs | grep -v '#'")
    policy = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("chage -l ghiz 2>/dev/null | grep -E 'Last|Expires'")
    user_status = stdout2.read().decode().strip()
    return policy, user_status

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
    policy, user_status = verifier_identifiants(client)
    print(f"Politique mots de passe :\n{policy}")
    print(f"Statut utilisateur :\n{user_status}")

    statut = "CONFORME" if policy else "A_REVOIR"
    detail = f"Policy: {policy[:50]}..., User: {user_status[:50]}..."
    enregistrer_resultat("A.8.22", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
