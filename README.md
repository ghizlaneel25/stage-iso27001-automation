# 🛡️ Automatisation de l'Audit ISO/IEC 27001

## 📌 Description
Système d'audit automatisé pour vérifier la conformité d'un serveur Ubuntu aux contrôles de sécurité des annexes A.5 (organisationnels) et A.8 (technologiques) de la norme ISO/IEC 27001:2022.

Projet réalisé dans le cadre d'un stage d'été à la **Caisse Marocaine des Retraites (CMR)**.

---

## 🏗️ Architecture

Le système repose sur une architecture à deux machines virtuelles communiquant de manière sécurisée via SSH.

**Kali Linux (Poste de Contrôle)**
- Exécute les scripts Python.
- Stocke les résultats dans la base SQLite.
- Affiche le Dashboard Streamlit.

**Ubuntu Server (Cible Auditée)**
- Reçoit les commandes via SSH.
- Exécute les outils d'audit (OpenSCAP, Lynis).
- Vérifie les services système (auditd, chrony, nftables).

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|-------------|------|
| **Python 3** | Langage des scripts d'audit |
| **Paramiko** | Connexion SSH sécurisée |
| **OpenSCAP** | Audit de conformité CIS Benchmark |
| **Lynis** | Score de durcissement (Hardening Index) |
| **Streamlit** | Dashboard interactif |
| **SQLite** | Base de données des résultats |
| **LaTeX** | Génération du rapport |

---

## 📊 Résultats

| Métrique | Valeur |
|----------|--------|
| **Contrôles couverts** | 71 (100% du périmètre A.5 + A.8) |
| **Contrôles automatisés** | 30 |
| **Contrôles manuels** | 41 |
| **Score global** | 53,8% (42/70 conformes) |
| **Score OpenSCAP** | 73,12% |

---

## 📁 Structure du projet

```text
stage-iso27001-automation/
├── controls/              # Scripts des 71 contrôles
├── dashboard/             # Application Dashboard Streamlit
├── data/                  # Fichiers de données (CSV)
├── scripts/               # Scripts utilitaires (Excel, templates)
└── db/                    # Base SQLite
