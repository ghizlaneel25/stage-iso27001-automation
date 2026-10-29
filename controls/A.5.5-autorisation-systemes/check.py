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

def verifier_autorisation(client):
    stdin, stdout, stderr = client.exec_command("ls -la /etc/sudoers.d/ 2>/dev/null | grep -v 'README' | wc -l")
    nb_fichiers = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("ls -la /etc/security/ 2>/dev/null | grep '.conf' | wc -l")
    nb_conf = stdout2.read().decode().strip()
    return nb_fichiers, nb_conf

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
    nb_fichiers, nb_conf = verifier_autorisation(client)
    print(f"Fichiers sudoers.d : {nb_fichiers}")
    print(f"Fichiers de configuration : {nb_conf}")

    total = int(nb_fichiers) + int(nb_conf)
    statut = "CONFORME" if total > 0 else "A_REVOIR"
    detail = f"Fichiers sudoers: {nb_fichiers}, Config: {nb_conf}"
    enregistrer_resultat("A.5.5", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
