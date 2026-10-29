import paramiko
import sqlite3
from datetime import datetime, date

HOTE = "192.168.119.142"
UTILISATEUR = "ghiz"
CLE_PRIVEE = "/home/kali/.ssh/id_ed25519"

def se_connecter():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOTE, username=UTILISATEUR, key_filename=CLE_PRIVEE)
    return client

def verifier_revue(client):
    stdin, stdout, stderr = client.exec_command("find /etc/security -name '*.pdf' -o -name '*.md' 2>/dev/null | head -1")
    fichier = stdout.read().decode().strip()
    if fichier:
        stdin2, stdout2, stderr2 = client.exec_command(f"stat -c %y {fichier} 2>/dev/null | cut -d' ' -f1")
        date_modif = stdout2.read().decode().strip()
        return fichier, date_modif
    return "Aucun fichier", "N/A"

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
    fichier, date_modif = verifier_revue(client)
    print(f"Fichier politique : {fichier}")
    print(f"Dernière modification : {date_modif}")

    statut = "CONFORME" if date_modif != "N/A" else "A_REVOIR"
    detail = f"Fichier: {fichier}, Date: {date_modif}"
    enregistrer_resultat("A.5.2", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
