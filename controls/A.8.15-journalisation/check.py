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

def verifier_auditd(client):
    # Vérifier si auditd est actif
    stdin, stdout, stderr = client.exec_command("systemctl is-active auditd")
    actif = stdout.read().decode().strip()
    
    # Vérifier la taille du fichier de log
    stdin2, stdout2, stderr2 = client.exec_command("ls -lh /var/log/audit/audit.log 2>/dev/null | awk '{print $5}'")
    taille = stdout2.read().decode().strip()
    
    # Vérifier si des logs récents existent
    stdin3, stdout3, stderr3 = client.exec_command("find /var/log/audit -name '*.log' -mtime -1 2>/dev/null | wc -l")
    recent = stdout3.read().decode().strip()
    
    return actif, taille, recent

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
    actif, taille, recent = verifier_auditd(client)
    print(f"auditd actif : {actif}")
    print(f"Taille logs : {taille}")
    print(f"Logs récents : {recent}")

    statut = "CONFORME" if (actif == "active" and int(recent) > 0) else "A_REVOIR"
    detail = f"auditd: {actif}, taille: {taille}, logs récents: {recent}"

    enregistrer_resultat("A.8.15", statut, detail)
    print(f"Résultat enregistré : {statut}")
    client.close()
