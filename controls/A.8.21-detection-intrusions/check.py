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

def verifier_fail2ban(client):
    # Vérifier si fail2ban est actif
    stdin, stdout, stderr = client.exec_command("systemctl is-active fail2ban")
    actif = stdout.read().decode().strip()
    
    # Vérifier si fail2ban est activé au démarrage
    stdin2, stdout2, stderr2 = client.exec_command("systemctl is-enabled fail2ban")
    active = stdout2.read().decode().strip()
    
    return actif, active

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
    actif, active = verifier_fail2ban(client)
    print(f"fail2ban actif : {actif}")
    print(f"fail2ban activé au démarrage : {active}")

    statut = "CONFORME" if (actif == "active" and active == "enabled") else "A_REVOIR"
    detail = f"Actif: {actif}, Activé: {active}"

    enregistrer_resultat("A.8.21", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
