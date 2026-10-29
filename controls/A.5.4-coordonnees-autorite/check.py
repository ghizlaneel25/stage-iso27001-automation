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

def verifier_coordonnees(client):
    stdin, stdout, stderr = client.exec_command("cat /etc/issue 2>/dev/null | grep -E 'contact|email|@' || echo 'Aucun contact'")
    contact = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("cat /etc/motd 2>/dev/null | grep -E 'contact|email|@' || echo 'Aucun contact MOTD'")
    contact2 = stdout2.read().decode().strip()
    return contact, contact2

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
    contact, contact2 = verifier_coordonnees(client)
    print(f"Contact issue : {contact}")
    print(f"Contact MOTD : {contact2}")

    tous_contacts = f"{contact} {contact2}".strip()
    statut = "CONFORME" if "Aucun" not in tous_contacts else "A_REVOIR"
    detail = f"Contacts: {tous_contacts}"
    enregistrer_resultat("A.5.4", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
