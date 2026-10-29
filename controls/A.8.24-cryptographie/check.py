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

def verifier_crypto(client):
    stdin, stdout, stderr = client.exec_command("grep -E 'Ciphers|MACs|KexAlgorithms' /etc/ssh/sshd_config 2>/dev/null | grep -v '#'")
    config = stdout.read().decode().strip()
    stdin2, stdout2, stderr2 = client.exec_command("ls -la /etc/ssl/certs/ 2>/dev/null | wc -l")
    nb_certs = stdout2.read().decode().strip()
    return config, nb_certs

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
    config, nb_certs = verifier_crypto(client)
    print(f"Configuration crypto SSH :\n{config}")
    print(f"Nombre de certificats : {nb_certs}")

    statut = "CONFORME" if config or int(nb_certs) > 0 else "A_REVOIR"
    detail = f"SSH config: {config[:50]}..., Certs: {nb_certs}"
    enregistrer_resultat("A.8.24", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
