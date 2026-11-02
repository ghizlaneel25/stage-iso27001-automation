import sqlite3
import pandas as pd
from datetime import datetime

# Connexion à la base
conn = sqlite3.connect("db/conformite.db")

# Récupérer tous les résultats
df = pd.read_sql_query("""
    SELECT 
        controle,
        statut,
        date_scan,
        detail
    FROM resultats 
    ORDER BY controle
""", conn)
conn.close()

# Ajouter une colonne pour la loi 05.20
df['Respecte loi 05.20'] = df['controle'].apply(
    lambda x: 'OUI' if x.startswith('A.8') else 'NON'
)

# Ajouter une colonne de description
descriptions = {
    "A.5.1": "Politiques de sécurité",
    "A.5.2": "Rôles et responsabilités",
    "A.5.3": "Ségrégation des tâches",
    "A.5.4": "Responsabilités de la direction",
    "A.5.5": "Contact avec les autorités",
    "A.5.6": "Contact avec les groupes d'intérêt",
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
df['Description'] = df['controle'].map(descriptions).fillna('À définir')

# Ajouter une colonne "Type d'automatisation"
def get_automatisation(controle):
    auto_controls = ["A.5.1", "A.5.2", "A.5.3", "A.5.4", "A.5.5", "A.5.6",
                     "A.8.1", "A.8.2", "A.8.3", "A.8.4", "A.8.5", "A.8.6",
                     "A.8.7", "A.8.8", "A.8.9", "A.8.10", "A.8.11", "A.8.12",
                     "A.8.13", "A.8.14", "A.8.15", "A.8.16", "A.8.17", "A.8.18",
                     "A.8.19", "A.8.20", "A.8.21", "A.8.22", "A.8.23", "A.8.24"]
    if controle in auto_controls:
        return "Automatique (script SSH)"
    else:
        return "Manuel (saisie)"

df['Type d\'automatisation'] = df['controle'].apply(get_automatisation)

# Ajouter une colonne "Lien avec loi 05.20"
df['Lien loi 05.20'] = df['controle'].apply(
    lambda x: 'Sécurité des systèmes d\'information' if x.startswith('A.8') else 'Gouvernance et organisation'
)

# Exporter en Excel
df.to_excel('rapport_conformite_iso27001_complet.xlsx', index=False)
print('✅ Rapport Excel généré : rapport_conformite_iso27001_complet.xlsx')
print(f'Total contrôles : {len(df)}')
print(f'Conformes : {len(df[df["statut"] == "CONFORME"])}')
print(f'À revoir : {len(df[df["statut"] == "A_REVOIR"])}')
print(f'Non applicables : {len(df[df["statut"] == "NON_APPLICABLE"])}')
print(f'En attente : {len(df[df["statut"] == "EN_ATTENTE"])}')
