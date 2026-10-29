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

def verifier_inventaire(client):
    stdin, stdout, stderr = client.exec_command("dpkg -l | wc -l")
    nb_packages = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("systemctl list-units --type=service --state=running | wc -l")
    nb_services = stdout2.read().decode().strip()
    return nb_packages, nb_services

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
    nb_packages, nb_services = verifier_inventaire(client)
    print(f"Nombre de packages : {nb_packages}")
    print(f"Nombre de services actifs : {nb_services}")
    statut = "CONFORME" if int(nb_packages) > 100 else "A_REVOIR"
    detail = f"Packages: {nb_packages}, Services actifs: {nb_services}"
    enregistrer_resultat("A.8.1", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
