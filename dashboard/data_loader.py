import sqlite3
import pandas as pd
import re
from datetime import datetime
import os

DB_PATH = "db/conformite.db"
RAPPORT_OPENSCAP = "scan-results/openscap-reports/scan_openscap_report.html"

def get_all_results():
    """Récupère tous les résultats depuis la base SQLite"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM resultats ORDER BY id", conn)
    conn.close()
    return df

def get_score_openscap():
    """Extrait le score depuis le rapport HTML OpenSCAP"""
    try:
        with open(RAPPORT_OPENSCAP, 'r') as f:
            content = f.read()
            # Chercher le score (ex: 69.05%)
            match = re.search(r'Score.*?([0-9.]+)%', content)
            if match:
                return float(match.group(1))
            return None
    except FileNotFoundError:
        return None

def get_compliance_stats():
    """Calcule les statistiques de conformité"""
    df = get_all_results()
    total = len(df)
    conformes = len(df[df['statut'] == 'CONFORME'])
    a_revoir = len(df[df['statut'] == 'A_REVOIR'])
    
    # Score global (pourcentage de conformité)
    score_global = (conformes / total * 100) if total > 0 else 0
    
    # Détail par contrôle
    controles = df[['controle', 'statut', 'detail']].to_dict('records')
    
    return {
        'total': total,
        'conformes': conformes,
        'a_revoir': a_revoir,
        'score_global': round(score_global, 1),
        'score_openscap': get_score_openscap(),
        'controles': controles
    }
