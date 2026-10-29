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

def verifier_erreurs(client):
    stdin, stdout, stderr = client.exec_command("journalctl -p 3 -n 5 --no-pager 2>/dev/null | wc -l")
    nb_erreurs = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("dmesg | grep -i error | wc -l")
    nb_dmesg = stdout2.read().decode().strip()
    return nb_erreurs, nb_dmesg

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
    nb_erreurs, nb_dmesg = verifier_erreurs(client)
    print(f"Erreurs journal : {nb_erreurs}")
    print(f"Erreurs dmesg : {nb_dmesg}")

    total = int(nb_erreurs) + int(nb_dmesg)
    statut = "CONFORME" if total < 20 else "A_REVOIR"
    detail = f"Journal: {nb_erreurs}, Dmesg: {nb_dmesg}"
    enregistrer_resultat("A.8.18", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
