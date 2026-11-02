import pandas as pd

# Lire le fichier Excel
df = pd.read_excel('rapport_conformite_iso27001_complet.xlsx')

# Exporter en CSV
df.to_csv('rapport_conformite_iso27001_complet.csv', index=False, encoding='utf-8')
print('✅ Fichier CSV généré : rapport_conformite_iso27001_complet.csv')
