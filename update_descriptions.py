import sqlite3

descriptions = {
    "A.5.7": "Renseignement sur les menaces",
    "A.5.8": "Sécurité de l'information dans la gestion de projet",
    "A.5.9": "Inventaire des informations et actifs",
    "A.5.10": "Utilisation acceptable des informations et actifs",
    "A.5.11": "Retour des actifs",
    "A.5.12": "Classification des informations",
    "A.5.13": "Étiquetage des informations",
    "A.5.14": "Transfert des informations",
    "A.5.15": "Contrôle d'accès",
    "A.5.16": "Gestion des identités",
    "A.5.17": "Informations d'authentification",
    "A.5.18": "Droits d'accès",
    "A.5.19": "Sécurité de l'information dans les relations avec les fournisseurs",
    "A.5.20": "Traitement de la sécurité de l'information dans les accords avec les fournisseurs",
    "A.5.21": "Gestion de la sécurité de l'information dans la chaîne d'approvisionnement TIC",
    "A.5.22": "Suivi, révision et gestion des changements des services fournisseurs",
    "A.5.23": "Sécurité de l'information pour l'utilisation des services cloud",
    "A.5.24": "Planification et préparation de la gestion des incidents de sécurité",
    "A.5.25": "Évaluation et décision sur les événements de sécurité",
    "A.5.26": "Réponse aux incidents de sécurité",
    "A.5.27": "Apprentissage des incidents de sécurité",
    "A.5.28": "Collecte de preuves",
    "A.5.29": "Sécurité de l'information en cas de perturbation",
    "A.5.30": "Préparation des TIC à la continuité d'activité",
    "A.5.31": "Exigences légales, réglementaires et contractuelles",
    "A.5.32": "Droits de propriété intellectuelle",
    "A.5.33": "Protection des enregistrements",
    "A.5.34": "Confidentialité et protection des PII",
    "A.5.35": "Revue indépendante de la sécurité de l'information",
    "A.5.36": "Conformité avec les politiques, règles et normes",
    "A.5.37": "Procédures opérationnelles documentées",
    "A.8.25": "Cycle de vie de développement sécurisé",
    "A.8.26": "Exigences de sécurité des applications",
    "A.8.27": "Principes d'architecture système sécurisée",
    "A.8.28": "Codage sécurisé",
    "A.8.29": "Tests de sécurité en développement",
    "A.8.30": "Développement externalisé",
    "A.8.31": "Séparation des environnements",
    "A.8.32": "Gestion des changements",
    "A.8.33": "Informations de test",
    "A.8.34": "Protection des systèmes lors des audits"
}

conn = sqlite3.connect("db/conformite.db")
cur = conn.cursor()
for controle, description in descriptions.items():
    # Vérifier si le contrôle existe déjà
    cur.execute("SELECT COUNT(*) FROM resultats WHERE controle = ?", (controle,))
    if cur.fetchone()[0] == 0:
        # Créer une entrée par défaut
        cur.execute(
            "INSERT INTO resultats (controle, statut, detail) VALUES (?, ?, ?)",
            (controle, "EN_ATTENTE", f"Description: {description}")
        )
conn.commit()
conn.close()
print("✅ Descriptions ajoutées")
