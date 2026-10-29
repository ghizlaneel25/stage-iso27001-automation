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

def verifier_ntp(client):
    # Vérifier si chrony est actif
    stdin, stdout, stderr = client.exec_command("systemctl is-active chrony")
    actif = stdout.read().decode().strip()
    
    # Vérifier si la synchronisation NTP est active
    stdin2, stdout2, stderr2 = client.exec_command("timedatectl show --property=NTPSynchronized --value")
    synchro = stdout2.read().decode().strip()
    
    return actif, synchro

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
    actif, synchro = verifier_ntp(client)
    print(f"Service chrony : {actif}")
    print(f"Synchronisation NTP : {synchro}")

    statut = "CONFORME" if (actif == "active" and synchro == "yes") else "A_REVOIR"
    detail = f"chrony: {actif}, NTP synchro: {synchro}"

    enregistrer_resultat("A.8.17", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
