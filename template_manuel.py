import sqlite3
from datetime import datetime

# À MODIFIER POUR CHAQUE CONTRÔLE
CONTROLE = "A.X.X"
DESCRIPTION = "Description du contrôle"

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
    print("=" * 50)
    print(f"{CONTROLE} - {DESCRIPTION}")
    print("=" * 50)
    print("Ce contrôle nécessite une vérification manuelle.")
    print()
    print("1 - CONFORME (le contrôle est respecté)")
    print("2 - A_REVOIR (le contrôle n'est pas respecté)")
    print("3 - NON_APPLICABLE (le contrôle ne s'applique pas)")
    print()
    choix = input("Votre choix (1/2/3) : ")

    if choix == "1":
        statut = "CONFORME"
    elif choix == "2":
        statut = "A_REVOIR"
    elif choix == "3":
        statut = "NON_APPLICABLE"
    else:
        statut = "A_REVOIR"

    detail = input("Détail / Justification (ex: 'Politique existante', 'Non implémenté') : ")
    enregistrer_resultat(CONTROLE, statut, f"Vérification manuelle : {detail}")
    print()
    print(f"✅ Résultat enregistré : {statut}")
