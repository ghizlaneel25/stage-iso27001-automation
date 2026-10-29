import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import get_compliance_stats, get_all_results

# Configuration de la page
st.set_page_config(
    page_title="Tableau de bord ISO 27001",
    page_icon="🛡️",
    layout="wide"
)

# Titre
st.title("🛡️ Tableau de bord - Audit ISO 27001")
st.markdown("**Automatisation des contrôles A.5 et A.8**")
st.markdown("---")

# Chargement des données
stats = get_compliance_stats()

# --- SECTION 1 : Indicateurs clés ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Score global", f"{stats['score_global']}%", 
              delta=f"{stats['conformes']}/{stats['total']} conformes")

with col2:
    st.metric("✅ Conformes", stats['conformes'], delta_color="off")

with col3:
    st.metric("⚠️ À revoir", stats['a_revoir'], delta_color="off")

with col4:
    if stats['score_openscap']:
        st.metric("🔍 Score OpenSCAP", f"{stats['score_openscap']}%")
    else:
        st.metric("🔍 Score OpenSCAP", "Non disponible")

st.markdown("---")

# --- SECTION 2 : Répartition des statuts (Graphique) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Répartition des contrôles")
    df_stats = pd.DataFrame({
        'Statut': ['Conforme', 'À revoir'],
        'Nombre': [stats['conformes'], stats['a_revoir']]
    })
    fig = px.pie(df_stats, values='Nombre', names='Statut', 
                 color='Statut',
                 color_discrete_map={'Conforme': '#2ecc71', 'À revoir': '#e74c3c'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Détail des contrôles")
    for ctrl in stats['controles']:
        if ctrl['statut'] == 'CONFORME':
            emoji = "✅"
            color = "green"
        else:
            emoji = "❌"
            color = "red"
        st.markdown(f"{emoji} **{ctrl['controle']}** : {ctrl['statut']}")
        if ctrl['detail']:
            st.caption(f"📝 {ctrl['detail']}")

st.markdown("---")

# --- SECTION 3 : Tableau détaillé ---
st.subheader("📋 Liste complète des résultats")

# Récupération des données
df = get_all_results()

# Nettoyer l'affichage
df_display = df[['controle', 'statut', 'detail', 'date_scan']].copy()
df_display.columns = ['Contrôle', 'Statut', 'Détail', 'Date du scan']

# Ajouter une couleur selon le statut
def color_status(val):
    if val == 'CONFORME':
        return 'background-color: #d4edda; color: #155724'
    elif val == 'A_REVOIR':
        return 'background-color: #f8d7da; color: #721c24'
    return ''

st.dataframe(
    df_display.style.map(color_status, subset=['Statut']),
    use_container_width=True,
    height=300
)

st.markdown("---")

# --- SECTION 4 : Recommandations ---
st.subheader("💡 Recommandations")

recommandations = []

# Vérifier chaque contrôle pour générer des recommandations
for ctrl in stats['controles']:
    if ctrl['statut'] == 'A_REVOIR':
        if ctrl['controle'] == 'A.8.7':
            recommandations.append("📌 **A.8.7** : Installez ClamAV (`sudo apt install clamav clamav-daemon`)")
        elif ctrl['controle'] == 'A.8.9':
            recommandations.append("📌 **A.8.9** : Appliquez les corrections SSH, nftables et AIDE pour améliorer le score")
        elif ctrl['controle'] == 'A.8.15':
            recommandations.append("📌 **A.8.15** : Activez auditd (`sudo systemctl enable --now auditd`)")
        elif ctrl['controle'] == 'A.8.17':
            recommandations.append("📌 **A.8.17** : Activez chrony (`sudo systemctl enable --now chrony`)")
        elif ctrl['controle'] == 'A.8.20':
            recommandations.append("📌 **A.8.20** : Configurez nftables avec des règles de base")

if recommandations:
    for rec in recommandations:
        st.warning(rec)
else:
    st.success("✅ Tous les contrôles sont conformes !")

st.markdown("---")

# --- SECTION 5 : Information système ---
with st.expander("ℹ️ Informations système"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Machine cible** : Ubuntu Server 22.04")
        st.write(f"**IP** : 192.168.119.142")
        st.write(f"**Dernière mise à jour** : {df['date_scan'].max() if not df.empty else 'Non disponible'}")
    with col2:
        st.write("**Outils utilisés** :")
        st.write("- ✅ OpenSCAP (scan CIS Level 1)")
        st.write("- ✅ Lynis (score: 56/100)")
        st.write("- ✅ Scripts Python (7 contrôles)")

st.caption("🛡️ Projet ISO 27001 - Audit automatisé | Kali + Ubuntu Server")
